import json
import os
from textwrap import dedent

def generate_brew_html(brew_id=None):
    """
    Generate HTML for homebrew entries from brews.json
    
    Args:
        brew_id: Optional specific brew ID to generate. If None, generates all brews.
        
    Returns:
        String with HTML for the brew card(s)
    """
    # Load brews.json
    json_path = "docs/brews.json"

    try:
        with open(json_path, 'r') as f:
            # Remove any potential JavaScript comments
            content = f.read()
            lines = content.splitlines()
            cleaned_lines = [line for line in lines if not line.strip().startswith('//')]
            cleaned_content = '\n'.join(cleaned_lines)
            
            brews = json.loads(cleaned_content)
    except Exception as e:
        print(f"Error loading brews.json: {e}")
        return None
    
    # Function to generate HTML for a single brew
    def generate_single_brew_html(brew_id, brew_data):
        # Determine main stat (hop or grain)
        main_stat_name = "Main Hop" if "main_hop" in brew_data else "Main Grain"
        main_stat_value = brew_data.get("main_hop", brew_data.get("main_grain", "N/A"))
        
        # Generate flavor tags HTML
        flavor_tags = brew_data.get("flavor_tags", [])
        flavor_tags_html = "\n              ".join([f'<span class="flavor-tag">{tag}</span>' for tag in flavor_tags])
        
        # Generate the HTML
        html = dedent(f'''\
          <div class="cocktail">
            <span class="icon">🍺</span>
            <h2>{brew_data.get("batch", "Batch")}: {brew_data.get("name", "Unnamed Brew")}</h2>
            <div class="brew-stats">
              <div class="brew-stat">
                <div class="value">{brew_data.get("stats", {}).get("abv", "N/A")}</div>
                <div class="label">ABV</div>
              </div>
              <div class="brew-stat">
                <div class="value">{brew_data.get("stats", {}).get("ibu", "N/A")}</div>
                <div class="label">IBU</div>
              </div>
              <div class="brew-stat">
                <div class="value">{main_stat_value}</div>
                <div class="label">{main_stat_name}</div>
              </div>
              <div class="brew-stat">
                <div class="value">{brew_data.get("style", "N/A")}</div>
                <div class="label">Style</div>
              </div>
            </div>
            <p>
              {brew_data.get("description", "No description available.")}
            </p>
            <br>
            <p>Flavor notes:</p>
            <div class="flavor-profile">
              {flavor_tags_html}
            </div>
            <button class="btn btn-small brew-details" data-brew="{brew_id}">View Details</button>
          </div>''')
        
        return html
    
    # Generate HTML for specific brew or all brews
    if brew_id:
        if brew_id in brews:
            return generate_single_brew_html(brew_id, brews[brew_id])
        else:
            print(f"Brew '{brew_id}' not found in brews.json")
            return None
    else:
        # Generate HTML for all brews
        all_html = []
        for bid, brew_data in brews.items():
            all_html.append(generate_single_brew_html(bid, brew_data))
        
        return "\n\n".join(all_html)

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

# Example usage
if __name__ == "__main__":
    # First format the JSON file to ensure it's valid
    format_json_file("docs/brews.json")
    
    # Generate HTML for all brews
    all_brews_html = generate_brew_html()
    if all_brews_html:
        print("HTML for all brews:")
        print(all_brews_html)
        
        # Optionally save to a file
        with open("generated_brews.html", "w") as f:
            f.write(all_brews_html)
        print("Generated HTML saved to generated_brews.html")
    
    # Or generate HTML for a specific brew
    # specific_brew_html = generate_brew_html("kama-citra")
    # if specific_brew_html:
    #     print("\nHTML for Kama Citra:")
    #     print(specific_brew_html)