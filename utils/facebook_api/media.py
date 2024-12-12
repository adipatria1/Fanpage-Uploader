import os
import requests
from .utils import get_media_type, get_api_url

def upload_media(page_id, access_token, media_path, description, schedule_time=None):
    """
    Upload media (photo/video) to Facebook page using simplified approach.
    """
    try:
        media_type = get_media_type(media_path)
        url = get_api_url(page_id, media_type)

        with open(media_path, 'rb') as media_file:
            files = {'source': (os.path.basename(media_path), media_file, 'application/octet-stream')}
            data = {
                'access_token': access_token,
                'message': description  # Changed from description to message for regular posts
            }

            if schedule_time:
                data['scheduled_publish_time'] = schedule_time
                data['published'] = False

            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
            return response.json()
            
    except Exception as e:
        raise Exception(f"Media upload failed: {str(e)}")