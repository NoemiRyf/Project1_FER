from fer import FER
from flask import Flask, url_for, render_template
from flask.helpers import send_from_directory
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = 'JSFKS'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)



class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only Images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload') 


@app.route('/')
def welcome():
    html = render_template('index.html')
    return html

	
@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_image():
    form = UploadForm()
    entry = ""
    if form.validate_on_submit():
        filename = secure_filename(photos.save(form.photo.data))
        file_url = url_for('get_file', filename=filename)
        # Open image using PIL
        input_image = Image.open("uploads/smile.jpg")
        input_image_arr = np.array(input_image)
        emotion_detector = FER()
        # Output image's information
        entry = emotion_detector.detect_emotions(input_image_arr)
        print(entry)
           
    else:
        file_url = None
    
    html = render_template('faceExpressionRecognition.html', form=form, file_url=file_url, entry=entry)
    return html

    if _name_ == "_main_":
        app.run(host="0.0.0.0", port=8000)


