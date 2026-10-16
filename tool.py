import json
from pathlib import Path


# Find recipes.json in the same folder as this file
RECIPE_FILE = Path(__file__).with_name("recipes.json")


def load_recipes():
    """Load recipes from the JSON database."""

    with RECIPE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_ingredients(text):
    """Convert ingredient names into a standard format."""

    synonyms = {
        "eggs": "egg",
        "tomatoes": "tomato",
        "onions": "onion",
        "potatoes": "potato",
        "carrots": "carrot",
        "cooking oil": "oil"
    }

    ingredients = set()

    for item in text.lower().replace("\n", ",").split(","):
        item = item.strip()

        if item:
            ingredients.add(synonyms.get(item, item))

    return ingredients


def recommend_recipes(user_input):
    """Find and rank recipes using available ingredients."""

    available = normalize_ingredients(user_input)
    recipes = load_recipes()
    results = []

    for recipe in recipes:
        required = set(
            normalize_ingredients(",".join(recipe["ingredients"]))
        )

        matched = available.intersection(required)
        missing = required.difference(available)

        if not matched:
            continue

        match_percentage = round(
            len(matched) / len(required) * 100
        )

        results.append({
            "name": recipe["name"],
            "matched": sorted(matched),
            "missing": sorted(missing),
            "match_percentage": match_percentage,
            "time": recipe.get("time", 0),
            "instructions": recipe.get("instructions", [])
        })

    # Prioritize fewer missing ingredients.
    # Use match percentage and cooking time to break ties.
    results.sort(
        key=lambda item: (
            len(item["missing"]),
            -item["match_percentage"],
            item["time"]
        )
    )

    return results


def display_recipes(recipes):
    """Display recipe recommendations."""

    if not recipes:
        print("No matching recipes found.")
        return

    print("\n===== SMARTCHEF AI RECOMMENDATIONS =====")

    for number, recipe in enumerate(recipes[:5], start=1):
        print(f"\n{number}. {recipe['name']}")
        print(f"Match: {recipe['match_percentage']}%")
        print(f"Cooking time: {recipe['time']} minutes")

        print(
            "Available ingredients: "
            + ", ".join(recipe["matched"])
        )

        if recipe["missing"]:
            print(
                "Missing ingredients: "
                + ", ".join(recipe["missing"])
            )
        else:
            print("All listed ingredients are available!")

        print("\nCooking instructions:")

        for step, instruction in enumerate(
            recipe["instructions"], start=1
        ):
            print(f"{step}. {instruction}")
