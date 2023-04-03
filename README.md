# Project1_FER

This is a Python Flask web application that provides a web interface for recognizing emotions in facial expressions.
The app.py imports the necessary libraries, including Flask, PIL (Python Imaging Library), numpy, and FER (Facial Emotion Recognition) library.
The app creates an instance of Flask and sets the secret key and the destination for uploaded photos. 
It also sets up a FlaskForm and UploadSet for handling photo uploads.
The application has three routes. the first route handles uploaded photos and saves them to a specified directory. 
The second route retrieves the uploaded photo from the specified directory and displays it. The third route is the home page.
When a photo is uploaded and submitted, the app first removes all previously uploaded files, saves the most recently uploaded file, and retrieves the uploaded image. 
The FER library is then used to recognize emotions in the image. The detected emotions are then returned to the user.
application server listens for incoming requests on port 8000.

The flask_uploads.py file is not only in the requirements.txt listed but also seperately in the Project because there wehere some manually changes done for the flask werkzeug library.
Otherwise it would not notice the manually change. Without the change the application is not working. The change was just a simple change with the import.

