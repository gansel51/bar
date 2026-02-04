import json
from textwrap import dedent

from utils import format_json_file, load_json_file

def generate_spirits_html():
    """
    Generate HTML for spirits from spirits.json
    
    Returns:
        String with HTML for the spirits section
    """
    # Load spirits.json
    json_path = "docs/assets/spirits.json"

    spirits = load_json_file(json_path)
    if spirits is None:
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
