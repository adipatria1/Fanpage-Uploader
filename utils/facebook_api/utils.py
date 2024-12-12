import mimetypes
from config import BASE_URL

def get_media_type(file_path):
    """
    Determine media type based on file extension.
    """
    if file_path.lower().endswith(('.mp4', '.mov')):
        return 'video'
    return 'photo'

def get_api_url(page_id, media_type):
    """
    Generate the appropriate API URL based on media type.
    """
    return f"{BASE_URL}/{page_id}/{media_type}s"