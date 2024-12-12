import requests
from config import BASE_URL

def get_page_list(user_access_token):
    """Fetch list of pages based on user access token."""
    url = f"{BASE_URL}/me/accounts"
    params = {
        'access_token': user_access_token,
        'fields': 'id,name,access_token'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching pages: {str(e)}")
        return []