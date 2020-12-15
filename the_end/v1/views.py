import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse

from .form import RecipeForm
from .models import User, Tag, Recipes, IngredientIncomposition, \
    Ingredient, Follow, Favorite, ShoppingList


tags_list = {}


def index(request):
    """
    Отрисовывает главную страницу и показывает по 6 постов на странице
    При наличии выбраных тэгов производит фильтрафию рецептов по тэгу
    """

    tag = request.GET.get("tag_list")
    if tag is not None:
        if tag not in tags_list:
            tags_list[tag] = tag
        else:
            del tags_list[tag]

    if len(tags_list) > 0:
        recipe_list = Recipes.objects.filter(tag__slug__in=tags_list).order_by("-pub_date").all()
    else:
        recipe_list = Recipes.objects.order_by("-pub_date").all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    tags = Tag.objects.all()

    return render(request, 'indexAuth.html', {
        'page': page,
        'paginator': paginator,
        'recipes': recipe_list,
        'page_number': page_number,
        'tags': tags,
        'tags_list': tags_list,
    })


def recipe_view(request, recipe_id):
    """
    Отрисовывает страницу одиночного рецепта по id
    :return:
    """
    recipe = get_object_or_404(Recipes, id=recipe_id)
    tags = Tag.objects.filter(recipes=recipe)
    ings = IngredientIncomposition.objects.filter(recipes=recipe)

    return render(request, 'singlePage.html', {
        'recipe': recipe,
        'tags': tags,
        'ings': ings,
    })


def author_list(request, user_id):
    """
    Отрисовывает страницу выбранного автора по id автора
    При наличии выделения тэгов происходит фильтрация
    """
    tag = request.GET.get("tag_list")
    if tag is not None:
        if tag not in tags_list:
            tags_list[tag] = tag
        else:
            del tags_list[tag]
    user = get_object_or_404(User, id=user_id)

    if len(tags_list) > 0:
        recipe_list = Recipes.objects.filter(tags__slug__in=tags_list, author=user).order_by("-pub_date").all()
    else:
        recipe_list = Recipes.objects.filter(author=user).order_by("-pub_date").all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    tags = Tag.objects.all()

    return render(request, 'indexAuth.html', {
        'page': page,
        'paginator': paginator,
        'recipes': recipe_list,
        'page_number': page_number,
        'tags': tags,
        'tags_list': tags_list,
    })


@login_required
def follow_index(request):

    """
    Показывает список рецептов полписанных авторов
    """
    my_follow = Follow.objects.filter(
        user_id=request.user.id).order_by("author").all()
    authors = User.objects.filter(following__in=my_follow)

    paginator = Paginator(my_follow, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, 'myFollow.html', {
        'page': page,
        'paginator': paginator,
        'follow': my_follow,
        'authors': authors,
    })


@login_required
def favorite(request):
    """
    Отрисовывает страницу избранных рецептов
    При выбранных тэгах происходит фильтрация
    :param request:
    :return:
    """
    tag = request.GET.get("tag_list")
    if tag is not None:
        if tag not in tags_list:
            tags_list[tag] = tag
        else:
            del tags_list[tag]

    if len(tags_list) > 0:
        recipe_list = Recipes.objects.filter(tag__slug__in=tags_list,
                                             favorite_recipe__fuser__id=request.user.id).order_by("-pub_date").all()
    else:
        recipe_list = Recipes.objects.filter(favorite_recipe__fuser__id=request.user.id).order_by("-pub_date").all()

    tags = Tag.objects.all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'recipes': recipe_list,
        'page_number': page_number,
        'tags': tags,
        'tags_list': tags_list,
    }
    return render(request, 'favorite.html', context)


@login_required
def add_favorite(request):
    """
    Добавляет рецепт в избранное

    """
    if request.method == "POST":
        recipe_id = int(json.loads(request.body).get('id'))
        recipe = get_object_or_404(Recipes, id=recipe_id)
        created = Favorite.objects.get_or_create(
            fuser=request.user, recipe=recipe)
        print(created)
        if not created:
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def delete_favorite(request, recipe_id):
    """
    Исключает рецепт из избранного
    """
    if request.method == "DELETE":
        user = request.user
        deleted = Favorite.objects.filter(
            fuser_id=user.id, recipe_id=recipe_id).delete()
        print(deleted)
        return JsonResponse({'success': True}) if deleted else JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False})


