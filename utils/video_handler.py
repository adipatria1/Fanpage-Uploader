import os
from datetime import datetime
from pytz import timezone
import mimetypes

TEMP_UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(TEMP_UPLOAD_FOLDER, exist_ok=True)

def save_temp_media(media_file, index):
    """
    Save uploaded media to temporary file with proper extension.
    """
    timestamp = int(datetime.now().timestamp())
    original_filename = media_file.filename
    extension = os.path.splitext(original_filename)[1]
    
    filename = f"temp_{timestamp}_{index}{extension}"
    file_path = os.path.join(TEMP_UPLOAD_FOLDER, filename)
    media_file.save(file_path)
    return file_path

def parse_schedule_time(schedule_time_str):
    """
    Parse and convert local time to UTC timestamp for scheduling.
    """
    if not schedule_time_str:
        return None
        
    try:
        local_time = datetime.strptime(schedule_time_str, '%Y-%m-%dT%H:%M')
        jakarta_tz = timezone('Asia/Jakarta')
        local_time = jakarta_tz.localize(local_time)
        utc_time = local_time.astimezone(timezone('UTC'))
        return int(utc_time.timestamp())
    except ValueError as e:
        print(f"Error parsing schedule time: {str(e)}")
        return None

def cleanup_temp_file(file_path):
    """
    Remove temporary media file.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except OSError as e:
        print(f"Error removing temporary file: {str(e)}")

def get_media_type(file_path):
    """
    Determine if the file is a video or photo.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return 'video' if mime_type and mime_type.startswith('video') else 'photo'