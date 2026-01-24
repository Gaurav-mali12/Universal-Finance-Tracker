# Universal Finance Tracker 🛡️

A professional-grade personal finance dashboard built with **Python** and **Streamlit**. This application serves as a "Universal Parser" that transforms messy, non-standard bank statements (PDF, Excel, CSV) into actionable visual analytics and executive reports.

[🚀 Live Demo](https://gaurav-finance-tracker.streamlit.app)

## 📖 Project Overview
Financial data often comes in unstructured or varied formats depending on the bank. This project solves that problem by implementing a standardized data pipeline to:
- **Ingest**: Read raw files regardless of their header names.
- **Clean**: Strip currency symbols, fix dates, and handle missing values.
- **Analyze**: Provide monthly trends and category breakdowns.
- **Report**: Export professional 2-page PDF summaries.

## 🚀 Key Features
- **Dynamic Search**: Instant transaction filtering with a dedicated "Reset" logic.
- **Smart Budgeting**: Visual indicators (Red/Green) that track monthly spending against user-defined limits.
- **Executive PDF Export**: High-resolution reporting with embedded charts and audit tables.
- **Privacy-Centric**: Data is processed locally in memory; no financial records are stored on the server.

## 🛠️ Tech Stack
- **Frontend/Hosting**: Streamlit
- **Data Analysis**: Pandas, NumPy
- **Visualizations**: Plotly Express
- **File Parsing**: pdfplumber, OpenPyXL
- **PDF Engine**: FPDF2, Kaleido

## 📦 Installation & Local Usage

## 📚 Documentation
For a deeper dive into how this project was built and how to set it up, please refer to our detailed guides:
- [**Installation Guide**](docs/installation.md): Full list of libraries and environment setup.
- [**Project Roadmap**](docs/project_roadmap.md): Detailed explanation of the logic and development phases.
  
1. **Clone the repo**:
   ```bash
   git clone [https://github.com/Gaurav-mali12/Universal-Finance-Tracker.git](https://github.com/Gaurav-mali12/Universal-Finance-Tracker.git)
## Install requirements: 
 **Run In Terminal**:
 pip install -r requirements.txt

## Run Dashbord :
**Run In Terminal**:-streamlit run app.py

## 📄 License
**-This project is licensed under the MIT License - see the LICENSE file for details.**


## 📁 Repository Structure
```text
Universal-Finance-Tracker/
│
├── docs/               # Detailed Project Documentation
│   ├── installation.md # Step-by-step environment setup
│   └── project_roadmap.md # Technical journey and methodology
│
├── app.py              # Main Application Logic & UI
├── requirements.txt    # Library Dependencies for Deployment
├── .gitignore          # Security: Prevents private data from being uploaded
├── LICENSE             # MIT License
└── README.md           # Project Overview & Quick Start


