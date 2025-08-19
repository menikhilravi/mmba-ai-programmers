from google import genai
from pydantic import BaseModel, Field
from typing import List
from pprint import pprint
import os
import json

# TODO: Add a new Ingredients model that can be used in the Recipe model with the following properties:
# - amount
# - unit
# - name
class Ingredients(BaseModel):
    amount: float = Field(description="Amount of the ingredient")
    unit: str = Field(description="Unit of the ingredient (e.g., cups, tablespoons, grams)")
    name: str = Field(description="Name of the ingredient")

class Recipe(BaseModel):
    """
    Use this model when working with complete cooking recipes.
    """
    title: str = Field(description="Name of the recipe")
    ingredients: List[Ingredients] = Field(description="List of ingredients needed for the recipe")
    instructions: List[str] = Field(description="Step-by-step instructions to prepare the recipe")

def get_recipe_from_text(recipe_text: str) -> Recipe:
    """
    Convert recipe text into a structured Recipe object using OpenAI.
    """
    client = genai.Client()

    # Make the API call
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Convert this recipe into the specified format:\n\n{recipe_text}",
        config={
            "response_mime_type": "application/json",
            "response_schema": Recipe
        }
    )

    return response.text

# Example usage
if __name__ == "__main__":
    # Read recipe text from file
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    recipe_path = os.path.join(script_dir, "mac_and_cheese_recipe.txt")
    with open(recipe_path, "r") as file:
        recipe_text = file.read()

    # Get structured recipe
    recipe = json.loads(get_recipe_from_text(recipe_text))
    
    # Print results
    pprint(recipe["ingredients"][0])
    # pprint(recipe) # to see the whole object