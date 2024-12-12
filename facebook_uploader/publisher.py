import requests
from .exceptions import PublishError

class ReelPublisher:
    def __init__(self, base_url: str, page_id: str, access_token: str, is_profile: bool):
        self.base_url = base_url
        self.page_id = page_id
        self.access_token = access_token
        self.is_profile = is_profile

    def publish(self, video_id: str, description: str, publish_time=None):
        """Publish or schedule the uploaded video"""
        if self.is_profile:
            url = f"{self.base_url}/me/video_reels"
        else:
            url = f"{self.base_url}/{self.page_id}/video_reels"
        
        payload = {
            'access_token': self.access_token,
            'description': description,
            'video_id': video_id
        }

        if self.is_profile:
            payload.update({
                'upload_phase': 'finish',
                'video_type': 'reels'
            })
        else:
            payload.update({
                'upload_phase': 'finish',
                'video_state': 'SCHEDULED' if publish_time else 'PUBLISHED'
            })

        if publish_time:
            payload['scheduled_publish_time'] = publish_time

        try:
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                raise PublishError(response.json())
            return response.json()
        except Exception as e:
            raise PublishError(f"Publishing failed: {str(e)}")