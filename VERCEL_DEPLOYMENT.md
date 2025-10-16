# Vercel Deployment Guide

## 🚀 Deploy Marathi Font Converter to Vercel

This guide explains how to deploy the Marathi Font Converter to Vercel's serverless platform.

### 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Vercel CLI** (optional): `npm i -g vercel`

### 🔧 Vercel-Specific Changes

The following files have been created/modified for Vercel deployment:

- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless function entry point
- ✅ `api/templates/` - Templates for Vercel
- ✅ `static/` - Static assets
- ✅ `requirements-vercel.txt` - Simplified dependencies

### 🌐 Deploy Methods

#### Method 1: GitHub Integration (Recommended)

1. **Connect Repository**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Connect your GitHub account
   - Select `font-unicode` repository

2. **Configure Build**:
   - Framework Preset: "Other"
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements-vercel.txt`

3. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live at `https://your-project.vercel.app`

#### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to project directory
cd warje

# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name: font-unicode
# - Directory: ./
```

### ⚙️ Configuration

The `vercel.json` file configures:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "static/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ]
}
```

### 🔒 Environment Variables

If needed, add environment variables in Vercel dashboard:
- Go to Project Settings → Environment Variables
- Add any required variables

### 📝 Vercel Limitations

Due to Vercel's serverless nature, some features are simplified:

1. **File Formats**: Only TXT files supported (no DOCX/PDF processing)
2. **File Storage**: No persistent file storage (downloads are client-side)
3. **Processing Time**: 30-second timeout limit
4. **Memory**: Limited memory for large files

### 🔗 API Endpoints

Once deployed, your app will have these endpoints:

- `GET /` - Main web interface
- `POST /api/convert` - Text conversion API
- `POST /api/convert-file` - File conversion API
- `GET /api/font-info` - Font information API

### 🧪 Testing

After deployment, test your app:

1. **Web Interface**: Visit your Vercel URL
2. **Text Conversion**: Use the preview feature
3. **File Upload**: Upload a TXT file with Marathi text
4. **API Testing**: Use curl or Postman

```bash
# Test text conversion API
curl -X POST https://your-project.vercel.app/api/convert \
  -H "Content-Type: application/json" \
  -d '{"text": "your marathi text here"}'
```

### 🐛 Troubleshooting

**Common Issues:**

1. **Import Errors**: Ensure all imports are available in `requirements-vercel.txt`
2. **Timeout**: Large files may timeout (30s limit)
3. **Path Issues**: Check file paths in `vercel.json`

**Logs:**
- View deployment logs in Vercel dashboard
- Use `vercel logs` command for CLI

### 📈 Performance

**Optimizations for Vercel:**
- ✅ Minimal dependencies
- ✅ Serverless-optimized code
- ✅ Static asset optimization
- ✅ Client-side file downloads

### 🔄 Updates

To update your deployment:

1. **GitHub Integration**: Push to main branch (auto-deploys)
2. **CLI**: Run `vercel` command again

### 📞 Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **GitHub Issues**: Report issues in the repository
- **Community**: Vercel Discord/Forums

---

## 🎯 Quick Start

1. Push this repository to GitHub
2. Connect to Vercel
3. Deploy with one click
4. Your Marathi Font Converter is live! 🎉

**Full Feature Version**: For complete document support (DOCX, PDF), use the Docker deployment option.