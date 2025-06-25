import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import pdfplumber
from collections import defaultdict
import re
from PIL import Image
import pytesseract
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

KNOWN_MERCHANT_CATEGORIES = [
    "Merchandise", "Restaurants", "Supermarkets", "Internet",
    "Entertainment", "Gasoline", "Services", "Medical Services"
]

def parse_pdf(filepath, income=None, savings_goal=None):
    print(f"--- Starting OCR Parse for {filepath} ---")
    categories = defaultdict(float)
    other_charges = []

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
                        continue
                    if 'Total Purchases' in line or 'PAYMENTS AND CREDITS' in line:
                        in_transactions_section = False
                        continue

                    if in_transactions_section:
                        match = transaction_pattern.search(line)
                        if match:
                            description = match.group(1).strip()
                            amount = float(match.group(2).replace(',', ''))

                            assigned_category = "Other"
                            for cat in KNOWN_MERCHANT_CATEGORIES:
                                if re.search(r'\b' + re.escape(cat) + r'\b', description, re.IGNORECASE):
                                    assigned_category = cat
                                    break

                            if assigned_category == "Other":
                                other_charges.append({'description': description, 'amount': amount})

                            categories[assigned_category] += amount

    except Exception as e:
        print(f"An error occurred during OCR processing: {e}")
        raise

    if not categories:
        raise ValueError("No transactions found using OCR.")

    categories.pop("Other", None)
    labels = list(categories.keys())
    values = list(categories.values())
    df = pd.DataFrame({"Category": labels, "Amount": values})

    static_dir = os.path.join(os.getcwd(), 'static')
    os.makedirs(static_dir, exist_ok=True)

    # PIE
    plt.figure(figsize=(10, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Merchant Category')
    plt.axis('equal')
    pie_path = os.path.join(static_dir, 'pie_chart.png')
    plt.savefig(pie_path)
    plt.close()

    # DONUT
    fig_donut = px.pie(df, names='Category', values='Amount', hole=0.4, title="Spending Donut Chart")
    fig_donut.write_html(os.path.join(static_dir, 'donut.html'))

    # BAR
    fig_bar = px.bar(df, x='Category', y='Amount', title='Category Spending - Bar Chart', color='Category')
    fig_bar.update_traces(marker_line_width=1.5, marker_line_color="black")
    fig_bar.write_html(os.path.join(static_dir, 'bar3d.html'))

    # Circle Packing Data
    circle_data = {
        "name": "Expenses",
        "children": [{"name": label, "value": val} for label, val in categories.items()]
    }
    with open(os.path.join(static_dir, 'circle_data.json'), 'w') as f:
        json.dump(circle_data, f)

    # Sankey Data
    sankey_nodes = [{"name": "Total Expenses"}] + [{"name": label} for label in labels]
    sankey_links = [{"source": 0, "target": i + 1, "value": val} for i, val in enumerate(values)]
    sankey_data = {
        "nodes": sankey_nodes,
        "links": sankey_links
    }
    with open(os.path.join(static_dir, 'sankey_data.json'), 'w') as f:
        json.dump(sankey_data, f)

    return {
        "chart_url": "/static/pie_chart.png",
        "donut_url": "/static/donut.html",
        "bar3d_url": "/static/bar3d.html",
        "circle_json_url": "/static/circle_data.json",
        "sankey_json_url": "/static/sankey_data.json",
        "totalSpending": sum(values)
    }
