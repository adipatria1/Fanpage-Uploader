import os
import requests
from config import BASE_URL
import time

def upload_reel(page_id, access_token, video_path, description, schedule_time=None):
    """
    Upload video as a reel to Facebook page using multi-step process.
    """
    try:
        # Step 1: Initialize upload session
        video_id = _initialize_upload(page_id, access_token, video_path)
        
        # Step 2: Upload video content
        _upload_video_content(video_id, access_token, video_path)
        
        # Step 3: Finish upload and publish
        return _publish_reel(page_id, access_token, video_id, description, schedule_time)
    except Exception as e:
        raise Exception(f"Reel upload failed: {str(e)}")

def _initialize_upload(page_id, access_token, video_path):
    """Initialize upload session and get video ID."""
    url = f"{BASE_URL}/{page_id}/video_reels"
    video_size = os.path.getsize(video_path)
    
    data = {
        'access_token': access_token,
        'file_size': video_size,
        'upload_phase': 'start'
    }

    response = requests.post(url, data=data)
    response.raise_for_status()
    
    video_id = response.json().get('video_id')
    if not video_id:
        raise Exception("Failed to initialize video upload")
    return video_id

def _upload_video_content(video_id, access_token, video_path):
    """Upload the actual video content."""
    upload_url = f"https://rupload.facebook.com/video-upload/v21.0/{video_id}"
    video_size = os.path.getsize(video_path)
    
    headers = {
        'Authorization': f'OAuth {access_token}',
        'offset': '0',
        'file_size': str(video_size),
        'Content-Type': 'application/octet-stream'
    }
    
    with open(video_path, 'rb') as video_file:
        response = requests.post(upload_url, data=video_file.read(), headers=headers)
        response.raise_for_status()
        return response.json()

def _publish_reel(page_id, access_token, video_id, description, schedule_time=None):
    """Publish or schedule the reel."""
    url = f"{BASE_URL}/{page_id}/video_reels"
    
    data = {
        'access_token': access_token,
        'description': description,
        'video_id': video_id,
        'upload_phase': 'finish'
    }

    if schedule_time:
        data.update({
            'video_state': 'SCHEDULED',
            'scheduled_publish_time': schedule_time
        })
    else:
        data['video_state'] = 'PUBLISHED'

    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()