from .upload_session import UploadSession
from .upload_processor import UploadProcessor
from .publisher import ReelPublisher
from .exceptions import ReelIdNoneError
from .reel import Reel
import requests

class FacebookReelsAPI:
    def __init__(self, page_id: str, page_token: str, api_version: str = 'v21.0', is_profile: bool = False):
        self.page_id = page_id
        self.page_access_token = page_token
        self.api_version = api_version
        self.base_url = f"https://graph.facebook.com/{api_version}"
        self.is_profile = is_profile
        
        # Initialize components
        self.upload_session = UploadSession(self.base_url, page_id, page_token, api_version, is_profile)
        self.upload_processor = UploadProcessor(api_version, page_token)
        self.publisher = ReelPublisher(self.base_url, page_id, page_token, is_profile)

    def is_page_access_token_valid(self) -> bool:
        endpoint = 'videos' if self.is_profile else 'video_reels'
        url = f"{self.base_url}/{self.page_id}/{endpoint}"
        params = {
            'since': 'today',
            'access_token': self.page_access_token
        }
        response = requests.get(url, params=params)
        return response.status_code == 200

    def upload(self, reel: Reel, publish_time=None) -> str:
        """Upload a reel and return its ID"""
        try:
            # Initialize upload
            reel.id = self.upload_session.initialize(reel.file_size)
            
            # Process upload
            self.upload_processor.process(reel.id, reel.file_data, reel.file_size)
            
            # Publish
            self.publisher.publish(reel.id, reel.description, publish_time)
            
            return reel.id
        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")

    def upload_status(self, reel: Reel, fields: list[str] = None) -> dict:
        if reel.id is None:
            raise ReelIdNoneError('Initialize upload first')

        if fields is None:
            fields = ['status']

        url = f'{self.base_url}/{reel.id}'
        params = {
            'access_token': self.page_access_token,
            'fields': ','.join(fields)
        }

        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to get upload status: {str(e)}")

    def get_reels(self, since: str | int = None, until: str | int = None) -> list[Reel]:
        endpoint = 'videos' if self.is_profile else 'video_reels'
        url = f'{self.base_url}/{self.page_id}/{endpoint}'
        params = {
            'access_token': self.page_access_token,
            'since': since,
            'until': until
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json().get('data', [])
            
            return [
                Reel(
                    description=reel_data.get('description', ''),
                    id=reel_data.get('id'),
                    updated_time=reel_data.get('updated_time')
                )
                for reel_data in data
            ]
        except Exception as e:
            raise Exception(f"Failed to get reels: {str(e)}")