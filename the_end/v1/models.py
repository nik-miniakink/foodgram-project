from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingredient(models.Model):
    """
    Информация об ингредиенте
    """
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.CharField(max_length=1000, verbose_name='Описание')

    measurement = (
        ('шт', 'шт'),
        ('г', 'г'),
        ('ст.л', 'ст.л'),
        ('ч.л', 'ч.л'),
        ('мл','мл')
    )

    units_of_measurement = models.CharField(choices=measurement, max_length=20, verbose_name='Единицы измерения')

    def __str__(self):
        return f'{self.name} ({self.units_of_measurement})'

class Tag(models.Model):
    """
    Информация о тэгах
    """
    name = models.CharField(max_length=10, null=False, verbose_name='Название')
    slug = models.SlugField(max_length=15, unique=True, null=False, verbose_name='slug')
    style = models.CharField(max_length=15, default='purple', verbose_name='Цвет оформления')

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """
    Информация о рецептах
    """
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Автор')
    name = models.CharField(max_length=200, unique=True, verbose_name='Название рецепта')
    image = models.ImageField(upload_to='irecipes/%d_%m_%Y/')
    description = models.CharField(max_length=1000, verbose_name='Описание ')
    ingredient_in = models.ManyToManyField('IngredientIncomposition',blank=False)
    tag = models.ManyToManyField('Tag')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time = models.PositiveSmallIntegerField(default=10, verbose_name='Время приготовления')

    def __str__(self):
        return self.name


class IngredientIncomposition(models.Model):
    """
    Информация о ингредиентах, входящих в рецепт
    """
    # recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, blank=True, null=False)
    ingredient = models.ForeignKey(Ingredient,on_delete=models.DO_NOTHING)
    quantity = models.SmallIntegerField(verbose_name='Количество')

    def __str__(self):
        return self.ingredient.name


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower", verbose_name="Подписчик")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following", verbose_name="Автор постов")


class Favorite(models.Model):
    fuser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites_user", verbose_name="Пользователь")
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name="favorite_recipe", verbose_name="Рецепт в избранном")


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shoplist_user", verbose_name="Пользователь")
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name="shoplist_recipe", verbose_name="Рецепт с продуктами для покупки")