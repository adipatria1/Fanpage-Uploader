from flask import Blueprint, request, jsonify
from utils.video_handler import save_temp_media, parse_schedule_time, cleanup_temp_file
from utils.facebook_api.media import upload_media
from utils.facebook_api.reels import upload_reel
from utils.facebook_api.utils import get_media_type

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_content():
    """
    Handle multiple media uploads to Facebook Pages.
    """
    try:
        # Get form data
        upload_type = request.form.get('upload_type', 'reels')
        selected_pages = request.form.getlist('pages')
        descriptions = request.form.getlist('description[]')
        schedule_times = request.form.getlist('schedule_time[]')
        media_files = request.files.getlist('media[]')

        # Validate inputs
        if not selected_pages:
            return jsonify({
                "status": "error",
                "message": "Please select at least one page."
            })

        if len(descriptions) != len(media_files) or len(schedule_times) != len(media_files):
            return jsonify({
                "status": "error",
                "message": "Inconsistent number of media files, descriptions, or schedule times."
            })

        results = []
        for i, media_file in enumerate(media_files):
            # Save and process media file
            temp_file_path = save_temp_media(media_file, i)
            publish_time = parse_schedule_time(schedule_times[i])

            # Validate media type for reels
            if upload_type == 'reels' and get_media_type(temp_file_path) != 'video':
                cleanup_temp_file(temp_file_path)
                return jsonify({
                    "status": "error",
                    "message": f"File {i + 1} must be a video for reels upload."
                })

            # Upload to each selected page
            for page in selected_pages:
                try:
                    page_id, page_access_token = page.split('|')
                    
                    if upload_type == 'reels':
                        result = upload_reel(
                            page_id=page_id,
                            access_token=page_access_token,
                            video_path=temp_file_path,
                            description=descriptions[i],
                            schedule_time=publish_time
                        )
                    else:
                        result = upload_media(
                            page_id=page_id,
                            access_token=page_access_token,
                            media_path=temp_file_path,
                            description=descriptions[i],
                            schedule_time=publish_time
                        )

                    results.append({
                        "page_id": page_id,
                        "status": "success",
                        "media_index": i + 1,
                        "media_id": result.get('id')
                    })
                except Exception as e:
                    results.append({
                        "page_id": page_id,
                        "status": "error",
                        "media_index": i + 1,
                        "error": str(e)
                    })

            cleanup_temp_file(temp_file_path)

        return jsonify({
            "status": "success",
            "message": "Upload process completed",
            "results": results
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })