from flask import Flask, render_template, request, url_for, abort
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

@app.route('/')
@app.route('/live-webcam')
def index():
    return render_template('index.html')

@app.route('/video-detection')
@app.route('/image-detection')
def not_found():
    abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video_file' not in request.files:
        return "No file part", 400

    file = request.files['video_file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        video_url = url_for('static', filename='uploads' + file.filename)
        return render_template('video_display.html', video_url=video_url)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
