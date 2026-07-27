import os
from openai import OpenAI
from monday_client import fetch_board_data

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEALS_BOARD_ID = os.getenv("DEALS_BOARD_ID")
WORK_ORDERS_BOARD_ID = os.getenv("WORK_ORDERS_BOARD_ID")

def query_business_agent(user_query):
    # Dynamically fetch latest board data
    deals_df = fetch_board_data(DEALS_BOARD_ID)
    work_orders_df = fetch_board_data(WORK_ORDERS_BOARD_ID)
    
    deals_csv = deals_df.to_csv(index=False)
    work_orders_csv = work_orders_df.to_csv(index=False)
    
    system_prompt = f"""
    You are an executive BI Assistant for C-suite founders.
    Analyze the live Monday.com datasets below to answer the user's prompt.
    
    CRITICAL INSTRUCTIONS:
    1. Provide insights and context, not just raw counts or tables.
    2. If there are missing, incomplete, or messy records, explicitly state the data quality caveats.
    3. Cross-reference both datasets when analyzing high-level pipeline vs execution.
    
    --- SALES DEALS BOARD DATA ---
    {deals_csv}
    
    --- WORK ORDERS BOARD DATA ---
    {work_orders_csv}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0.2
    )
    
    return response.choices[0].message.content