@login_required
def add_subscription(request):
    """
    Создает подписку
    """
    following_id = int(json.loads(request.body).get('id'))
    following = get_object_or_404(User, id=following_id)

    if request.user.id != following_id:
        created = Follow.objects.get_or_create(
            user=request.user, author=following)

    return JsonResponse({'success': True}) if created else JsonResponse({'success': False})


@login_required
def delete_subscription(request, following_id):
    """
    Удаляет подписку
    """
    deleted = Follow.objects.filter(
        user_id=request.user.id, author_id=following_id).delete()
    return JsonResponse({'success': True}) if deleted else JsonResponse({'success': False})

@login_required
def add_purchases(request):
    """
    Добавляет рецепт в покупки
    """
    if request.method == "POST":
        recipe_id = int(json.loads(request.body).get('id'))
        created = ShoppingList.objects.get_or_create(
            user_id=request.user.id, recipe_id=recipe_id)
        if not created:
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def delete_purchases(request, recipe_id):
    if request.method == "DELETE":
        deleted = ShoppingList.objects.filter(
            user_id=request.user.id, recipe_id=recipe_id).delete()
        return JsonResponse({'success': True}) if deleted else JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

@login_required
def get_ingredients(request):
    """
    Вытягивает ингредиенты из формы
    """
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = int(request.POST[
                f'valueIngredient_{_[1]}']
            )
    return ingredients

@login_required
def get_ingredients_js(request):
    """
    По первым буквам делает запрос к js и получает в ответ игредиенты начинающиеся на данные буквы
    """
    text = request.GET.get('query')
    data = []
    ingredients = Ingredient.objects.filter(
        name__startswith=text).all()
    for ingredient in ingredients:
        data.append(
            {'title': ingredient.name, 'dimension': ingredient.units_of_measurement})

    return JsonResponse(data, safe=False)


@login_required
def user_recipe_new(request):
    """
    Создание рецепта
    """
    user = User.objects.get(username=request.user)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None)

    if request.method == 'POST':
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')
        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            print(request.POST)
            recipe_tags_list = request.POST.getlist('tag')
            for tag_id in recipe_tags_list:
                tag = Tag.objects.get(id=tag_id)
                recipe.tag.add(tag)

            for ing_name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, name=ing_name)
                IngredientIncomposition.objects.create(
                    ingredient=ingredient,
                    quantity=quantity)
            form.save_m2m()
            return redirect('index')
    else:
        form = RecipeForm()

    tags = Tag.objects.all()
    return render(request, 'formRecipe.html', {
        'form': form,
        'tags': tags,
    })


@login_required
def user_recipe_edit(request, recipe_id):
    """
    Редактирование рецепта
    """

    recipe = get_object_or_404(Recipes, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe_view', id=recipe_id)

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if request.method == "POST":
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')
        if form.is_valid():
            form.save()
            IngredientIncomposition.objects.filter(recipes=recipe).delete()

            for ing_name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, name=ing_name)
                IngredientIncomposition.objects.create(
                    ingredient=ingredient,
                    quantity=quantity)

            return redirect('recipe_view', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    tags = Tag.objects.all()
    tags_list = Tag.objects.filter(recipes=recipe)

    ingredients = IngredientIncomposition.objects.filter(recipes=recipe.id)

    return render(request, 'formChangeRecipe.html', {
        'form': form,
        'recipe': recipe,
        'tags': tags,
        'ingredients': ingredients,
        'tags_list': tags_list
    })


@login_required
def shopping_list(request):
    """
    Отрисовывает страницу покупок
    :param request:
    :return:
    """
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    return render(
        request,
        'shopping-list.html',
        {'shopping_list': shopping_list}
    )
