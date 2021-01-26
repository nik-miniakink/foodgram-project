from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def get_recipe_ingredients(shoplist):
    final_dict = {}
    for qwer in shoplist:
        for ing in qwer.recipe.ingredient_in.all():
            name = ing.ingredient.name
            description = ing.ingredient.description
            quantity = ing.quantity
            if name in final_dict and description == final_dict[name][1]:
                final_dict[name][0] += quantity
            else:
                final_dict[name] = [quantity, description]
    return final_dict


def generate_pdf(ingredients, buffer):
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(
        TTFont('FreeSansOblique', 'static/FreeSansOblique.ttf'))
    p.setFont('FreeSansOblique', 20)
    header = "Список ингредиентов:"
    x, y = 30, 800
    p.drawString(x, y, header)
    p.setFont('FreeSansOblique', 15)
    x1, y1 = 50, 790
    for index, ing in enumerate(ingredients):
        text = f"{index + 1}) {ing} - {ingredients[ing][0]} " \
               f"{ingredients[ing][1]}."
        y1 -= 25
        p.drawString(x1, y1, text)
    p.showPage()
    p.save()