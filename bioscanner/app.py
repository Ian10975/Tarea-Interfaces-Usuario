from flask import Flask, render_template, request, redirect, url_for, session
from flask_assets import Environment, Bundle
from werkzeug.utils import secure_filename
import utils as tech
import base64
import os
import random

app = Flask(__name__)
assets = Environment(app)

# Configurar assets (CSS y JS)
css = Bundle(
    'css/style.css',
    output='gen/packed.css'
)
assets.register('css_all', css)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
DETECTION_RESULTS = 'static/detection_results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

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
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the image
            has_jaguar, result_image = detect_jaguar(filepath, request)
            print(has_jaguar, result_image)
            print(url_for('jaguar_detected'))
            print(url_for('no_jaguar_found'))
            session["result"] = result_image
            
            if has_jaguar:
                return redirect(url_for('jaguar_detected', result=result_image))
            else:
                return redirect(url_for('no_jaguar_found'))
            
    return render_template('upload.html')

@app.route('/jaguar-detected')
def jaguar_detected():
    result = session['result'] 
    return render_template('jaguar_detected.html', result=result)

@app.route('/no-jaguar')
def no_jaguar_found():
    return render_template('no_jaguar.html')

if __name__ == '__main__':
    # Create necessary folders if they don't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(DETECTION_RESULTS, exist_ok=True)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, port=5000, host='0.0.0.0')