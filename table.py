import fitz
import pandas as pd


def fitz_doc_to_table(doc:bytes) -> pd.DataFrame:
    result = list()
    columns = None
    for page in doc:
        tables = page.find_tables()
        for table in tables:
            rows = table.extract()
            for (index, row) in enumerate(rows):
                if index == 3:
                    columns = row
                if len(row) == 60 and row[0].isdigit() and row[-1].isdigit():
                    result.append(row)
    columns[1] = 'nome'
    return pd.DataFrame(result, columns=columns)

def pdf_to_table(pdf_path:str) -> pd.DataFrame:
    doc = fitz.open(pdf_path)
    return fitz_doc_to_table(doc)

def filter_df_by_month(df:pd.DataFrame, month:str) -> pd.DataFrame:
    names = list(df.pop('nome').values)
    dates = df.filter(regex=f'/{month}/')
    dates['nome'] = names
    return dates

def sum_fs(df:pd.DataFrame) -> pd.DataFrame:
    df['soma'] = df.apply(lambda x: len([f for f in x if f=='F']), axis=1)
    return df


def pipeline(doc:bytes, month:str='12') -> pd.DataFrame:
    df = fitz_doc_to_table(doc)
    df = filter_df_by_month(df, month)
    df = sum_fs(df)
    df = _differentiate_repeated_columns(df)
    return df


def _differentiate_repeated_columns(df: pd.DataFrame) -> pd.DataFrame:
    column_counts = {}
    new_columns = []
    
    for column in df.columns:
        if column in column_counts:
            column_counts[column] += 1
            new_columns.append(f'{column}-{column_counts[column]}')
        else:
            column_counts[column] = 0
            new_columns.append(column)
    df.columns = new_columns
    return df
if __name__ == '__main__':
    doc = fitz.open('index.pdf')
    df = pipeline(doc)
    print(df)
