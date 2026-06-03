import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


def test_ingredient_creation():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_invalid_quantity_string():
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        Ingredient("Мука", "не число", "г")

def test_ingredient_invalid_quantity_negative():
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        Ingredient("Мука", -50, "г")

def test_ingredient_str():
    ing = Ingredient("Мука", 500.0, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq_safe():
    ing1 = Ingredient("Мука", 500, "г")
    ing2 = Ingredient("Мука", 200, "г")
    assert ing1 == ing2
    assert ing1 != "просто строка"



def test_recipe_creation():
    recipe = Recipe("Пицца", [Ingredient("Мука", 200, "г")])
    assert recipe.title == "Пицца"
    assert len(recipe) == 1

def test_recipe_add_ingredient_accumulation():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 500.0


def test_shopping_list_add_recipe():
    recipe = Recipe("Пицца", [Ingredient("Мука", 200, "г")])
    sl = ShoppingList()
    sl.add_recipe(recipe, 2)
    res = sl.get_list()
    assert len(res) == 1
    assert res[0].quantity == 400.0

def test_shopping_list_invalid_portions():
    recipe = Recipe("Пицца", [Ingredient("Мука", 200, "г")])
    sl = ShoppingList()
    with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
        sl.add_recipe(recipe, 0)

def test_shopping_list_remove():
    recipe = Recipe("Пицца", [Ingredient("Мука", 200, "г")])
    sl = ShoppingList()
    sl.add_recipe(recipe, 1)
    sl.remove_recipe("Пицца")
    assert len(sl.get_list()) == 0

def test_shopping_list_sorting_and_merging():
    r1 = Recipe("Пицца", [Ingredient("Сыр", 150, "г"), Ingredient("Мука", 200, "г")])
    r2 = Recipe("Паста", [Ingredient("Мука", 100, "г")])
    sl = ShoppingList()
    sl.add_recipe(r1, 1)
    sl.add_recipe(r2, 1)
    
    res = sl.get_list()
    assert len(res) == 2
    assert res[0].name == "Мука"
    assert res[0].quantity == 300.0 
    assert res[1].name == "Сыр"

def test_dietary_recipe_attributes():
    dr = DietaryRecipe("Смузи", "веган", [Ingredient("Банан", 1, "шт")])
    assert dr.diet_type == "веган"
    assert "[веган]" in str(dr)

def test_dietary_recipe_scale_type():
    dr = DietaryRecipe("Смузи", "веган", [Ingredient("Банан", 1, "шт")])
    scaled = dr.scale(2)
    assert isinstance(scaled, DietaryRecipe)
    assert scaled.diet_type == "веган"
    assert scaled.ingredients[0].quantity == 2.0