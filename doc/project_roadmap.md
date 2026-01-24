# 🛣️ Project Roadmap: Universal Finance Tracker

This roadmap details the engineering journey of building a standardized financial analytics tool from scratch.

### 🏁 Phase 1: Problem Definition & Requirement Analysis
* **The Problem**: Bank statements come in inconsistent formats (PDF, CSV, Excel) with varying header names like "Withdrawal," "Amount," or "Debit".
* **The Goal**: Create a "Universal Parser" that identifies financial data regardless of the source bank.
* **UI Choice**: Selected **Streamlit** for its ability to create interactive data applications with minimal frontend overhead.

### 🛠️ Phase 2: Data Engineering (The "Silver" Layer)
* **Standardization Logic**: Developed a fuzzy-matching header system. If a column contains keywords like 'txn' or 'day', it is automatically renamed to 'date'.
* **Data Cleaning**: 
    * Implemented **Regular Expressions (Regex)** to strip currency symbols (₹, $) and commas to prevent math errors.
    * Filtered out credit transactions to focus purely on expenditure analysis.
* **Date Normalization**: Used `pd.to_datetime` with `errors='coerce'` to handle different date formats (DD-MM-YY vs MM-DD-YYYY).



### 📊 Phase 3: Analytics & Visualization (The "Gold" Layer)
* **Visual Strategy**: Chose **Plotly Express** to allow users to hover over data points for exact transaction details.
* **Monthly Budgeting**: Built a conditional logic system. If monthly spending > user-defined limit, the bar turns **Crimson Red**; otherwise, it remains **Emerald Green**.
* **Performance Optimization**: Used `st.session_state` and "Key-Counter" logic to allow the search filter to be reset without refreshing the entire dataset or crashing the app.

### 📄 Phase 4: Executive Reporting Engine
* **PDF Generation**: Integrated `fpdf2` to create a multi-page static report.
* **Chart Rendering**: Solved the "interactive-to-static" problem by using `kaleido` and `tempfile` to capture Plotly charts as high-resolution PNGs for the PDF.
* **Data Audit**: Added a "Top 10" ledger table in the PDF to provide an immediate audit trail for high-value expenses.

### 🚀 Phase 5: Deployment & Security
* **Security**: Created a `.gitignore` to ensure no private `.pdf` or `.xlsx` statements were ever uploaded to the public GitHub repo.
* **Cloud Hosting**: Deployed via **Streamlit Community Cloud**, connecting the GitHub repository to a live web server for public access.
