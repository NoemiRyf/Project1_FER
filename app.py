import os


# Your existing Flask code below
from fer import FER
from flask import Flask, url_for, render_template, request
from flask.helpers import send_from_directory
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'JSFKS'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES) 
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Detect Emotion')
#test

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/uploader', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    file_url = None
    entry = ""

    if form.validate_on_submit():
        # Remove all previously uploaded files
        for filename in os.listdir(app.config['UPLOADED_PHOTOS_DEST']):
            os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))

        # Save the most recently uploaded file
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
        file_url = url_for('get_file', filename=filename)


        # Open image using PIL
        input_image = Image.open(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
        input_image_arr = np.array(input_image)

        emotion_detector = FER()
        # Output image's information
        entry = emotion_detector.detect_emotions(input_image_arr)
  


    return render_template('face_expression_recognition.html', form=form, file_url=file_url, entry=entry)


@app.route('/')
def welcome():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
