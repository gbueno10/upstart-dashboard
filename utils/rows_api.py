import requests
from dotenv import load_dotenv
import os
import pandas as pd 

load_dotenv()
api_key=os.getenv('ROWS_API_KEY')



def get_spreadsheets_ids(api_key):
    # URL endpoint for fetching spreadsheets
    api_url = 'https://api.rows.com/v1/spreadsheets'
    
    # Set up the headers with your API key for authentication
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Fetch the list of spreadsheets
        response = requests.get(api_url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Extract spreadsheet IDs and titles
            spreadsheets = response.json()
            spreadsheet_ids = [(spreadsheet['id'], spreadsheet['name']) for spreadsheet in spreadsheets['items']]
            return spreadsheet_ids
        else:
            print(f"Failed to retrieve spreadsheets: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")

'''
Exemplo de execution
spreadsheets_ids = get_spreadsheets_ids(api_key)
if spreadsheets_ids:
    for spreadsheet_id, title in spreadsheets_ids:
        print(f"ID: {spreadsheet_id} - Title: {title}")

'''




def fetch_table_data(api_key, spreadsheet_id, table_id, cell_range):
    base_url = 'https://api.rows.com/v1/spreadsheets'
    url = f"{base_url}/{spreadsheet_id}/tables/{table_id}/values/{cell_range}"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
            data = response.json()
            if response.status_code == 200:
                data = response.json()
                if 'items' in data and data['items']:
                    df = pd.DataFrame(data['items'][1:], columns=data['items'][0])
                    df['Date'] = pd.to_datetime(df['Date'])
                    # Corrigindo números que são interpretados como strings
                    cols_to_fix = ['Impressions', 'Unique Impressions', 'Likes', 'Comments', 'Shares']
                    for col in cols_to_fix:
                        df[col] = df[col].astype(str).str.replace(',', '').astype(float)
                    return df
            else:
                print("No data to display.")
                return pd.DataFrame()  # Return an empty DataFrame if no data
    else:
        error_message = f"Failed to retrieve values: {response.status_code}, Response: {response.text}"
        print(error_message)
        return None

"""
spreadsheet_id = '7FIZkV8hcSztF47bvxPzUw'  # Example spreadsheet ID
table_id = '1dc0bfbf-d735-4443-a00a-bfd419a06f5d'  # Example table ID
cell_range = 'A1:Z999'  # Example range

data=fetch_table_data(api_key,spreadsheet_id, table_id, cell_range)
pd.set_option('display.max_rows', None)  # ou um número específico de linhas
pd.set_option('display.max_columns', None)  # para exibir todas as colunas
pd.set_option('display.width', None)  
print(data)
"""


