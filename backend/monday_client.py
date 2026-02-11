import requests
import os

API_URL = "https://api.monday.com/v2"
API_TOKEN = os.getenv("MONDAY_API_TOKEN")

HEADERS = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

def fetch_board_items(board_id):
    query = f"""
    {{
      boards(ids: {board_id}) {{
        items_page {{
          items {{
            name
            column_values {{
              id
              text
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        API_URL,
        json={"query": query},
        headers=HEADERS
    )

    result = response.json()

    # 🔴 HANDLE API ERRORS GRACEFULLY
    if "errors" in result:
        raise Exception(f"Monday API Error: {result['errors']}")

    if "data" not in result:
        raise Exception(f"Unexpected response from monday.com: {result}")

    return result["data"]["boards"][0]["items_page"]["items"]
