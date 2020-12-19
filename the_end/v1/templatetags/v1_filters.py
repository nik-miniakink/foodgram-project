
from django import template
from django.conf import settings


from ..models import Favorite, ShoppingList, Follow
from ..models import Recipes


register = template.Library()


@register.filter(name='items_follow')
def get_filter_values(request, author_id):
    """
    Возвращает N первых рецепта по id автора
    """
    return Recipes.objects.filter(author=author_id).order_by("pub_date")[:settings.RECIPE_ON_PAGE]


@register.filter(name='count_recipises')
def get_filter_values(request, author_id):
    """
    Возращает количество рецептов без показанных на странице
    """
    count = Recipes.objects.filter(author=author_id).count()
    return (count - settings.RECIPE_ON_PAGE)


@register.filter(name='is_favorite')
def get_filter_value(request, recipe_id):
    """
    Возвращет True, если рецепт добавлен у пользователя в избранное
    """
    is_favorites = Favorite.objects.filter(
        fuser=request.user,
        recipe_id=recipe_id).exists()
    return is_favorites


@register.filter(name='is_follow')
def get_filter_value(request, author_id):
    """
    Проверяет добавлен
    """
    is_follow = Follow.objects.filter(
        user=request.user,
        author_id=author_id).exists()
    return is_follow


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
        recipe_id=recipe_id).exists()
    return is_slist
