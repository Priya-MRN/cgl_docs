from pathlib import Path
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / 'Static-GK'
OUT_DIR.mkdir(exist_ok=True)

states = [
    ("Andhra Pradesh", "South", "Kuchipudi; Vilasini Natyam", "Classical and temple-linked traditions"),
    ("Arunachal Pradesh", "Northeast", "Bardo Chham; Aji Lamu", "Tribal and mask-based dances"),
    ("Assam", "Northeast", "Bihu; Sattriya; Bagurumba", "Classical and harvest celebration dances"),
    ("Bihar", "East", "Jat-Jatin; Bidesia", "Folk and regional performance traditions"),
    ("Chhattisgarh", "Central", "Panthi; Raut Nacha", "Tribal and ritual dance forms"),
    ("Goa", "West", "Fugdi; Dhalo; Dekhni", "Folk and community dances"),
    ("Gujarat", "West", "Garba; Dandiya; Tippani", "Festival dance and cultural identity"),
    ("Haryana", "North", "Khoria; Jhumar", "Rural and folk dance forms"),
    ("Himachal Pradesh", "North", "Nati; Dangi", "Mountain-region folk dances"),
    ("Jharkhand", "East", "Chhau; Jhumar", "Tribal and masked theatrical dances"),
    ("Karnataka", "South", "Yakshagana; Dollu Kunitha", "Classical and folk dance traditions"),
    ("Kerala", "South", "Kathakali; Mohiniyattam; Theyyam", "Temple and classical dance heritage"),
    ("Madhya Pradesh", "Central", "Tertali; Gaur Maria dance", "Tribal and folk traditions"),
    ("Maharashtra", "West", "Lavani; Tamasha", "Popular folk and stage performance"),
    ("Manipur", "Northeast", "Manipuri; Ras Lila", "Classical and devotional dance"),
    ("Meghalaya", "Northeast", "Nongkrem; bamboo dance", "Festival and community dances"),
    ("Mizoram", "Northeast", "Cheraw; bamboo dance", "Traditional bamboo dance"),
    ("Nagaland", "Northeast", "War dance; tribal dances", "Ceremonial and cultural performances"),
    ("Odisha", "East", "Odissi; Chhau; Ghumura", "Classical and martial dance forms"),
    ("Punjab", "North", "Bhangra; Gidda", "Harvest and festive dance forms"),
    ("Rajasthan", "West", "Ghoomar; Kalbelia; Bhavai", "Folk and desert-region dances"),
    ("Sikkim", "Northeast", "Chaam; Yak dance", "Buddhist and ritual traditions"),
    ("Tamil Nadu", "South", "Bharatanatyam; Karagattam", "Classical and temple-based forms"),
    ("Telangana", "South", "Perini Shivatandavam; Burrakatha", "Classical and folk traditions"),
    ("Tripura", "Northeast", "Hojagiri; Garia", "Traditional community dances"),
    ("Uttar Pradesh", "North", "Kathak; Raslila; Ramlila", "Classical and devotional arts"),
    ("Uttarakhand", "North", "Garhwali folk dance; Langvir Nritya", "Mountain folk forms"),
    ("West Bengal", "East", "Rabindra Nritya; Chhau", "Classical, folk, and theatre-based arts"),
    ("Andaman and Nicobar Islands", "Islands", "Nicobarese dances", "Coastal community culture"),
    ("Chandigarh", "North", "Urban cultural performances", "Regional cultural events"),
    ("Dadra and Nagar Haveli and Daman and Diu", "West", "Local folk performances", "Coastal and tribal traditions"),
    ("Delhi", "North", "Kathak; contemporary dance", "Capital cultural hub"),
    ("Jammu and Kashmir", "North", "Rouf; Dumhal; Bhand Pather", "Kashmiri folk and ritual forms"),
    ("Ladakh", "North", "Mask dances; Buddhist ritual dances", "Monastic and cultural traditions"),
    ("Lakshadweep", "Islands", "Island dance forms", "Coastal cultural traditions"),
    ("Puducherry", "South", "Bharatanatyam; folk performances", "French-influenced cultural space"),
]

# Master dataset rows
master_rows = [
    {
        'State_UT': state,
        'Region': region,
        'Representative_Dances': dances,
        'SSC_Significance': note,
        'Category': 'Starter dataset',
        'Exam_One_Liner': f'{state} is known for {dances.split(";")[0]}.'
    }
    for state, region, dances, note in states
]

# Create workbook
wb = Workbook()
ws = wb.active
ws.title = 'Master Database'
headers = ['State_UT', 'Region', 'Representative_Dances', 'Category', 'SSC_Significance', 'Exam_One_Liner']
ws.append(headers)
for row in master_rows:
    ws.append([row['State_UT'], row['Region'], row['Representative_Dances'], row['Category'], row['SSC_Significance'], row['Exam_One_Liner']])

# Style header
header_fill = PatternFill('solid', fgColor='1f4e78')
header_font = Font(bold=True, color='FFFFFF')
thin = Side(border_style='thin', color='D9D9D9')
border = Border(left=thin, right=thin, top=thin, bottom=thin)
for cell in ws[1]:
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = border

