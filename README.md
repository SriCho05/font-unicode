# Marathi Font Converter

A web-based intelligent document converter that detects and converts non-Unicode Marathi fonts (DVTT Yogesh / DTT Dhruv) to Unicode (Lohit Marathi) while preserving formatting, tables, and English text.

## Features

- **Font Detection**: Automatically detects DVTT Yogesh and DTT Dhruv fonts in documents
- **Smart Conversion**: Converts non-Unicode Marathi text to Unicode (Lohit Marathi) 
- **Format Preservation**: Maintains document formatting, tables, and English text
- **Multiple Formats**: Supports DOC, DOCX, PDF, and TXT files
- **Web Interface**: User-friendly web application for easy file upload and conversion
- **Preview Mode**: Before/after comparison of conversion results
- **Linux Optimized**: Designed for deployment on Linux servers

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap framework)
- **Document Processing**: python-docx, PyPDF2, openpyxl
- **Font Processing**: Custom mapping algorithms
- **Deployment**: Docker, Linux

## Installation

### Prerequisites

- Python 3.8+
- pip package manager
- Git

### Setup for Development

1. Clone/navigate to the repository:
```bash
cd warje
```

2. Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Linux
# OR
.\.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open browser and navigate to `http://localhost:5000`

## Docker Deployment (Linux)

### Build and Run with Docker

```bash
# Build the image
docker build -f Dockerfile.linux -t marathi-converter .

# Run the container
docker run -p 5000:5000 marathi-converter
```

### Using Docker Compose (Recommended)

```bash
# Start with nginx reverse proxy
docker-compose up -d

# Access at http://localhost
```

## Usage

1. **Upload Document**: Select your document file (TXT, DOC, DOCX, or PDF)
2. **Auto-Detection**: The system automatically detects non-Unicode Marathi fonts
3. **Preview Results**: View before/after comparison of the conversion
4. **Download**: Get your converted document with Unicode fonts

### Supported Input Formats
- **TXT**: Plain text files
- **DOCX**: Microsoft Word documents (recommended)
- **PDF**: Portable Document Format (converted to TXT output)
- **DOC**: Legacy Word format (limited support)

### Font Support
- **Input Fonts**: DVTT Yogesh, DTT Dhruv
- **Output Font**: Unicode Devanagari (Lohit Marathi compatible)

## API Endpoints

- `GET /` - Main application interface
- `POST /upload` - File upload and conversion
- `POST /preview` - Text preview conversion
- `GET /download/<filename>` - Download converted files
- `GET /api/font-info` - Font information and supported formats

## Features in Detail

### Smart Font Detection
- Automatically identifies non-Unicode Marathi fonts in text
- Distinguishes between DVTT Yogesh and DTT Dhruv character patterns
- Preserves English text and numbers during conversion

### Document Format Preservation
- **DOCX**: Maintains paragraphs, tables, and basic formatting
- **PDF**: Extracts text content (formatting limitations)
- **TXT**: Direct text conversion with encoding detection

### Web Interface
- Responsive design with Bootstrap framework
- Drag-and-drop file upload
- Real-time conversion progress
- Before/after text preview
- Conversion statistics

## Project Structure

```
warje/
├── app/
│   ├── converters/
│   │   ├── __init__.py
│   │   ├── font_detector.py      # Font detection algorithms
│   │   ├── font_mapper.py        # Character mapping tables
│   │   └── document_converter.py # Document processing
│   ├── static/
│   │   ├── css/style.css         # Custom styling
│   │   └── js/main.js           # Frontend JavaScript
│   ├── templates/
│   │   └── index.html           # Main interface
│   ├── uploads/                 # Temporary upload storage
│   └── downloads/               # Converted file storage
├── app.py                       # Flask application
├── requirements.txt             # Python dependencies
├── Dockerfile.linux            # Linux container image
├── docker-compose.yml          # Multi-container setup
├── nginx.conf                  # Reverse proxy config
└── README.md                   # This file
```

## Configuration

### Environment Variables
- `FLASK_ENV`: Set to 'production' for deployment
- `FLASK_APP`: Set to 'app.py'
- `PYTHONPATH`: Set to application root

### File Limits
- Maximum file size: 16MB
- Supported formats: TXT, PDF, DOC, DOCX
- Processing timeout: 60 seconds

## Development

### Running Tests
```bash
python test_converter.py
```

### Code Structure
- **FontDetector**: Identifies font types in text
- **FontMapper**: Converts between character encodings  
- **DocumentConverter**: Processes various file formats
- **Flask App**: Web interface and API endpoints

## Deployment

### Linux Production Deployment

1. **Using Docker Compose** (Recommended):
```bash
docker-compose up -d
```

2. **Manual Docker**:
```bash
docker build -f Dockerfile.linux -t marathi-converter .
docker run -d -p 5000:5000 marathi-converter
```

3. **Direct Python**:
```bash
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Nginx Configuration
The included `nginx.conf` provides:
- Reverse proxy to Flask application
- Static file serving
- File upload size limits
- Gzip compression

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please create an issue in the repository.

## Acknowledgments

- DVTT and DTT font specifications
- Unicode Consortium for Devanagari standards
- Flask and Python community
- Bootstrap for UI framework