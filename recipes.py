class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        try:
            val_float = float(value)
        except (ValueError, TypeError):
            raise ValueError("Количество должно быть положительным")
        
        if val_float <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = val_float

    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self) -> str:
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit


class Recipe:
    def __init__(self, title: str, ingredients: list = None):
        self.title = title
        self.ingredients = []
        if ingredients is not None:
            for ing in ingredients:
                self.add_ingredient(ing)

    def add_ingredient(self, ingredient: Ingredient):
        for ing in self.ingredients:
            if ing == ingredient:
                ing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio) -> bool:
        return isinstance(ratio, (int, float)) and ratio > 0

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("ratio должен быть положительным числом")
        
        scaled_ings = []
        for ing in self.ingredients:
            scaled_ings.append(Ingredient(ing.name, ing.quantity * ratio, ing.unit))
        return Recipe(self.title, scaled_ings)

    def __len__(self) -> int:
        return len(self.ingredients)

    def __str__(self) -> str:
        res = self.title
        for ing in self.ingredients:
            res += "\n- " + str(ing)
        return res


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        
        scaled_recipe = recipe.scale(portions)
        for ing in scaled_recipe.ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self) -> list:
        totals = {}
        for ing, _ in self._items:
            key = (ing.name, ing.unit)
            totals[key] = totals.get(key, 0.0) + ing.quantity
        
        result_list = []
        for (name, unit), qty in totals.items():
            result_list.append(Ingredient(name, qty, unit))
            
        result_list.sort(key=lambda x: x.name)
        return result_list

    def __add__(self, other: 'ShoppingList') -> 'ShoppingList':
        if not isinstance(other, ShoppingList):
            return NotImplemented
        
        new_list = ShoppingList()
        for ing, title in self._items:
            new_list._items.append((Ingredient(ing.name, ing.quantity, ing.unit), title))
        for ing, title in other._items:
            new_list._items.append((Ingredient(ing.name, ing.quantity, ing.unit), title))
        return new_list


class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients: list = None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float) -> 'DietaryRecipe':
        scaled_recipe = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, scaled_recipe.ingredients)

    def __str__(self) -> str:
        return f"[{self.diet_type}] {super().__str__()}"