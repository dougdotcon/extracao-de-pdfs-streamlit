# PDF Data Extractor

A robust Streamlit application designed to streamline the extraction and processing of data from PDF files of various formats. The tool converts unstructured or semi-structured data into organized Excel spreadsheets, utilizing either Optical Character Recognition (OCR) for scanned documents or direct table extraction for structured files.

## 📋 Features

- **Multi-Model Processing:**
  - **Models 1, 3, and 4 (OCR):** Converts PDFs to images, extracts text using Tesseract OCR, and applies regex patterns to structure the data. Suitable for scanned documents.
  - **Model 2 (Tabula):** Directly extracts tables from PDFs using the Tabula library. Performs data cleaning and consolidation before generating the final Excel file.

- **User-Friendly Interface:**
  - Simple file upload via the Streamlit dashboard.
  - Interactive buttons for processing and downloading the generated reports.

## 📂 Project Structure

bash
/pdf_data_extractor
├── app.py                  # Main Streamlit application code
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
├── uploads/                # Temporary storage for uploaded PDFs
├── outputs/                # Generated Excel (.xlsx) files
└── extracted_texts/        # Raw text files extracted via OCR


## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system (required for Models 1, 3, and 4).

### Installation
1. **Clone the repository:**
   bash
   git clone https://github.com/your-username/pdf_data_extractor.git
   cd pdf_data_extractor
   

2. **Install Python dependencies:**
   bash
   pip install -r requirements.txt
   

### Running the Application

Start the Streamlit server:
bash
streamlit run app.py


Navigate to the local URL provided in your terminal to use the application.

## 🛠️ Technology Stack

- **Streamlit:** For rapid web application development and UI.
- **Pytesseract & pdf2image:** For OCR processing of scanned PDFs.
- **Tabula-py:** For extracting tables from structured PDFs.
- **Pandas:** For data manipulation and cleaning.
- **OpenPyXL:** For writing Excel files.

## 📦 Dependencies

Ensure all required packages are installed:

bash
streamlit
pytesseract
pandas
tabula-py
openpyxl
Pillow
pdf2image


## ⚠️ Important Notes

- **Tesseract Installation:** The application relies on the Tesseract binary being installed and accessible via the system PATH. Ensure it is correctly installed on your OS.
- **Tabula Java Dependency:** Tabula requires a Java Runtime Environment (JRE) to function. Ensure Java is installed.
- **File Handling:** The `uploads` and `outputs` directories are used for temporary storage. Ensure the application has write permissions for these folders.