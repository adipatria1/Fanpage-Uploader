from flask import Flask, render_template
from config import USER_ACCESS_TOKEN
from utils.facebook_api import get_page_list
from routes.upload_routes import upload_bp

app = Flask(__name__)
app.register_blueprint(upload_bp)

@app.route('/')
def index():
    """
    Main page with media upload form.
    """
    pages = get_page_list(USER_ACCESS_TOKEN)
    return render_template('index.html', pages=pages)

if __name__ == '__main__':
    app.run(debug=True)