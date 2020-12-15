from django.contrib import admin

from .models import Recipes, Ingredient, IngredientIncomposition, Tag, \
    Favorite, Follow, ShoppingList


@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'description', 'pub_date')
    search_fields = ('name',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'units_of_measurement', 'description')


@admin.register(IngredientIncomposition)
class IngredientIncompositionAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'ingredient')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'style', 'slug')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'fuser', 'recipe')
    search_fields = ('fuser', )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', )


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe',)
