from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
import os
import tempfile
import shutil
from werkzeug.utils import secure_filename
from app.converters.font_detector import FontDetector
from app.converters.document_converter import DocumentConverter
from app.converters.font_mapper import FontMapper

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'app/uploads'
app.config['DOWNLOAD_FOLDER'] = 'app/downloads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize converters
font_detector = FontDetector()
font_mapper = FontMapper()
document_converter = DocumentConverter(font_detector, font_mapper)

@app.route('/')
def index():
    """Main page with file upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and conversion"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Create unique filename to avoid conflicts
        import uuid
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save uploaded file
        file.save(file_path)
        
        try:
            # Process the document
            result = document_converter.convert_document(file_path)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Document converted successfully',
                    'preview': result['preview'],
                    'download_url': url_for('download_file', filename=result['output_filename']),
                    'stats': result['stats']
                })
            else:
                return jsonify({
                    'success': False,
                    'message': result['error']
                })
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error processing document: {str(e)}'
            })
        
        finally:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
    
    else:
        flash('Invalid file type. Please upload DOC, DOCX, PDF, or TXT files.')
        return redirect(request.url)

@app.route('/download/<filename>')
def download_file(filename):
    """Download converted file"""
    file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('File not found')
        return redirect(url_for('index'))

@app.route('/preview', methods=['POST'])
def preview_conversion():
    """Preview conversion without downloading"""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'success': False, 'message': 'No text provided'})
    
    try:
        # Detect fonts in the text
        detected_fonts = font_detector.detect_fonts(text)
        
        # Convert text
        converted_text = font_mapper.convert_text(text)
        
        return jsonify({
            'success': True,
            'original': text,
            'converted': converted_text,
            'detected_fonts': detected_fonts
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error in preview: {str(e)}'
        })

@app.route('/api/font-info')
def font_info():
    """Get information about supported fonts"""
    return jsonify({
        'supported_fonts': [
            'DVTT Yogesh',
            'DTT Dhruv'
        ],
        'target_font': 'Lohit Marathi (Unicode)',
        'formats': list(ALLOWED_EXTENSIONS)
    })

if __name__ == '__main__':
    # Ensure upload and download directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)