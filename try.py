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
lookup_table = {
    "First Name": "PERSONAL INFORMATION->Name->First Name :",
    "Last Name": "PERSONAL INFORMATION->Name->Last Name :",
    "Date of Birth": "PERSONAL INFORMATION->Demographics->Birth Date :",
    "Social Security Number": "PERSONAL INFORMATION->Personal Identification Numbers->Social Security Number :",
    "Gender Identity": "PERSONAL INFORMATION->Demographics->Gender Identity:",
    "Primary E-mail Address": "PERSONAL INFORMATION->Primary Method of Contact->Primary E-mail Address :",
    "Personal E-mail Address": "PERSONAL INFORMATION->Primary Method of Contact->Personal E-Mail Address :",
    "Personal Cell Phone": "PERSONAL INFORMATION->Phone Numbers->Personal Cell Phone :",
    "Race/Ethnicity": "PERSONAL INFORMATION->Demographics->Race/Ethnicity :",
    "Are you a US Citizen": "PERSONAL INFORMATION->Demographics->Are you a US Citizen :",
    "Home Address Street": "PERSONAL INFORMATION->Home Address->Street 1 :",
    "Home Address City": "PERSONAL INFORMATION->Home Address->City :",
    "Home Address State": "PERSONAL INFORMATION->Home Address->State :",
    "Home Address Zip Code": "PERSONAL INFORMATION->Home Address->Zip Code :",
    "UPIN": "PERSONAL INFORMATION->Personal Identification Numbers->UPIN :",
    "Individual NPI": "PERSONAL INFORMATION->Personal Identification Numbers->Individual NPI :",
    "License State": "PROFESSIONAL IDENTIFICATION NUMBERS->Professional License->0->License State :",
    "License Number": "PROFESSIONAL IDENTIFICATION NUMBERS->Professional License->0->License Number :",
    "License Type": "PROFESSIONAL IDENTIFICATION NUMBERS->Professional License->0->License Type :",
    "License Status": "PROFESSIONAL IDENTIFICATION NUMBERS->Professional License->0->License Status :",
    "License Issue Date": "PROFESSIONAL IDENTIFICATION NUMBERS->Professional License->0->Issue Date :",
    "License Expiration Date": "PROFESSIONAL IDENTIFICATION NUMBERS->Professional License->0->Expiration Date :",
    "DEA Number": "PROFESSIONAL IDENTIFICATION NUMBERS->DEA Registration->DEA Number :",
    "DEA State": "PROFESSIONAL IDENTIFICATION NUMBERS->DEA Registration->DEA State :",
    "DEA Issue Date": "PROFESSIONAL IDENTIFICATION NUMBERS->DEA Registration->Issue Date :",
    "DEA Expiration Date": "PROFESSIONAL IDENTIFICATION NUMBERS->DEA Registration->Expiration Date :",
    "Medicaid Number": "PROFESSIONAL IDENTIFICATION NUMBERS->Medicaid->Medicaid Number :",
    "Medicaid State": "PROFESSIONAL IDENTIFICATION NUMBERS->Medicaid->State :",
    "Professional School": "EDUCATION->Professional School Information->0->Professional School :",
    "Professional School Street": "EDUCATION->Professional School Information->0->Street 1 :",
    "Professional School City": "EDUCATION->Professional School Information->0->City :",
    "Professional School State": "EDUCATION->Professional School Information->0->State :",
    "Professional School Zip Code": "EDUCATION->Professional School Information->0->Zip Code :",
    "Professional School Degree": "EDUCATION->Professional School Information->0->Degree :",
    "Professional School Start Date": "EDUCATION->Professional School Information->0->Professional School Start Date :",
    "Professional School End Date": "EDUCATION->Professional School Information->0->Professional School End Date :",
    "Professional School Graduation Date": "EDUCATION->Professional School Information->0->Graduation Date :",
    "Undergraduate School": "EDUCATION->Undergraduate Education->School :",
    "Undergraduate State": "EDUCATION->Undergraduate Education->State :",
    "Undergraduate Zip Code": "EDUCATION->Undergraduate Education->Zip Code :",
    "Undergraduate Degree": "EDUCATION->Undergraduate Education->Degree :",
    "Undergraduate Start Date": "EDUCATION->Undergraduate Education->Start Date :",
    "Undergraduate End Date": "EDUCATION->Undergraduate Education->End Date :",
    "Undergraduate Major": "EDUCATION->Undergraduate Education->Area of Training / Course of Study / Major :",
    "Undergraduate Graduation Date": "EDUCATION->Undergraduate Education->Graduation Date :",
    "Internship Institution": "TRAINING INFORMATION->Internship :->0->Institution/Hospital Name :",
    "Internship Street": "TRAINING INFORMATION->Internship :->0->Street1 :",
    "Internship City": "TRAINING INFORMATION->Internship :->0->City :",
    "Internship State": "TRAINING INFORMATION->Internship :->0->State :",
    "Internship Zip Code": "TRAINING INFORMATION->Internship :->0->Zip Code :",
    "Internship Department": "TRAINING INFORMATION->Internship :->0->Department :",
    "Internship Specialty": "TRAINING INFORMATION->Internship :->0->Specialty :",
    "Internship Start Date": "TRAINING INFORMATION->Internship :->0->Start Date :",
    "Internship End Date": "TRAINING INFORMATION->Internship :->0->End Date :",
    "Residency Institution": "TRAINING INFORMATION->Residency :->0->Institution/Hospital Name :",
    "Residency Street": "TRAINING INFORMATION->Residency :->0->Street1 :",
    "Residency City": "TRAINING INFORMATION->Residency :->0->City :",
    "Residency State": "TRAINING INFORMATION->Residency :->0->State :",
    "Residency Zip Code": "TRAINING INFORMATION->Residency :->0->Zip Code :",
    "Residency Department": "TRAINING INFORMATION->Residency :->0->Department :",
    "Residency Specialty": "TRAINING INFORMATION->Residency :->0->Specialty :",
    "Residency Start Date": "TRAINING INFORMATION->Residency :->0->Start Date :",
    "Residency End Date": "TRAINING INFORMATION->Residency :->0->End Date :",
    "Primary Specialty": "SPECIALTY INFORMATION->Primary Specialty->Primary Specialty :",
    "Board Certified": "SPECIALTY INFORMATION->Primary Specialty->Board Certified?",
    "Certifying Board": "SPECIALTY INFORMATION->Primary Specialty->Name of Certifying Board :",
    "Certification Number": "SPECIALTY INFORMATION->Primary Specialty->Certification Number :",
    "Initial Certification Date": "SPECIALTY INFORMATION->Primary Specialty->Initial Certification Date :",
    "Practice Name": "PRACTICE LOCATIONS->Active Locations->0->General Information :->Practice Name :",
    "Practice Street": "PRACTICE LOCATIONS->Active Locations->0->General Information :->Street 1 :",
    "Practice City": "PRACTICE LOCATIONS->Active Locations->0->General Information :->City :",
    "Practice State": "PRACTICE LOCATIONS->Active Locations->0->General Information :->State :",
    "Practice Zip Code": "PRACTICE LOCATIONS->Active Locations->0->General Information :->Zip Code :",
    "Practice Phone Number": "PRACTICE LOCATIONS->Active Locations->0->Phone Numbers :->Appointment Phone Number :",
    "Practice Fax Number": "PRACTICE LOCATIONS->Active Locations->0->Phone Numbers :->Fax Number :",
    "Office Manager Name": "PRACTICE LOCATIONS->Active Locations->0->Office Manager or Business Staff Contact :->First Name :",
    "Office Manager Email": "PRACTICE LOCATIONS->Active Locations->0->Office Manager or Business Staff Contact :->E-mail Address :",
    "Billing Contact Name": "PRACTICE LOCATIONS->Active Locations->0->Billing Contact :->First Name :",
    "Billing Contact Email": "PRACTICE LOCATIONS->Active Locations->0->Billing Contact :->E-mail Address :",
    "Office Hours Monday": "PRACTICE LOCATIONS->Active Locations->0->Monday->Start Time :",
    "Office Hours Tuesday": "PRACTICE LOCATIONS->Active Locations->0->Tuesday->Start Time :",
    "Office Hours Wednesday": "PRACTICE LOCATIONS->Active Locations->0->Wednesday->Start Time :",
    "Office Hours Thursday": "PRACTICE LOCATIONS->Active Locations->0->Thursday->Start Time :",
    "Office Hours Friday": "PRACTICE LOCATIONS->Active Locations->0->Friday->Start Time :",
    "Office Hours Saturday": "PRACTICE LOCATIONS->Active Locations->0->Saturday->Start Time :",
    "Accepting New Patients": "PRACTICE LOCATIONS->Active Locations->0->General Information :->Accepting New Patients?",
    "Handicapped Accessible": "PRACTICE LOCATIONS"
}

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
output_pdf = 'filled_form.pdf'

try:
    pdf = PdfReader(template_pdf)
except FileNotFoundError:
    print(f"Error: {template_pdf} file not found.")
    exit()

# Create a PDF writer object to save the filled PDF later
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

                normalized_field = field_name.strip()

                if normalized_field in lookup_table:
                    json_path = lookup_table[normalized_field]
                    value = get_value_from_path(data, json_path)
                    if value is not None:
                        print(f"Filling field '{field_name}' with value '{value}'")
                        if normalized_field == "Gender Identity":
                            if value.lower() == "male":
                                annotation.update(PdfDict(V=PdfName('Yes')))
                            elif value.lower() == "female":
                                annotation.update(PdfDict(V=PdfName('Yes')))
                        else:
                            annotation.update(
                                PdfDict(V=value)
                            )
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
