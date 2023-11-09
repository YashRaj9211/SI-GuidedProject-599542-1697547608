import numpy as np
import os
from PIL import Image
from flask import redirect
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import preprocess_input

# Load the pre-trained model
model = load_model("./wcv.h5")

app = Flask(__name__)

# Ensure the 'uploads' folder exists
os.makedirs(os.path.join(app.root_path, 'uploads'), exist_ok=True)

@app.route('/')
@app.route('/home')
def home():
    # Assuming 'templates' is your folder for HTML files and 'index.html' is in that folder
    return render_template("index.html")

@app.route('/input')
def input():
    # Assuming 'input.html' is also in the 'templates' folder
    return render_template("input.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    print(request.method)
    if request.method == "POST":
        # Check if the file part is present in request
        if 'image' not in request.files:
            print('No file part')
            return redirect(request.url)
        f = request.files['image']
        print(f.filename)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if f.filename == '':
            print('No selected file')
            return redirect(request.url)
        
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(filepath)

        img = image.load_img(filepath, target_size=(250, 250, 3))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        img_data = preprocess_input(x)
        prediction = model.predict(img_data)
        predicted_class = np.argmax(prediction, axis=1)

        index = ['Cloudy',
'Rain',
'Shine',
'Sunrise']
        result = str(index[predicted_class[0]])
        print(result)
        
        # Make sure 'output.html' is in your 'templates' folder
        return result
    
    # A GET request to '/predict' could return a useful page or redirect
    Output =  request.args.get("output")
    return render_template('output.html', output = Output)

if __name__ == "__main__":
    app.run(debug=False)
