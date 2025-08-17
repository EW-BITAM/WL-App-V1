import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd

# Authenticate and connect to Google Sheets
def connect_to_gsheet(creds_json, spreadsheet_name, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", 
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", 
             "https://www.googleapis.com/auth/drive"]
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open(spreadsheet_name)  
    return spreadsheet.worksheet(sheet_name)  # Access specific sheet by name

# Google Sheet credentials and details
SPREADSHEET_NAME = 'Streamlit'
SHEET_NAME = 'Sheet1'
CREDENTIALS_FILE = './credentials.json'

# Connect to the Google Sheet
sheet_by_name = connect_to_gsheet(CREDENTIALS_FILE, SPREADSHEET_NAME, sheet_name=SHEET_NAME)

st.title("Wireline Daily Operation Report")

# Read Data from Google Sheets
def read_data():
    data = sheet_by_name.get_all_records()  # Get all records from Google Sheet
    return pd.DataFrame(data)

# Add Data to Google Sheets
def add_data(row):
    sheet_by_name.append_row(row)  # Append the row to the Google Sheet

# Sidebar form for data entry
with st.sidebar:
    st.header("Enter New Data")
    # Assuming the sheet has columns: 'Well', 'Nature', 'Field','Job_Date','TD', 'Description','Job_Type','Job_Status','Lowest_Perf'
    with st.form(key="data_form"):
        Well = st.text_input("Well")
        Nature = st.text_input("Nature")
        Field = st.text_input("Field")
        Job_Date = st.date_input("Job_Date")
        TD = st.text_input("TD")
        Description = st.text_input("Description")
        Job_Type = st.text_input("Job_Type")
        Job_Status = st.text_input("Job_Status")
        Lowest_Perf = st.text_input("Lowest_Perf")
        # Submit button inside the form
        submitted = st.form_submit_button("Submit")
        # Handle form submission
        if submitted:
            if Well and Job_Date:  # Basic validation to check if required fields are filled
                add_data([Well, Nature, Field, Job_Date, TD, Description, Job_Type, Job_Status, Lowest_Perf])  # Append the row to the sheet
                st.success("Data added successfully!")
            else:
                st.error("Please fill out the form correctly.")

# Display data in the main view
# st.header("Data Table")
df = read_data()
st.dataframe(df, width=2000, height=400)
