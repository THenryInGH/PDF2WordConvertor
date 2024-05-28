from flask import Flask, request, send_file, render_template, redirect, url_for
import os
from pdf2docx import Converter

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return redirect(url_for('index'))
    
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return redirect(url_for('index'))
    
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(pdf_path)
    
    docx_filename = os.path.splitext(pdf_file.filename)[0] + '.docx'
    docx_path = os.path.join(CONVERTED_FOLDER, docx_filename)
    
    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()
    
    return send_file(docx_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
