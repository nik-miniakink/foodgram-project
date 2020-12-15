from django import template

from ..models import Favorite, ShoppingList, Follow
from ..models import Recipes


register = template.Library()
recipe_on_page = 3


@register.filter(name='items_follow')
def get_filter_values(request, author_id):
    """
    Возвращает N первых рецепта по id автора
    """
    return Recipes.objects.filter(author=author_id).order_by("pub_date")[:recipe_on_page]


@register.filter(name='count_recipises')
def get_filter_values(request, author_id):
    """
    Возращает количество рецептов без показанных на странице
    """
    count = Recipes.objects.filter(author=author_id).count()
    return (count - recipe_on_page)


@register.filter(name='is_favorite')
def get_filter_value(request, recipe_id):
    """
    Возвращет True, если рецепт добавлен у пользователя в избранное
    """
    is_favorites = Favorite.objects.filter(
        fuser=request.user,
        recipe_id=recipe_id).all()
    if is_favorites:
        return True
    return False


@register.filter(name='is_follow')
def get_filter_value(request, author_id):
    is_follow = Follow.objects.filter(
        user=request.user,
        author_id=author_id
    )
    if is_follow:
        return True
    return False


@register.filter(name='count_shoplist')
def get_filter_values(request):
    """
    Возвращает количество рецептов добавленных в покупки
    """
    counts_list = ShoppingList.objects.filter(user=request.user).all()
    if counts_list.count() > 0:
        return counts_list.count()
    return 0


@register.filter(name='is_shoplist')
def get_filter_values(request, recipe_id):
    """
    Возвращает True, еслу пользователь добавил рецепт в список покупок
    """
    is_slist = ShoppingList.objects.filter(
        user=request.user,
        recipe_id=recipe_id).all()
    if is_slist:
        return True
    return False    
