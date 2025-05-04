import json
import os
from textwrap import dedent

def generate_spirits_html():
    """
    Generate HTML for spirits from spirits.json
    
    Returns:
        String with HTML for the spirits section
    """
    # Load spirits.json
    json_path = "docs/assets/spirits.json"

    try:
        with open(json_path, 'r') as f:
            # Remove any potential JavaScript comments
            content = f.read()
            lines = content.splitlines()
            cleaned_lines = [line for line in lines if not line.strip().startswith('//')]
            cleaned_content = '\n'.join(cleaned_lines)
            
            spirits = json.loads(cleaned_content)
    except Exception as e:
        print(f"Error loading spirits.json: {e}")
        return None
    
    # Generate HTML for all spirit types
    html_sections = []
    
    for spirit_type, spirit_data in spirits.items():
        title = spirit_data.get("title", spirit_type.capitalize())
        categories = spirit_data.get("categories", [])
        
        # Start a section for this spirit type
        section_html = f'        <h2>{title}</h2>\n'
        
        # Generate HTML for each category
        for category in categories:
            cat_name = category.get("name", "")
            cat_type = category.get("type", "")
            items = category.get("items", [])
            
            section_html += dedent(f'''
        <div class="beverage-item" data-type="{cat_type}">
          <h3>{cat_name}</h3>
          <ul>
''')
            
            # Generate items list
            for item in items:
                item_name = item.get("name", "")
                item_notes = item.get("notes", "")
                section_html += f'            <li>{item_name} <span class="beverage-notes">{item_notes}</span></li>\n'
            
            section_html += '          </ul>\n        </div>\n'
        
        html_sections.append(section_html)
    
    # Combine all sections
    full_html = '      <section class="spirits-category">\n'
    full_html += '\n'.join(html_sections)
    full_html += '      </section>'
    
    return full_html

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
    format_json_file("docs/assets/spirits.json")
    
    # Generate HTML
    spirits_html = generate_spirits_html()
    if spirits_html:
        print("HTML for spirits generated successfully")
        
        # Save to a file
        with open("generated_spirits.html", "w") as f:
            f.write(spirits_html)
        print("Generated HTML saved to generated_spirits.html")
