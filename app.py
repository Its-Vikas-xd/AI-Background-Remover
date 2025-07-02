import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from rembg import remove

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['RESULT_FOLDER'] = '/tmp/results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_first_request
def create_folders():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file selected')
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            
            output_filename = f"removed_bg_{filename.split('.')[0]}.png"
            output_path = os.path.join(app.config['RESULT_FOLDER'], output_filename)
            
            with open(upload_path, 'rb') as i:
                with open(output_path, 'wb') as o:
                    input_data = i.read()
                    output_data = remove(input_data)
                    o.write(output_data)
            
            # You cannot display the image from /tmp on Vercel directly.
            return render_template('index.html', result='Image processed successfully (but file not saved permanently on Vercel).')
    
    return render_template('index.html')

def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)
