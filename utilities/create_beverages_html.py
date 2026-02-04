import json
from textwrap import dedent

from utils import format_json_file, load_json_file

def generate_beverage_html():
    """
    Generate HTML for beverages from beverages.json
    
    Returns:
        String with HTML for the beverage section
    """
    # Load beverages.json
    json_path = "docs/assets/beverages.json"

    beverages = load_json_file(json_path)
    if beverages is None:
        return None
    
    # Generate HTML for all beverage types
    html_sections = []
    
    for beverage_type, beverage_data in beverages.items():
        title = beverage_data.get("title", beverage_type.capitalize())
        categories = beverage_data.get("categories", [])
        
        # Start a section for this beverage type
        section_html = f'        <h2>{title}</h2>\n'
        
        # Generate HTML for each category
        for category in categories:
            cat_name = category.get("name", "")
            cat_type = category.get("type", "")
            items = category.get("items", [])
            custom_html = category.get("custom_html", "")
            
            section_html += dedent(f'''
        <div class="beverage-item" data-type="{cat_type}">
          <h3>{cat_name}</h3>
''')
            
            # Either use custom HTML or generate item list
            if custom_html:
                section_html += f'          {custom_html}\n'
            else:
                section_html += '          <ul>\n'
                for item in items:
                    item_name = item.get("name", "")
                    item_notes = item.get("notes", "")
                    section_html += f'            <li>{item_name} <span class="beverage-notes">{item_notes}</span></li>\n'
                section_html += '          </ul>\n'
            
            section_html += '        </div>\n'
        
        html_sections.append(section_html)
    
    # Combine all sections
    full_html = '      <section class="spirits-category">\n'
    full_html += '\n'.join(html_sections)
    full_html += '      </section>'
    
    return full_html


# Example usage
if __name__ == "__main__":
    # First format the JSON file to ensure it's valid
    format_json_file("docs/assets/beverages.json")
    
    # Generate HTML
    beverages_html = generate_beverage_html()
    if beverages_html:
        print("HTML for beverages generated successfully")
        
        # Save to a file
        with open("generated_beverages.html", "w") as f:
            f.write(beverages_html)
        print("Generated HTML saved to generated_beverages.html")