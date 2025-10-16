// Main JavaScript for Marathi Font Converter

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const convertBtn = document.getElementById('convertBtn');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.querySelector('.progress-bar');
    const progressText = document.getElementById('progressText');
    const resultsContainer = document.getElementById('resultsContainer');
    const previewBtn = document.getElementById('previewBtn');
    const previewInput = document.getElementById('previewInput');
    const previewOutput = document.getElementById('previewOutput');

    // File upload and conversion
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            showAlert('Please select a file to upload.', 'warning');
            return;
        }

        // Validate file type
        const allowedTypes = ['text/plain'];
        if (!allowedTypes.includes(file.type) && !file.name.match(/\.(txt)$/i)) {
            showAlert('Please upload a valid text file (TXT only in Vercel deployment).', 'danger');
            return;
        }

        // Validate file size (16MB)
        if (file.size > 16 * 1024 * 1024) {
            showAlert('File size must be less than 16MB.', 'danger');
            return;
        }

        // Show progress
        showProgress();
        updateProgress(10, 'Uploading file...');

        // Prepare form data
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/convert-file', {
                method: 'POST',
                body: formData
            });

            updateProgress(50, 'Processing document...');

            const result = await response.json();

            updateProgress(90, 'Finalizing conversion...');

            if (result.success) {
                updateProgress(100, 'Conversion complete!');
                setTimeout(() => {
                    hideProgress();
                    showResults(result);
                }, 1000);
            } else {
                hideProgress();
                showAlert(result.message || 'Conversion failed. Please try again.', 'danger');
            }

        } catch (error) {
            hideProgress();
            showAlert('An error occurred during conversion. Please try again.', 'danger');
            console.error('Error:', error);
        }
    });

    // Text preview functionality
    previewBtn.addEventListener('click', async function() {
        const text = previewInput.value.trim();
        if (!text) {
            showAlert('Please enter some text to preview.', 'warning');
            return;
        }

        previewBtn.disabled = true;
        previewBtn.innerHTML = '<span class="loading-spinner"></span> Processing...';

        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            const result = await response.json();

            if (result.success) {
                previewOutput.innerHTML = `
                    <div class="row">
                        <div class="col-12">
                            <h6>Converted Text:</h6>
                            <div class="converted-font">${escapeHtml(result.converted)}</div>
                        </div>
                        <div class="col-12 mt-2">
                            <small class="text-muted">
                                Detected fonts: ${result.detected_fonts ? 
                                    Object.keys(result.detected_fonts)
                                        .filter(font => result.detected_fonts[font].detected)
                                        .join(', ') || 'None' 
                                    : 'None'}
                            </small>
                        </div>
                    </div>
                `;
            } else {
                previewOutput.innerHTML = `
                    <div class="alert alert-danger">
                        ${result.message || 'Preview failed'}
                    </div>
                `;
            }

        } catch (error) {
            previewOutput.innerHTML = `
                <div class="alert alert-danger">
                    Error generating preview. Please try again.
                </div>
            `;
            console.error('Preview error:', error);
        }

        previewBtn.disabled = false;
        previewBtn.innerHTML = '<i class="fas fa-eye"></i> Preview Conversion';
    });

    // Helper functions
    function showProgress() {
        progressContainer.style.display = 'block';
        resultsContainer.style.display = 'none';
        convertBtn.disabled = true;
        convertBtn.innerHTML = '<span class="loading-spinner"></span> Converting...';
    }

    function hideProgress() {
        progressContainer.style.display = 'none';
        convertBtn.disabled = false;
        convertBtn.innerHTML = '<i class="fas fa-exchange-alt"></i> Convert Document';
    }

    function updateProgress(percent, text) {
        progressBar.style.width = percent + '%';
        progressBar.setAttribute('aria-valuenow', percent);
        progressText.textContent = text;
    }

    function showResults(result) {
        resultsContainer.style.display = 'block';
        
        // Set download functionality for Vercel
        const downloadBtn = document.getElementById('downloadBtn');
        if (result.download_content && result.filename) {
            downloadBtn.onclick = function() {
                downloadTextFile(result.download_content, result.filename);
            };
            downloadBtn.style.display = 'inline-block';
        } else if (result.download_url) {
            downloadBtn.href = result.download_url;
            downloadBtn.style.display = 'inline-block';
        } else {
            downloadBtn.style.display = 'none';
        }

        // Show statistics
        const statsContainer = document.getElementById('conversionStats');
        const stats = result.stats;
        statsContainer.innerHTML = `
            <div class="row text-center">
                <div class="col-6">
                    <div class="stats-number">${stats.original_length || 0}</div>
                    <div class="stats-label">Original Characters</div>
                </div>
                <div class="col-6">
                    <div class="stats-number">${stats.converted_length || 0}</div>
                    <div class="stats-label">Converted Characters</div>
                </div>
            </div>
        `;

        // Show detected fonts
        const fontsContainer = document.getElementById('detectedFonts');
        const detectedFonts = stats.detected_fonts || {};
        const fontsList = Object.keys(detectedFonts)
            .filter(font => detectedFonts[font].detected)
            .map(font => `<span class="badge bg-primary me-1">${font}</span>`)
            .join('');
        
        fontsContainer.innerHTML = fontsList || '<span class="text-muted">No non-Unicode fonts detected</span>';

        // Show preview
        if (result.preview) {
            document.getElementById('originalPreview').textContent = result.preview.original || '';
            document.getElementById('convertedPreview').textContent = result.preview.converted || '';
        }
    }

    function showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert at the top of the card body
        const cardBody = document.querySelector('.card-body');
        cardBody.insertBefore(alertDiv, cardBody.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // File drag and drop functionality
    const formElement = uploadForm;
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        formElement.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        formElement.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        formElement.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        formElement.classList.add('dragover');
    }

    function unhighlight(e) {
        formElement.classList.remove('dragover');
    }

    formElement.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            fileInput.files = files;
            // Trigger file input change event
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    }

    // File input change handler
    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            // Show file info
            const fileInfo = `Selected: ${file.name} (${formatFileSize(file.size)})`;
            let fileInfoElement = document.getElementById('fileInfo');
            if (!fileInfoElement) {
                fileInfoElement = document.createElement('div');
                fileInfoElement.id = 'fileInfo';
                fileInfoElement.className = 'form-text text-success mt-1';
                this.parentNode.appendChild(fileInfoElement);
            }
            fileInfoElement.textContent = fileInfo;
        }
    });

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Download function for Vercel deployment
    function downloadTextFile(content, filename) {
        const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }

    // Load font information on page load
    loadFontInfo();

    async function loadFontInfo() {
        try {
            const response = await fetch('/api/font-info');
            const info = await response.json();
            console.log('Supported fonts:', info);
        } catch (error) {
            console.error('Error loading font info:', error);
        }
    }
});