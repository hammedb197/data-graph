from myapp import app

from flask import render_template, redirect, request, url_for, flash
from werkzeug.utils import secure_filename
import os

from .services.extract_from_pdf import extract_text_from_pdf
from .services.doc import extract_text_from_doc 
from .services.ocr import extract_from_images

from .services.wiki import get_wiki_data
from .services.save_to_db import sendToNeo4j
from .services.nifi import send_topic

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/text', methods = ['POST'])
def get_data_from_wiki():
    # db = sendToNeo4j()
    if request.method == 'POST':
        if request.form['text'] == '':
            flash("Sorry, you have to fill a field")
            return redirect(url_for('home'))
        
        else:
            
            text = request.form['text']
            get_wiki_data(text) 
            # send_topic(text)
            return redirect(url_for('home'))
        
@app.route('/file', methods=['POST'])
def get_data_from_files():
    if request.method == 'POST':
        
        file = request.files['file']
        if allowed_file(file.filename):
            if file.filename.split('.')[-1] == 'pdf':
                filename = secure_filename(file.filename)
                file.save('upload/' + filename)    
                extract_text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('home'))
              
            
            elif file.filename.split('.')[-1] == 'doc' or file.filename.split('.')[-1] == 'docx' or file.filename.split('.')[-1] == 'txt':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                extract_text_from_doc(os.path.join(app.config['UPLOAD_FOLDER'], filename))                
                return redirect(url_for('home'))

            else:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                extract_from_images(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
        