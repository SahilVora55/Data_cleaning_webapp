import streamlit as st
import pandas as pd
import numpy as np
import re

# Add a title to the app
st.set_page_config(page_title='Data Cleaning web-app', page_icon="./dataclean_icon.png", layout="wide")

# Add a file uploader to the app
uploaded_file = st.file_uploader('Upload your data file', type=['csv', 'xlsx'])

# Add a checkbox to skip header row
skip_header = st.checkbox('Skip header row',True)

# Display the uploaded data file
if uploaded_file is not None:
     # Load the data file into a Pandas DataFrame
    if uploaded_file.type == 'application/vnd.ms-excel':
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    else:
        df = pd.read_csv(uploaded_file, header= 0 if skip_header else None)
    col10, col11 = st.columns([1,3])
    with col10:
        st.write('**Uploaded Data:**')
    with col11:
        # Display the shape of the data
        st.write(f'Shape of data is : <span style="color:blue">{df.shape}</span>', unsafe_allow_html=True)
    st.dataframe(df, height=220)

    # Select columns to keep
    st.write('**Column Selection:**')
    cols_to_keep = []
    col_chunks = [df.columns[i:i+4] for i in range(0, len(df.columns), 4)]

    # Display columns in chunks of 4
    for cols_chunk in col_chunks:
        cols_column = st.columns(len(cols_chunk))
        for i, col in enumerate(cols_chunk):
            if cols_column[i].checkbox(col):
                cols_to_keep.append(col)

    # Keep only the selected columns
    if cols_to_keep:
        df = df[cols_to_keep]
        st.write('Dataframe with Selected Columns:')
        st.dataframe(df, height=220)
    else:
        st.write('No columns were selected.')

    st.write('**Rename selected columns:**')
    rename = st.checkbox('Rename columns')
    if rename:
        st.write('**Rename Columns:**')
        col1, col2, col3, col4 = st.columns(4)  # create 4 columns

        # Loop through each column and create a text input in each column
        rename_map = {}
        for i, col in enumerate(df.columns):
            with locals()[f"col{i % 4 + 1}"]:
                new_col_name = st.text_input(f'Rename "{col}" to:', col)
                if new_col_name != col:
                    rename_map[col] = new_col_name

        if rename_map:
            df = df.rename(columns=rename_map)
            st.write('Renamed Columns:')
            st.dataframe(df,height=220)
        else:
            st.write('No columns were renamed.')


    # Number of missing value in each column.
    st.write('**Missing value:**')
    if st.checkbox('Show number of missing data in each selected columns.'):
        st.write(df.isnull().sum())

    # Drop or Fill NaN values
    st.write('**Drop or Fill NaN values:**')
    if st.checkbox('Process for missing value Values'):
        # Replace missing values with NaN
        df.replace({'': np.nan, ' ': np.nan, 'NaN': np.nan, 'N/A': np.nan, 'n/a': np.nan, 'na': np.nan}, inplace=True)

        # Remove leading and trailing whitespaces
        df = df.applymap(lambda x: x.strip() if type(x) == str else x)

        # Choose fill method
        fill_methods = st.selectbox('Select a data filling method:', ['No Fill', 'Fill with Mean', 'Fill with Median', 'Fill with Mode', 'Fill with ffill', 'Fill with bfill'])

        if fill_methods == 'No Fill':
            # Drop NaN
            df.dropna(inplace=True)
        elif fill_methods == 'Fill with Mean':
            # Fill NaN with mean value
            df.fillna(df.mean(), inplace=True)
        elif fill_methods == 'Fill with Median':
            # Fill NaN with median value
            df.fillna(df.median(), inplace=True)
        elif fill_methods == 'Fill with Mode':
            # Fill NaN with mode value
            df.fillna(df.mode().iloc[0], inplace=True)
        elif fill_methods == 'Fill with ffill':
            # Fill NaN with forward fill method
            df.fillna(method='ffill', inplace=True)
        elif fill_methods == 'Fill with bfill':
            # Fill NaN with backward fill method
            df.fillna(method='bfill', inplace=True)


        # Display the cleaned data
        col7,col8 = st.columns([1,3])
        with col7:
            st.write('**Cleaned Data:**')
        with col8:
            st.write(f'Shape of cleaned data is : <span style="color:blue">{df.shape}</span>', unsafe_allow_html=True)
        st.dataframe(df,height=220)
        st.write('<span style="color:green">Successfully processed NaN values', unsafe_allow_html=True)


    # Add a download button to download the cleaned data
    cleaned_data = df.to_csv(index=False)
    if st.download_button(
        label='Download Cleaned Data',
        data=cleaned_data,
        file_name='cleaned_data.csv',
        mime='text/csv'):

        st.write('<span style="color:green">Downloaded successfully.', unsafe_allow_html=True)
