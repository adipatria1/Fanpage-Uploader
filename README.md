# Facebook Media Uploader

A Flask-based web application for uploading and scheduling media content (Reels, Videos, Photos) to Facebook Pages.

## Features

- Upload multiple media files simultaneously
- Support for Facebook Reels and regular media posts
- Schedule posts for future publication
- Multiple page selection for batch uploads
- Automatic hashtag management
- Auto-fill descriptions from filenames
- Intelligent scheduling with automatic time increments

## Prerequisites

- Python 3.8 or higher
- Facebook Developer Account
- Facebook App with proper permissions
- Page Access Tokens for target Facebook Pages

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd facebook-media-uploader
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Facebook Access Token:
```
FB_USER_ACCESS_TOKEN=your_facebook_access_token_here
```

## Configuration

### Facebook API Setup

1. Create a Facebook App at [developers.facebook.com](https://developers.facebook.com)
2. Enable the following permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`
   - `publish_video`
3. Generate a User Access Token with the required permissions
4. Add the token to your `.env` file

## Usage

1. Start the application:
```bash
python app.py
```

2. Access the web interface at `http://localhost:5000`

3. Upload Media:
   - Select target Facebook Pages
   - Choose media files (videos for Reels, photos/videos for regular posts)
   - Add descriptions or use auto-fill from filenames
   - Select hashtags (optional)
   - Set schedule times (optional)
   - Click Upload

### Supported Features

#### Media Types
- **Reels**: MP4 video files
- **Regular Posts**: Photos (JPG, PNG) and Videos (MP4)

#### Scheduling
- Immediate posting
- Future scheduling with automatic time increments
- Timezone-aware scheduling (configured for Asia/Jakarta)

#### Description Management
- Manual entry
- Auto-fill from filenames
- Hashtag presets
- Custom hashtag combinations

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- Upload failures
- API errors
- Scheduling issues
- Token validation

## Best Practices

1. **File Types**
   - Use MP4 format for videos
   - Optimize video size before upload
   - Use high-quality images for photos

2. **Scheduling**
   - Space out posts by at least 1 hour
   - Consider peak engagement times
   - Use timezone-aware scheduling

3. **Descriptions**
   - Keep descriptions concise
   - Use relevant hashtags
   - Include calls to action

## Troubleshooting

### Common Issues

1. **Upload Failures**
   - Verify access token validity
   - Check file size limits
   - Ensure proper file formats

2. **Scheduling Issues**
   - Verify timezone settings
   - Check for conflicting schedules
   - Ensure future dates are valid

3. **Permission Errors**
   - Verify page access tokens
   - Check app permissions
   - Ensure proper page roles


## Acknowledgments

This project was inspired by:
- [Xavier Zambrano](https://github.com/xavierZambrano/)
