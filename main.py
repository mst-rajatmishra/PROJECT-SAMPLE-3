import json
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName

# Load JSON data from a file
try:
    with open('data.json') as data_file:
        data = json.load(data_file)
except FileNotFoundError:
    print("Error: data.json file not found.")
    exit()
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from data.json.")
    exit()

# Load the lookup table that maps PDF fields to JSON paths
try:
    with open('look2.json') as lookup_file:
        lookup_table = json.load(lookup_file)
except FileNotFoundError:
    print("Error: lookup_table.json file not found.")
    exit()
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from lookup_table.json.")
    exit()

# Function to extract a value from the nested JSON data using a path
def get_value_from_path(data, path):
    keys = path.split('->')
    value = data
    for key in keys:
        key = key.strip()
        if isinstance(value, list):
            try:
                index = int(key)
                value = value[index]
            except (ValueError, IndexError):
                return None
        else:
            value = value.get(key)
        if value is None:
            return None
    return value

# Load the PDF template that will be filled with data
template_pdf = 'form_App Application 2024.pdf'
output_pdf = 'Output.pdf'

try:
    pdf = PdfReader(template_pdf)
except FileNotFoundError:
    print(f"Error: {template_pdf} file not found.")
    exit()
    
# Create a PDF writer object to save the filled PDF lat'er
writer = PdfWriter()

# Iterate through each page in the PDF
for page in pdf.pages:
    annotations = page.get('/Annots')
    if annotations:
        for annotation in annotations:
            field = annotation.get('/T')
            if field:
                field_name = field[1:-1].strip()
                print(f"Found field in PDF: '{field_name}'")

                # Normalize the field name for comparison (optional)
                normalized_field = field_name.strip()

                # Check if the field name exists in the lookup table
                if normalized_field in lookup_table:
                    json_path = lookup_table[normalized_field]
                    if "==" in json_path:
                        # Handle checkboxes
                        condition, value_to_set = json_path.split("==")
                        condition = condition.strip()
                        value_to_set = value_to_set.strip().strip("'")
                        actual_value = get_value_from_path(data, condition)
                        if actual_value == value_to_set:
                            print(f"Checking checkbox '{field_name}'")
                            annotation.update(PdfDict(AS=PdfName('Yes')))
                    else: 
                        # Handle regular fields
                        value = get_value_from_path(data, json_path)
                        if value is not None:
                            print(f"Filling field '{field_name}' with value '{value}'")
                            annotation.update(PdfDict(V=value))
                        else:
                            print(f"No value found for field '{field_name}' in JSON data")
                else:
                    print(f"Field '{field_name}' not found in lookup table")

    writer.addpage(page)

# Save the filled PDF to a new file
try:
    writer.write(output_pdf)
    print(f"PDF form filled and saved as {output_pdf}")
except Exception as e:
    print(f"Error saving filled PDF: {e}")
