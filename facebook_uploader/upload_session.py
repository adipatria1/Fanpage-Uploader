import time
import requests
from .exceptions import InitializeUploadError

class UploadSession:
    def __init__(self, base_url: str, page_id: str, access_token: str, api_version: str, is_profile: bool):
        self.base_url = base_url
        self.page_id = page_id
        self.access_token = access_token
        self.api_version = api_version
        self.is_profile = is_profile

    def initialize(self, file_size: int) -> str:
        """Initialize upload session and return video ID"""
        endpoint = 'videos' if self.is_profile else f"{self.page_id}/videos"
        url = f"{self.base_url}/{endpoint}"
        
        payload = {
            'access_token': self.access_token,
            'file_size': file_size,
            'upload_phase': 'start'
        }

        if self.is_profile:
            payload.update({
                'upload_setting': '{"video_type":"reels"}',
                'composer_session_id': f"reels_upload_{int(time.time())}",
                'video_type': 'reels'
            })
        else:
            payload['video_type'] = 'VIDEO_ASSET'
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            video_id = response.json().get('video_id')
            if not video_id:
                raise InitializeUploadError("No video_id in response")
            return video_id
        else:
            raise InitializeUploadError(response.json())