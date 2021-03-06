from django.urls import path
from . import views


urlpatterns = [
    path("ingredients", views.get_ingredients_js, name="get_ingredients"),

    path("recipe/new/", views.user_recipe_new, name="recipe_new"),
    path("recipe/<int:recipe_id>/", views.recipe_view, name="recipe_view"),
    path("recipe/<int:recipe_id>/edit/", views.user_recipe_edit, name="recipe_edit"),

    path("author/<int:user_id>/",views.author_list, name="author"),

    path("favorite/", views.favorite, name="favorites"),
    path("favorites", views.add_favorite, name="add_favorite"),
    path("favorites/", views.add_favorite, name="add_favorite"),
    path("favorites/<int:recipe_id>",
         views.delete_favorite, name="delete_favorite"),

    path("follow/", views.follow_index, name="follow_index"),

    path("subscriptions", views.add_subscription, name="add_subscription"),
    path("subscriptions/", views.add_subscription, name="add_subscription"),
    path("subscriptions/<int:following_id>",
         views.delete_subscription, name="delete_subscription"),

    path("purchases", views.add_purchases, name="add_purchases"),
    path("purchases/", views.add_purchases, name="add_purchases"),
    path("purchases/<int:recipe_id>",
         views.delete_purchases, name="delete_purchases"),
    path("purchases/<int:recipe_id>/",
         views.delete_purchases, name="delete_purchases"),

    path('shopping-list/', views.shopping_list, name='shopping-list'),
    path("shop_list/get_pdf/", views.send_pdf, name="shop_list_send_pdf"),
    path("", views.index, name="index"),
]
