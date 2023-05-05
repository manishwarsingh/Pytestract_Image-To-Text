from flask import Flask, json, request, jsonify,render_template
import os
import urllib.request
from werkzeug.utils import secure_filename

import cv2 as cv
import pytesseract
import sys 
app = Flask(__name__,template_folder='templates')
 
app.secret_key = "caircocoders-ednalan"
 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def home():
    # return render_template('index.html')
    return '<h2 style=text-align:center; > Hola! EveryOne welcome to my Flask Homepage!!</h2>'
 
@app.route('/get-text', methods=['POST'])
def upload_file():
    
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    # dict_obj= {}
    success = False
     
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True

            try:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print("image_path : ",image_path)
                image = cv.imread(image_path)
                text = pytesseract.image_to_string(image)

                output = text.strip()
                output = output.replace("\n'","")
                output = ''.join(output.splitlines())
                
                result ={
                "text" : output
                }
                # dict_obj.update(result)

            except Exception as e:
                print("Img is not found",e)
                pass

            # return jsonify(result)
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify(result)
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
 
if __name__ == '__main__':
    app.run(debug=True)