from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import tempfile
import uuid
from werkzeug.utils import secure_filename
import sys
import base64
import io

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.converters.font_detector import FontDetector
from app.converters.font_mapper import FontMapper

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'vercel-deployment-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize converters
font_detector = FontDetector()
font_mapper = FontMapper()

@app.route('/')
def index():
    """Main page with file upload form"""
    return render_template('index.html')

@app.route('/api/convert', methods=['POST'])
def convert_text_api():
    """API endpoint for text conversion"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'success': False, 'message': 'No text provided'})
        
        # Detect fonts
        detection = font_detector.detect_fonts(text)
        
        # Convert text
        converted_text = font_mapper.convert_with_preservation(text)
        
        # Generate statistics
        stats = font_mapper.get_conversion_stats(text, converted_text)
        stats['detected_fonts'] = detection
        
        return jsonify({
            'success': True,
            'original': text,
            'converted': converted_text,
            'detected_fonts': detection,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error converting text: {str(e)}'
        })

@app.route('/api/convert-file', methods=['POST'])
def convert_file_api():
    """API endpoint for file conversion - simplified for Vercel"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        # Read file content as text (simplified for Vercel)
        try:
            if file.filename and file.filename.endswith('.txt'):
                content = file.read().decode('utf-8')
            else:
                return jsonify({
                    'success': False, 
                    'message': 'Only TXT files supported in Vercel deployment. For full document support, use the Docker deployment.'
                })
        except UnicodeDecodeError:
            return jsonify({'success': False, 'message': 'Unable to decode file. Please ensure it\'s a valid text file.'})
        
        # Detect and convert
        detection = font_detector.detect_fonts(content)
        converted_content = font_mapper.convert_with_preservation(content)
        
        # Generate statistics
        stats = font_mapper.get_conversion_stats(content, converted_content)
        stats['detected_fonts'] = detection
        
        return jsonify({
            'success': True,
            'original': content[:1000] + '...' if len(content) > 1000 else content,
            'converted': converted_content,
            'detected_fonts': detection,
            'stats': stats,
            'download_content': converted_content,
            'filename': f"converted_{file.filename}"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing file: {str(e)}'
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
        'formats': ['txt'],  # Limited in Vercel
        'deployment': 'vercel',
        'note': 'This is a simplified version for Vercel. For full document support (DOCX, PDF), use the Docker deployment.'
    })

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('../static', filename)

# Vercel expects the app to be available at the module level
def handler(event, context):
    """Vercel serverless function handler"""
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)