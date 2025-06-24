import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import re
from pdfminer.high_level import extract_text


def parse_pdf(filepath):
    print("parse_pdf() called with:", filepath)

    try:
        
        text = extract_text(filepath) # extract text
        data = get_financial_data(text) # extract data 
        return create_chart(data)
    
    except Exception as e:
        print(f"Error!: {e}")
        raise


def get_financial_data(text):
    category_expenses = {}
    lines = text.split('\n')

    for line in lines:
        line = line.strip()

        if not line:
            continue
        
        category = None

        if 'Merchandise' in line:
            category = 'Shopping'
        elif 'Gasoline' in line:  
            category = 'Gas'
        elif 'Restaurants' in line:   
            category = 'Restaurants'
        elif 'Supermarkets' in line:      
            category = 'Groceries'
        elif 'Services' in line:
            category = 'Services'
        elif 'Medical' in line:
            category = 'Medical'
      
        if category:
            get_amount = re.findall(r'(\d+\.\d{2})', line)
            if get_amount:
                try:
                    amount = float(get_amount[-1])
                    if amount > 0.01:
                        category_expenses[category] = category_expenses.get(category, 0) + amount
                except ValueError:
                    continue
    return category_expenses

    

def create_chart(financial_data):
    try:
        if not os.path.exists('static'):
            os.makedirs('static')
        
        plt.figure(figsize=(6, 6))
    
        if not financial_data:
            plt.text(0.5, 0.5, 'No data found', ha='center', va='center')
            plt.axis('off')
        else:
            categories = list(financial_data.keys())
            amounts = list(financial_data.values())

            plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
            plt.title('Expense Distribution')

        output_path = 'static/pie_chart.png'
        print("Saving chart to:", output_path)

        plt.savefig(output_path)
        plt.close()
        print("Chart saved successfully.")

        return {
        "chart_url": "/static/pie_chart.png"
            }

    except Exception as e:
        print(f"Error:", e)
        raise