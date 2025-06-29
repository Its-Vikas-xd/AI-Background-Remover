import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            
            # Process image
            output_filename = f"removed_bg_{filename.split('.')[0]}.png"
            output_path = os.path.join(app.config['RESULT_FOLDER'], output_filename)
            
            with open(upload_path, 'rb') as i:
                with open(output_path, 'wb') as o:
                    input_data = i.read()
                    output_data = remove(input_data)
                    o.write(output_data)
            
            return render_template('index.html', 
                                   original=upload_path, 
                                   result=output_path)
    
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)
    app.run(debug=True)