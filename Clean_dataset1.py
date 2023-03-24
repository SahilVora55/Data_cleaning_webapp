import streamlit as st
import pandas as pd
import numpy as np
import re

# Add a title to the app
st.title('Data Cleaning App')

# Add a file uploader to the app
uploaded_file = st.file_uploader('Upload your data file', type=['csv', 'xlsx'])

# Add a checkbox to skip header row
skip_header = st.sidebar.checkbox('Skip header row')

# Display the uploaded data file
if uploaded_file is not None:
     # Load the data file into a Pandas DataFrame
    if uploaded_file.type == 'application/vnd.ms-excel':
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    else:
        df = pd.read_csv(uploaded_file, delimiter=delimiter, header= 0 if skip_header else None)
    st.write('**Uploaded Data:**')
    st.write(df)

    # Add a text area for column names
    st.write('**Column Renaming:**')
    column_names = st.text_area('Enter all column names (separated by commas)| The number of columns entered must match the existing number of columns in the dataset. | Skip this if you want to keep existing column names.')
    if column_names:
        column_names = re.split(r'\s*,\s*', column_names)
        df.columns = column_names
        st.write('Renamed Columns:')
        st.write(df)
    
    # Select columns to keep
    st.sidebar.write('**Column Selection:**')
    cols = st.sidebar.multiselect('Select columns to keep', options=df.columns)

    # Keep only the selected columns
    if cols:
        df = df[cols]

    # Number of missing value in each column.
    if st.sidebar.button('Missing data in each selected column'):
        st.write(df.isnull().sum())

    # Drop NaN values
    if st.sidebar.button('Drop NaN Values'):
        # Replace missing values with NaN
        df.replace({'': np.nan, ' ': np.nan, 'NaN': np.nan, 'N/A': np.nan, 'n/a': np.nan, 'na': np.nan}, inplace=True)

        # Remove leading and trailing whitespaces
        df = df.applymap(lambda x: x.strip() if type(x) == str else x)

        # Drop NaN
        df.dropna(inplace=True)

        # Display the cleaned data
        st.write('**Cleaned Data:**')
        st.write(df)
        st.sidebar.write('<span style="color:green">Successfully removed raws containing NaN values', unsafe_allow_html=True)


    # Add a download button to download the cleaned data
    cleaned_data = df.to_csv(index=False)
    if st.download_button(
        label='Download Cleaned Data',
        data=cleaned_data,
        file_name='cleaned_data.csv',
        mime='text/csv'):

        st.write('<span style="color:green">Download successfully.', unsafe_allow_html=True)