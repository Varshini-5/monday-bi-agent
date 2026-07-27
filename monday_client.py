import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_URL = "https://api.monday.com/v2"
API_KEY = os.getenv("MONDAY_API_KEY")

def fetch_board_data(board_id):
    """Fetches raw item data from a Monday.com board using GraphQL."""
    query = f'''
    query {{
        boards (ids: {board_id}) {{
            name
            items_page {{
                items {{
                    id
                    name
                    column_values {{
                        title
                        text
                    }}
                }}
            }}
        }}
    }}
    '''
    headers = {
        "Authorization": API_KEY,
        "API-Version": "2023-10",
        "Content-Type": "application/json"
    }
    response = requests.post(MONDAY_API_URL, json={'query': query}, headers=headers)
    
    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()
    items = data['data']['boards'][0]['items_page']['items']
    
    rows = []
    for item in items:
        row = {"Item Name": item["name"]}
        for col in item["column_values"]:
            row[col["title"]] = col["text"]
        rows.append(row)
        
    df = pd.DataFrame(rows)
    return clean_data(df)

def clean_data(df):
    """Cleans null values, inconsistent dates, and formatted currency text."""
    if df.empty:
        return df
    
    # 1. Fill empty missing values explicitly
    df = df.fillna("Unknown / Missing")
    
    # 2. Convert currency/numeric text (e.g. '$10,000' -> 10000.0)
    for col in df.columns:
        if any(term in col.lower() for term in ['value', 'amount', 'revenue', 'budget', 'price']):
            df[col] = df[col].astype(str).str.replace(r'[\$,]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
            
    return df