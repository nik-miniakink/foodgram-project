from django import forms
from django.forms import ModelForm

from .models import Recipes, IngredientIncomposition

class RecipeForm(ModelForm):
    class Meta:
        model = Recipes
        fields = ('name', "time", "description", "image",)


class ING(ModelForm):
    class Meta:
        model = IngredientIncomposition
        fields = ('ingredient','quantity')
