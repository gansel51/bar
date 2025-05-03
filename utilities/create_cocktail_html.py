import json
import os
from textwrap import dedent

def generate_cocktail_html(cocktail_name):
    """
    Generate HTML for a cocktail card based on cocktail name in recipes.json
    
    Args:
        cocktail_name: The name of the cocktail (e.g. "manhattan", "gin-fizz")
        
    Returns:
        String with HTML for the cocktail card
    """
    # Load recipes.json
    json_path = "docs/recipes.json"

    try:
        with open(json_path, 'r') as f:
            recipes = json.load(f)
    except Exception as e:
        print(f"Error loading recipes.json: {e}")
        return None
    
    # Check if cocktail exists
    if cocktail_name not in recipes:
        print(f"Cocktail '{cocktail_name}' not found in recipes.json")
        return None
    
    # Get recipe data
    recipe = recipes[cocktail_name]

    # Define spirit categories
    spirit_categories = {
        "whiskey": ["bourbon", "rye", "scotch", "irish", "whiskey", "whisky"],
        "gin": ["gin"],
        "rum": ["rum"],
        "tequila-mezcal": ["tequila", "mezcal", "sotol"],
        "vodka": ["vodka"],
        "brandy": ["brandy", "cognac"]
    }
    
    # Define icons based on base spirit
    icon_map = {
        "whiskey": "🥃",
        "bourbon": "🥃",
        "rye": "🥃",
        "scotch": "🥃",
        "irish": "🥃",
        "gin": "🍸",
        "rum": "🍹",
        "tequila": "🍸",
        "mezcal": "🍸",
        "vodka": "🍸",
        "brandy": "🥃",
        "cognac": "🥃"
    }
    
    # Default icon and base spirit
    icon = "🍸"
    base_spirit = "other"
    
    # Try to determine icon and base spirit from ingredients
    if "ingredients" in recipe:
        for ingredient in recipe["ingredients"]:
            ingredient_lower = ingredient.lower()
            
            # First check for icon
            for spirit, spirit_icon in icon_map.items():
                if spirit in ingredient_lower:
                    icon = spirit_icon
                    break
                    
            # Then check for base spirit category
            for category, spirits in spirit_categories.items():
                if any(spirit in ingredient_lower for spirit in spirits):
                    base_spirit = category
                    break
            
            # If we found a base spirit, we can stop checking ingredients
            if base_spirit != "other":
                break
    
    # Get name in proper format
    display_name = recipe.get("name", cocktail_name.replace("-", " ").title())
    
    # Get ingredients
    ingredients = recipe.get("ingredients", [])
    ingredients_html = "\n          ".join([f"<li>{ingredient}</li>" for ingredient in ingredients])
    
    # Get description
    description = recipe.get("description", "A delicious cocktail.")
    
    # Generate HTML for the cocktail card with proper indentation
    html = dedent(f'''\
        <div class="cocktail" data-type="{base_spirit}">
          <span class="icon">{icon}</span>
          <h2>{display_name}</h2>
          <div class="cocktail-details">
            <div class="ingredients">
              <h3>Ingredients:</h3>
              <ul>
                {ingredients_html}
              </ul>
            </div>
            <div class="description">
              <p>{description}</p>
            </div>
          </div>
          <br>
          <div class="cocktail-footer">
            <button class="btn btn-small view-recipe" data-cocktail="{cocktail_name}">Full Recipe</button>
          </div>
        </div>''')
    
    return html


def format_json_file(input_file, output_file=None):
    """
    Format a JSON file with proper indentation and structure
    
    Args:
        input_file: Path to the input JSON file
        output_file: Path to the output JSON file (defaults to same as input)
    """
    if output_file is None:
        output_file = input_file
        
    try:
        with open(input_file, 'r') as f:
            # Remove any potential JavaScript comments that make the JSON invalid
            content = f.read()
            lines = content.splitlines()
            cleaned_lines = [line for line in lines if not line.strip().startswith('//')]
            cleaned_content = '\n'.join(cleaned_lines)
            
            # Parse the cleaned JSON
            data = json.loads(cleaned_content)
        
        # Write the formatted JSON
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, sort_keys=False)
            
        print(f"JSON file formatted successfully: {output_file}")
        return True
    except Exception as e:
        print(f"Error formatting JSON file: {e}")
        return False


def generate_all_cocktail_html():
    """
    Generate HTML for all cocktails in recipes.json
    
    Returns:
        String with HTML for all cocktail cards
    """
    # Load recipes.json
    json_path = "docs/recipes.json"
    
    # Format the JSON file first
    format_json_file(json_path)
    
    try:
        with open(json_path, 'r') as f:
            recipes = json.load(f)
    except Exception as e:
        print(f"Error loading recipes.json: {e}")
        return None
    
    # Generate HTML for each cocktail
    all_html = ""
    for cocktail_name in recipes.keys():
        cocktail_html = generate_cocktail_html(cocktail_name)
        if cocktail_html:
            all_html += cocktail_html + "\n\n"
    
    return all_html


# Example usage:
if __name__ == "__main__":
    # Format the JSON file first
    format_json_file("docs/recipes.json")
    
    # Generate HTML for a single cocktail
    cocktail_input = "martini"
    generated_drink = generate_cocktail_html(cocktail_input)
    if generated_drink:
        with open("generated_single_drink.html", "w") as f:
            f.write(generated_drink)
        print(f"Generated HTML for {cocktail_input} saved to generated_single_drink.html")
    
    # Generate HTML for all cocktails
    # all_html = generate_all_cocktail_html()
    # if all_html:
    #     with open("generated_all_drinks.html", "w") as f:
    #         f.write(all_html)
    #     print("Generated HTML for all cocktails saved to generated_all_drinks.html")