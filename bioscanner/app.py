from flask import Flask, render_template, request, redirect, url_for, session
from flask_assets import Environment, Bundle
from werkzeug.utils import secure_filename
import utils as tech
import base64
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
assets = Environment(app)

# Configurar assets (CSS y JS)
css = Bundle(
    'css/style.css',
    'css/loading.css',
    output='gen/packed.css'
)
assets.register('css_all', css)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
DETECTION_RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/detection_results')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Crear las carpetas necesarias al inicio
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECTION_RESULTS, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_image(image_path):
    pass

def is_jaguar(image_path, request):
    file = request.files['file']
    print("Making inference...")
    print(file)
    #here we have the file as binary
    with open(image_path, 'rb') as f:
        fileb = f.read()
    f.close()
    #fileb = request.files['file'].read()
    #file_path = dy.save_image_static(file)
    #img = dt.loadImage(fileb)
    #outputs = [int(x[0][0]) for x in new_model.predict(img)]
    #pred= label.boundingbox(file_path,outputs)
    #we started drawing the bounding box to the image
    #we got the bytes and encode it to b64
    my_string = base64.b64encode(fileb).decode()
    print("Image encoded b64")
    #we got the width and the height from the image
    w,h,try1 = tech.b64_to_PIL(my_string)
    print("Image converted to PIL")
    #lets make the prediction 
    predicts = tech.query_class_api(my_string)
    #predicts = tech.query_class_api(my_string)
    #resize the bounding box the original proportions 
    print("Making query to the presence API")
    response = predicts.json()
    print(response)
    #draw the rectangle
    return response["Resultados"][0] > 0.5


def make_inference(image_path, request):
    file = request.files['file']
    print("Making inference...")
    print(file)
    #here we have the file as binary
    with open(image_path, 'rb') as f:
        fileb = f.read()
    f.close()
    #fileb = request.files['file'].read()
    #file_path = dy.save_image_static(file)
    #img = dt.loadImage(fileb)
    #outputs = [int(x[0][0]) for x in new_model.predict(img)]
    #pred= label.boundingbox(file_path,outputs)
    #we started drawing the bounding box to the image
    #we got the bytes and encode it to b64
    my_string = base64.b64encode(fileb).decode()
    print("Image encoded b64")
    #we got the width and the height from the image
    w,h,try1 = tech.b64_to_PIL(my_string)
    print("Image converted to PIL")
    #lets make the prediction 
    predicts = tech.query_api(my_string)
    #predicts = tech.query_class_api(my_string)
    #resize the bounding box the original proportions 
    print("Making query to the API")
    print(predicts)
    #draw the rectangle
    try2 = tech.draw_rectangle(try1,w,h,predicts)
    #convert the Image object to b64
    try3 = tech.img_to_base64_str(try2)
    #return the new image drawn 
        
    #return render(request, 'mlModels/detect.html', {'outputs':try3})
    return try3

def detect_jaguar(image_path, request):
    """
    Placeholder for the external jaguar detection function
    Returns: (boolean, str) - Detection result and path to result image
    """
    jaguar_present = is_jaguar(image_path, request)
    # Here you would call your actual detection model
    if jaguar_present:
        data = make_inference(image_path, request)
        #print(data)
        image_file = "inference_" + str(random.randint(1, 10000)) + ".png"
        filepath = os.path.join(DETECTION_RESULTS, image_file)
        print(f"Saving results... {filepath}")
        tech.save_base64_to_png(data, filepath)
        return True, filepath

    return False, ''  # Replace with actual detection

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return render_template('upload.html', error='No se seleccionó ningún archivo')
            
            file = request.files['file']
            if file.filename == '':
                return render_template('upload.html', error='No se seleccionó ningún archivo')
            
            if file and allowed_file(file.filename):
                try:
                    # Save the uploaded file
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    # Get file size in KB
                    file_size = os.path.getsize(filepath) / 1024  # Convert to KB
                    
                    # Store file info in session
                    session['uploaded_file'] = {
                        'name': filename,
                        'size': f"{file_size:.0f}",
                        'path': filepath,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    return redirect(url_for('uploaded'))
                except Exception as e:
                    print(f"Error processing image: {str(e)}")
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    return render_template('upload.html', error='Error al procesar la imagen')
            else:
                return render_template('upload.html', error='Tipo de archivo no permitido')
        except Exception as e:
            print(f"Upload error: {str(e)}")
            return render_template('upload.html', error='Error al subir el archivo')
            
    return render_template('upload.html')

@app.route('/uploaded')
def uploaded():
    if 'uploaded_file' not in session:
        return redirect(url_for('upload'))
        
    file_info = session['uploaded_file']
    time_uploaded = datetime.strptime(file_info['timestamp'], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    time_diff = now - time_uploaded
    
    # Calculate time difference in minutes
    minutes = int(time_diff.total_seconds() / 60)
    
    return render_template('uploaded.html', 
                         filename=file_info['name'],
                         filesize=file_info['size'],
                         minutes_ago=minutes)

@app.route('/analyze')
def analyze():
    if 'uploaded_file' not in session:
        return redirect(url_for('upload'))
    # Aquí irá la lógica de análisis
    return "Análisis en proceso..."

# Esta ruta es del demo
@app.route('/jaguar-detected')
def jaguar_detected():
    result = session['result'] 
    return render_template('jaguar_detected.html', result=result)
# Esta ruta es del demo
@app.route('/no-jaguar')
def no_jaguar_found():
    return render_template('no_jaguar.html')
# Estas ruta se implentó en el nuevo diseño
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')


@app.route('/request-access')
def waitlist():
    return render_template('request_access.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