# Auto-size columns
for col in ws.columns:
    max_len = max(len(str(cell.value)) for cell in col if cell.value is not None)
    ws.column_dimensions[get_column_letter(col[0].column)].width = min(max_len + 2, 35)

# Additional sheets
sheet_specs = {
    'State-wise Summary': [['State_UT', 'Region', 'Representative_Dances', 'SSC_Significance']],
    'Classical Dances': [['State_UT', 'Dance', 'Category']],
    'Folk Dances': [['State_UT', 'Dance', 'Category']],
    'Tribal Dances': [['State_UT', 'Dance', 'Category']],
    'Important Dancers': [['State_UT', 'Dancer', 'Note']],
    'UNESCO Heritage': [['State_UT', 'Heritage_Item', 'Note']],
    'Recent Current Affairs': [['Year', 'Topic', 'Note']],
    'SSC One-Liners': [['State_UT', 'One_Liner']],
    'MCQ Practice': [['Question', 'Answer']],
    'Revision Tables': [['State_UT', 'Dance_Form', 'Category']],
}

for sheet_name, rows in sheet_specs.items():
    ws2 = wb.create_sheet(title=sheet_name)
    for row in rows:
        ws2.append(row)
    for cell in ws2[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border

# Fill sample rows
for sheet_name, rows in {
    'Classical Dances': [('Andhra Pradesh', 'Kuchipudi', 'Classical'), ('Tamil Nadu', 'Bharatanatyam', 'Classical'), ('Odisha', 'Odissi', 'Classical'), ('Manipur', 'Manipuri', 'Classical')],
    'Folk Dances': [('Gujarat', 'Garba', 'Folk'), ('Punjab', 'Bhangra', 'Folk'), ('Rajasthan', 'Ghoomar', 'Folk'), ('Maharashtra', 'Lavani', 'Folk')],
    'Tribal Dances': [('Chhattisgarh', 'Raut Nacha', 'Tribal'), ('Jharkhand', 'Chhau', 'Tribal'), ('Nagaland', 'War dance', 'Tribal'), ('Arunachal Pradesh', 'Bardo Chham', 'Tribal')],
    'Important Dancers': [('Tamil Nadu', 'Padma Subrahmanyam', 'Renowned Bharatanatyam exponent'), ('Odisha', 'Sonal Mansingh', 'Prominent classical dancer'), ('Manipur', 'Bharati Shivaji', 'Noted dance scholar')],
    'UNESCO Heritage': [('India', 'Kutiyattam', 'UNESCO Intangible Cultural Heritage'), ('India', 'Ramlila', 'UNESCO Intangible Cultural Heritage')],
    'Recent Current Affairs': [('2025', 'National festivals and dance performances', 'Use for recent updates'), ('2026', 'Padma and Akademi awards', 'Use for recent updates')],
    'SSC One-Liners': [('Tamil Nadu', 'Bharatanatyam is one of the major classical dances of India.'), ('Gujarat', 'Garba is a major festival dance associated with Navratri.')],
    'MCQ Practice': [('Which state is associated with Garba?', 'Gujarat'), ('Which dance is linked to Odissi?', 'Odisha')],
    'Revision Tables': [('Odisha', 'Odissi', 'Classical'), ('Punjab', 'Bhangra', 'Folk')],
}.items():
    ws2 = wb[sheet_name]
    for row in rows:
        ws2.append(row)

# State-wise summary rows
ws_state = wb['State-wise Summary']
for item in master_rows:
    ws_state.append([item['State_UT'], item['Region'], item['Representative_Dances'], item['SSC_Significance']])

# Save workbook
xlsx_path = OUT_DIR / 'India-State-wise-Dance-Encyclopedia.xlsx'
wb.save(xlsx_path)

# Write CSV files
csv_specs = {
    'master_database.csv': master_rows,
    'dancers.csv': [
        {'State_UT': 'Tamil Nadu', 'Dancer': 'Padma Subrahmanyam', 'Note': 'Renowned Bharatanatyam exponent'},
        {'State_UT': 'Odisha', 'Dancer': 'Sonal Mansingh', 'Note': 'Prominent classical dancer'},
    ],
    'current_affairs.csv': [
        {'Year': '2025', 'Topic': 'National festivals and dance performances', 'Note': 'Recent updates'},
        {'Year': '2026', 'Topic': 'Padma and Akademi awards', 'Note': 'Recent updates'},
    ],
    'state_summary.csv': [
        {'State_UT': item['State_UT'], 'Region': item['Region'], 'Representative_Dances': item['Representative_Dances'], 'SSC_Significance': item['SSC_Significance']}
        for item in master_rows
    ],
}

for filename, rows in csv_specs.items():
    out_path = OUT_DIR / filename
    with out_path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)

print(f'Created workbook: {xlsx_path}')
for path in OUT_DIR.glob('*.csv'):
    print(f'Created csv: {path}')
