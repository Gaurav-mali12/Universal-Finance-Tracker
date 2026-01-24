import streamlit as st
import pandas as pd
import pdfplumber
import plotly.express as px
import re
from fpdf import FPDF
import tempfile
import os

# --- 1. CONFIGURATION ---
# We set the page to 'wide' to allow the charts to sit side-by-side comfortably
st.set_page_config(page_title="Universal Finance Tracker", layout="wide")
st.title("Universal Finance Tracker")

# We use a 'reset_count' in session state to handle the search box reset.
# Changing a widget's key name is the safest way to clear it in Streamlit.
if 'reset_count' not in st.session_state:
    st.session_state.reset_count = 0

def clear_search():
    """Increments the count to generate a brand new, empty search widget"""
    st.session_state.reset_count += 1

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("Dashboard Controls")
    # budget_limit is used for the conditional coloring (Red/Green) of bars
    budget_limit = st.number_input("Monthly Budget Limit", value=25000, step=1000)
    
    # The key changes every time 'Reset View' is clicked, clearing the text
    search_query = st.text_input(
        "Search Transactions", 
        key=f"search_{st.session_state.reset_count}"
    )
    st.button("Reset View", on_click=clear_search)

# --- 3. DATA PROCESSING (The Core Logic) ---
def process_file(file):
    """
    This function reads the raw file, finds the headers, and cleans the data
    so it can be used for math and visualization.
    """
    # A. Reading the file based on its extension
    if file.name.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            rows = []
            for page in pdf.pages:
                table = page.extract_table()
                if table: rows.extend(table)
        # Creating the initial DataFrame using the first row as the header
        df = pd.DataFrame(rows[1:], columns=rows[0])
    else:
        df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
    
    # B. Normalizing Headers: Lowercase and stripping spaces avoids 'KeyErrors'
    df.columns = [str(c).lower().strip() for c in df.columns]
    
    # C. Smart Column Mapping: Searches for keywords to find standard columns
    for col in df.columns:
        if any(x in col for x in ['date', 'txn']): df = df.rename(columns={col: 'date'})
        if any(x in col for x in ['amount', 'debit', 'spent']): df = df.rename(columns={col: 'amount'})
        if any(x in col for x in ['desc', 'particular', 'narration']): df = df.rename(columns={col: 'desc'})
    
    # D. Currency Cleaning: Uses 'Regex' to strip symbols like ₹ or commas
    df['amount'] = df['amount'].apply(lambda x: float(re.sub(r'[^\d.]', '', str(x))) if pd.notnull(x) else 0.0)
    
    # E. Refinement: We filter for positive spends and convert strings to Date objects
    df = df[df['amount'] > 0] 
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Dropping rows where the date couldn't be correctly read
    return df.dropna(subset=['date'])

# --- 4. PDF ENGINE (Advanced AI-Assisted Feature) ---
def generate_pdf_report(df_all, df_year, year, hist_pie, pie_fig, bar_fig):
    """
    Transforms dynamic dashboard charts and tables into a 2-page static PDF.
    """
    pdf = FPDF()
    
    # PAGE 1: ALL-TIME HISTORY
    pdf.add_page()
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(200, 15, "Personal Finance: Historical Summary", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Total Lifetime Expenditure: Rs. {df_all['amount'].sum():,.2f}", ln=True)
    
    # Saving Plotly charts as PNGs to embed them in the PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f_hist:
        hist_pie.update_layout(template="plotly_white")
        hist_pie.write_image(f_hist.name, scale=2)
        pdf.image(f_hist.name, x=30, y=50, w=150)
    
    # PAGE 2: ANNUAL PERFORMANCE & DETAILED TABLE
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 15, f"Annual Performance Review: {year}", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Total Annual Expenditure: Rs. {df_year['amount'].sum():,.2f}", ln=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t1, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t2:
        pie_fig.update_layout(template="plotly_white")
        bar_fig.update_layout(template="plotly_white")
        pie_fig.write_image(t1.name, scale=2)
        bar_fig.write_image(t2.name, scale=2)
        pdf.image(t1.name, x=10, y=45, w=90)
        pdf.image(t2.name, x=105, y=45, w=90)

    # Creating the Audit Ledger Table
    pdf.set_y(130)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f"Audit Ledger: Top 10 Transactions ({year})", ln=True)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(35, 10, "Date", 1, 0, 'C', 1)
    pdf.cell(110, 10, "Description", 1, 0, 'C', 1)
    pdf.cell(50, 10, "Amount (Rs.)", 1, 1, 'C', 1)
    
    pdf.set_font("Arial", size=10)
    # Adding the top 10 largest expenses to the table
    for _, row in df_year.nlargest(10, 'amount').iterrows():
        pdf.cell(35, 8, row['date'].strftime('%Y-%m-%d'), 1)
        pdf.cell(110, 8, str(row['desc'])[:50], 1)
        pdf.cell(50, 8, f"{row['amount']:,.2f}", 1, 1, 'R')
    
    # Returns raw bytes for the Streamlit download button
    return bytes(pdf.output())

# --- 5. DASHBOARD LAYOUT ---
uploaded_file = st.file_uploader("Upload Statement", type=['pdf', 'xlsx', 'csv'])

if uploaded_file:
    # Triggering the processing engine
    df = process_file(uploaded_file)
    
    # Adding metadata columns for sorting and grouping
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.strftime('%b')
    df['m_num'] = df['date'].dt.month

    # SECTION: ALL-TIME HISTORY
    st.header(f"Total Expenditure (All-Time): ₹{df['amount'].sum():,.2f}")
    hist_pie = px.pie(df.groupby('desc')['amount'].sum().nlargest(10).reset_index(), 
                      values='amount', names='desc', hole=0.5, title="Lifetime Distribution")
    st.plotly_chart(hist_pie, use_container_width=True)

    st.divider()

    # SECTION: YEARLY ANALYSIS
    years = sorted(df['year'].unique(), reverse=True)
    sel_year = st.selectbox("Select Fiscal Year", years)
    year_df = df[df['year'] == sel_year]
    
    # If a search term exists, filter the yearly dataframe
    if search_query:
        year_df = year_df[year_df['desc'].str.contains(search_query, case=False, na=False)]

    st.subheader(f"Fiscal Summary for {sel_year}: ₹{year_df['amount'].sum():,.2f}")
    c1, c2 = st.columns(2)
    
    # Yearly Pie Chart
    pie_yr = px.pie(year_df.groupby('desc')['amount'].sum().nlargest(10).reset_index(), 
                    values='amount', names='desc', title=f"Top Categories {sel_year}")
    c1.plotly_chart(pie_yr, use_container_width=True)

    # Yearly Bar Chart with conditional colors
    m_data = year_df.groupby(['m_num', 'month'])['amount'].sum().reset_index()
    m_data['color'] = m_data['amount'].apply(lambda x: '#D62728' if x > budget_limit else '#2CA02C')
    bar_yr = px.bar(m_data, x='month', y='amount', title=f"Monthly Trend {sel_year}")
    bar_yr.update_traces(marker_color=m_data['color'])
    c2.plotly_chart(bar_yr, use_container_width=True)

    # SECTION: EXPORT REPORT
    if st.button("Generate Pro PDF Report"):
        # We pass both the total and filtered dataframes for the 2-page report
        pdf_bytes = generate_pdf_report(df, year_df, sel_year, hist_pie, pie_yr, bar_yr)
        st.download_button(
            "Download Full Report", 
            data=pdf_bytes, 
            file_name=f"Finance_Report_{sel_year}.pdf", 
            mime="application/pdf"
        )