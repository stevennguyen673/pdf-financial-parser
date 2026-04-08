import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import pdfplumber
from collections import defaultdict
import re
from PIL import Image
import pytesseract
import sys

# If you installed Tesseract in a different location, update the path below.
if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Define the list of known merchant categories from expense statement
KNOWN_MERCHANT_CATEGORIES = [
    "Merchandise",
    "Restaurants",
    "Supermarkets",
    "Internet",
    "Entertainment",
    "Gasoline",
    "Services",
    "Medical Services"
]

def parse_pdf(filepath):
    """
    Parses a PDF using OCR and groups expenses by a comprehensive list of merchant categories.
    """
    print(f"--- Starting OCR Parse for {filepath} ---")
    categories = defaultdict(float)
    other_charges = []  # List to store transactions categorized as "Other"

    try:
        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"Processing Page {page_num} with OCR...")
                image = page.to_image(resolution=300).original
                text = pytesseract.image_to_string(image, lang='eng')

                transaction_pattern = re.compile(r'(.+?)\s+\$?([\d,]+\.\d{2})(?!\s*\d)', re.MULTILINE)
                in_transactions_section = False
                
                for line in text.split('\n'):
                    if 'MERCHANT CATEGORY' in line and 'AMOUNT' in line:
                        in_transactions_section = True
                        print("Found transaction header, starting capture.")
                        continue
                    if 'Total Purchases' in line or 'PAYMENTS AND CREDITS' in line:
                        in_transactions_section = False
                        print("Found transaction footer, ending capture.")
                        continue

                    if in_transactions_section:
                        match = transaction_pattern.search(line)
                        if match:
                            description = match.group(1).strip()
                            amount_str = match.group(2)
                            amount = float(amount_str.replace(',', ''))
                            
                            assigned_category = "Other"
                            for cat in KNOWN_MERCHANT_CATEGORIES:
                                if re.search(r'\b' + re.escape(cat) + r'\b', description, re.IGNORECASE):
                                    assigned_category = cat
                                    break
                            
                            # If the transaction is categorized as "Other", add it to our list
                            if assigned_category == "Other":
                                other_charges.append({'description': description, 'amount': amount})
                            
                            categories[assigned_category] += amount

    except Exception as e:
        print(f"An unexpected error occurred during OCR processing: {e}")
        raise

    if not categories:
        raise ValueError("Could not extract any transactions using OCR. The PDF format may be unusual.")

    print(f"--- OCR Parsing Complete. Categories: {dict(categories)} ---")
    
    if other_charges:
        print("\n--- Transactions Categorized as 'Other' ---")
        for charge in other_charges:
            print(f"  - Amount: ${charge['amount']:.2f}, Description: {charge['description']}")
        print("-------------------------------------------\n")
    else:
        print("\n--- No transactions were categorized as 'Other'. ---\n")
        
    # --- Chart Generation ---
    if "Other" in categories:
        del categories["Other"]
    labels = list(categories.keys())
    values = list(categories.values())

    # Prepare hierarchical data for circle packing
    children = [{"name": label, "value": value} for label, value in categories.items()]
    circle_packing_data = {"name": "Expenses", "children": children}

    # --- Sankey Data Generation ---
    # Node 0: "Total Expenses", then one node per category
    sankey_nodes = [{"name": "Total Expenses"}] + [{"name": label} for label in categories.keys()]
    sankey_links = [
        {"source": 0, "target": i + 1, "value": value}
        for i, value in enumerate(categories.values())
    ]

    plt.figure(figsize=(10, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Merchant Category')
    plt.axis('equal')

    static_dir = os.path.join(os.getcwd(), 'static')
    os.makedirs(static_dir, exist_ok=True)
    chart_path = os.path.join(static_dir, 'pie_chart.png')
    plt.savefig(chart_path)
    plt.close()

    return {
        "chart_url": "/static/pie_chart.png",
        "circle_packing_data": circle_packing_data,
        "sankey_data": {
            "nodes": sankey_nodes,
            "links": sankey_links
        }
    }
