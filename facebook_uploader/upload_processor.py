import requests
from .exceptions import ProcessUploadError

class UploadProcessor:
    def __init__(self, api_version: str, access_token: str):
        self.api_version = api_version
        self.access_token = access_token

    def process(self, video_id: str, file_data: bytes, file_size: int):
        """Process the actual file upload"""
        url = f'https://rupload.facebook.com/video-upload/{self.api_version}/{video_id}'
        headers = {
            'Authorization': f'OAuth {self.access_token}',
            'offset': '0',
            'file_size': str(file_size),
            'Content-Type': 'application/octet-stream'
        }
        
        try:
            response = requests.post(url, data=file_data, headers=headers)
            if response.status_code != 200:
                raise ProcessUploadError(response.json())
        except Exception as e:
            raise ProcessUploadError(f"Upload process failed: {str(e)}")