import requests
from config import BASE_URL
import mimetypes
import os

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

def upload_reel(page_id, access_token, video_path, description, schedule_time=None):
    """Upload video as a reel to Facebook page."""
    # Step 1: Initialize upload session
    init_url = f"{BASE_URL}/{page_id}/video_reels"
    
    with open(video_path, 'rb') as video_file:
        video_size = os.path.getsize(video_path)
        
        init_data = {
            'access_token': access_token,
            'file_size': video_size,
            'upload_phase': 'start'
        }

        init_response = requests.post(init_url, data=init_data)
        init_response.raise_for_status()
        video_id = init_response.json().get('video_id')

        if not video_id:
            raise Exception("Failed to initialize video upload")

        # Step 2: Upload video content
        upload_url = f"https://rupload.facebook.com/video-upload/{BASE_URL.split('/')[-1]}/{video_id}"
        headers = {
            'Authorization': f'OAuth {access_token}',
            'offset': '0',
            'file_size': str(video_size),
            'Content-Type': 'application/octet-stream'
        }
        
        video_file.seek(0)
        upload_response = requests.post(upload_url, data=video_file.read(), headers=headers)
        upload_response.raise_for_status()

        # Step 3: Finish upload and publish
        publish_data = {
            'access_token': access_token,
            'description': description,
            'video_id': video_id,
            'upload_phase': 'finish'
        }

        if schedule_time:
            publish_data['scheduled_publish_time'] = schedule_time

        publish_response = requests.post(init_url, data=publish_data)
        publish_response.raise_for_status()
        return publish_response.json()

def upload_media(page_id, access_token, media_path, description, schedule_time=None):
    """Upload photo or video to Facebook page."""
    mime_type, _ = mimetypes.guess_type(media_path)
    is_video = mime_type and mime_type.startswith('video')
    
    endpoint = 'videos' if is_video else 'photos'
    url = f"{BASE_URL}/{page_id}/{endpoint}"
    
    with open(media_path, 'rb') as media_file:
        files = {
            'source': (os.path.basename(media_path), media_file, mime_type),
        }
        
        data = {
            'access_token': access_token,
            'message': description
        }

        if schedule_time:
            data['scheduled_publish_time'] = schedule_time

        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()