import streamlit as st
import pandas as pd
from io import StringIO

from table import pipeline
import fitz

st.set_page_config(layout='wide')

def count_single_class(uploaded_file,) -> pd.DataFrame:
    if uploaded_file is not None:
        st.write(uploaded_file.name)
        bytes_data = uploaded_file.getvalue()
        data = fitz.open('pdf', bytes_data)
        table = pipeline(data)
        st.table(table)
        return table

def main():
    summation = None
    uploaded_files = st.file_uploader('Choose a file', type='pdf', accept_multiple_files=True)
    for file in uploaded_files:
        current_class = count_single_class(file)
        if summation is None:
            summation = pd.DataFrame({'nome':current_class.nome.values})
        summation[file.name.split('.')[0]] = current_class[['soma']]
    if summation is not None:
        summation['soma'] = summation.drop(columns=['nome']).sum(axis=1)
        st.table(summation)
        summation.to_excel('summation.xlsx')
        st.download_button(
            label='Download',
            data=open('summation.xlsx', 'rb'),
            file_name='summation.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    return summation

if __name__ == '__main__':
    main()
