"""Shared utility functions for HTML generation scripts."""

import json


def format_json_file(input_file, output_file=None):
    """
    Format a JSON file with proper indentation and structure.

    Args:
        input_file: Path to the input JSON file
        output_file: Path to the output JSON file (defaults to same as input)

    Returns:
        True if successful, False otherwise
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


def load_json_file(json_path):
    """
    Load a JSON file, stripping any JavaScript-style comments.

    Args:
        json_path: Path to the JSON file

    Returns:
        Parsed JSON data as a dict, or None if loading fails
    """
    try:
        with open(json_path, 'r') as f:
            content = f.read()
            lines = content.splitlines()
            cleaned_lines = [line for line in lines if not line.strip().startswith('//')]
            cleaned_content = '\n'.join(cleaned_lines)
            return json.loads(cleaned_content)
    except Exception as e:
        print(f"Error loading {json_path}: {e}")
        return None
