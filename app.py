from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import pickle
import re
import os
import uuid
import PyPDF2
import docx2txt
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Load your saved models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

try:
    tfidf = pickle.load(open(os.path.join(MODELS_DIR, 'tfidf.pkl'), 'rb'))
    clf = pickle.load(open(os.path.join(MODELS_DIR, 'clf.pkl'), 'rb'))
    le = pickle.load(open(os.path.join(MODELS_DIR, 'encoder.pkl'), 'rb'))
    model_loaded = True
except Exception as e:
    print(f"Error loading models: {e}")
    model_loaded = False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    try:
        text = docx2txt.process(file_path)
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def extract_text_from_file(file_path):
    file_extension = file_path.rsplit('.', 1)[1].lower()
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in ['docx', 'doc']:
        return extract_text_from_docx(file_path)
    elif file_extension == 'txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    else:
        return ""

def cleanResume(txt):
    cleanTxt = re.sub('http\S+\s', ' ', txt)
    cleanTxt = re.sub('RT|CC', ' ', cleanTxt)
    cleanTxt = re.sub('#\S+\s', ' ', cleanTxt)
    cleanTxt = re.sub('@\S+', ' ', cleanTxt)
    cleanTxt = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_{|}~"""), ' ', cleanTxt)
    cleanTxt = re.sub('r[^\x00-\x7f]', ' ', cleanTxt)
    cleanTxt = re.sub('\s+', ' ', cleanTxt)
    return cleanTxt

def classify_text(resume_text):
    """Helper function to classify resume text"""
    if not resume_text:
        return None, "No text content found"
    
    try:
        # Clean the resume text
        cleaned_text = cleanResume(resume_text)
        
        # Vectorize
        vectorized_text = tfidf.transform([cleaned_text])
        if hasattr(vectorized_text, "toarray"):
            vectorized_text = vectorized_text.toarray()
        
        # Predict
        prediction = clf.predict(vectorized_text)
        category = le.inverse_transform(prediction)[0]
        
        return category, None
    except Exception as e:
        return None, f"Classification error: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html', model_status=model_loaded)

@app.route('/classify_form', methods=['POST'])
def classify_form():
    if not model_loaded:
        return render_template('index.html', 
                              model_status=model_loaded, 
                              error="Model files not found")
    
    # Check if the post request has the file part
    if 'resume_file' in request.files and request.files['resume_file'].filename != '':
        file = request.files['resume_file']
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload a PDF, DOCX, or TXT file.')
            return redirect(request.url)
        
        # Create unique filename to prevent overwriting
        unique_filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(file_path)
        
        # Extract text from file
        resume_text = extract_text_from_file(file_path)
        
        # Delete the file after processing
        try:
            os.remove(file_path)
        except:
            pass
        
    else:
        resume_text = request.form.get('resume_text', '')
    
    if not resume_text:
        flash('No text found. Please enter text or upload a valid document.')
        return redirect(url_for('home'))
    
    category, error = classify_text(resume_text)
    
    if error:
        flash(error)
        return redirect(url_for('home'))
    
    return render_template('result.html', 
                         category=category, 
                         resume_preview=resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)

@app.route('/classify', methods=['POST'])
def classify_resume():
    if not model_loaded:
        return jsonify({'error': 'Model files not found'}), 500
    
    data = request.get_json()
    resume_text = data.get('resume', '')
    
    if not resume_text:
        return jsonify({'error': 'No resume text provided'}), 400
    
    category, error = classify_text(resume_text)
    
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify({
        'category': category,
        'confidence': 'high'
    })

@app.route('/api-docs')
def api_docs():
    return render_template('api_docs.html')

@app.after_request
def add_header(response):
    """Add headers to avoid cache"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
