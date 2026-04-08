# PDF Financial Statement Parser (Web App Backend)

A backend application built with Flask that parses PDF financial statements using OCR (Tesseract) and generates visualizations and structured data for financial analysis.

**Role:** Served as Backend Developer, contributing initial PDF parsing logic, analyzing raw data extraction, and assisting in transitioning to an OCR-based parser.

---

## 🚀 Features

- OCR-based PDF parsing using `pytesseract` and `pdfplumber`  
- Categorizes expenses into predefined merchant categories  
- Generates pie charts, circle packing JSON, and Sankey chart JSON for visualization  
- RESTful API endpoints for file upload, data processing, and savings goal calculations  
- Cross-Origin support with `Flask-CORS` for frontend integration  

---

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/pdf-parser-backend.git
cd pdf-parser-backend
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Setup static and upload folders**

```bash
mkdir uploads static
```

4. **Run Server**

```bash
python app.py

- The backend runs at http://127.0.0.1:5000/ by default.
```
---

## 🛠️ Technologies Used
- Python
- Flask, Flask-CORS
- pdfplumber, pytesseract
- pdfplumber, pytesseract
- PIL (Pillow)

## My Contributions
- Developed initial PDF parsing functionality using pdfplumber  
- Analyzed and handled unstructured PDF data, identifying extraction limitations  
- Assisted with transition to OCR-based parsing using Tesseract for higher accuracy  
- Collaborated in team discussions and maintained project documentation  






