# 🧠 YouTube Prompt Reconstructor

**YouTube Prompt Reconstructor** is an advanced, AI-powered tool that extracts, analyzes, and reconstructs prompts from any YouTube video. It provides SEO optimization, metadata generation, and prompt enhancement — helping content creators understand and recreate AI-generated content from videos.

---

## 🌟 Features

### 🎥 **Video Analysis**
- 📝 **Transcript Extraction**: Automatically fetches video transcripts/captions
- 🔍 **Content Analysis**: Detects topics, complexity, and content type
- 📊 **Statistics**: Word count, segments, and content metrics
- 🎬 **Video Preview**: Shows thumbnail and video information

### 🤖 **AI Prompt Reconstruction**
- 🧩 **Prompt Detection**: Identifies AI prompts used in videos
- 🎯 **Reconstructed Prompts**: Recreates original prompts with confidence scores
- 🚀 **Enhanced Prompts**: Improves prompts with best practices and structure
- 📈 **Multiple Prompts**: Extracts all detected prompts from a single video

### 🔍 **SEO & Metadata Optimization**
- 📊 **SEO Score**: 0-100 score with visual progress bar
- ✍️ **Title Suggestions**: 5 SEO-optimized title options (click to copy)
- 📝 **SEO Description**: Auto-generated YouTube description with formatting
- 🏷️ **Smart Tags**: Up to 30 relevant tags extracted from content
- 💡 **SEO Tips**: 6 actionable optimization recommendations

### ⚙️ **Advanced Features**
- 🔑 **Gemini API Integration**: Optional Google Gemini AI for enhanced analysis
- ✅ **API Key Verification**: One-click validation with clear status messages
- 🎨 **Dark Theme**: Professional black UI with YouTube red branding
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- 📋 **One-Click Copy**: Copy prompts, tags, descriptions instantly
- 💾 **Local Storage**: Saves API key for convenience

### 🔒 **Privacy & Performance**
- 🔐 **No Data Collection**: All processing happens on your device/server
- ⚡ **Fast Processing**: Quick transcript extraction and analysis
- 🌐 **Cloud Ready**: Deploy on Vercel, Heroku, or any cloud platform
- 🆓 **Free to Use**: Built-in AI engine works without API keys

---

## 🛠️ Technology Stack

### **Backend**
- **Framework**: Flask 3.0+ (Python)
- **AI Engine**: Built-in AI + Optional Google Gemini API
- **Transcript API**: youtube-transcript-api v1.x
- **HTTP Client**: requests with SSL/TLS support
- **Environment**: python-dotenv for configuration

### **Frontend**
- **Core**: Pure HTML5, CSS3, JavaScript (ES6+)
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Inter (Google Fonts)
- **UI Design**: Custom CSS with dark theme, modern cards, responsive layout
- **State Management**: Vanilla JavaScript with async/await

### **Deployment**
- **Server**: Gunicorn (production), Flask Dev Server (development)
- **Cloud**: Vercel, Heroku, Railway, Render, AWS
- **Hosting**: Any Python-compatible hosting platform

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** installed
- **Git** for cloning the repository
- **Modern Web Browser** (Chrome, Edge, Firefox, Safari)
- **Optional**: Google Gemini API key for enhanced AI features

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/subhankashif404/AI-Prompt-Reconstructor.git
cd AI-Prompt-Reconstructor
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Set up environment (optional):**
```bash
# Create .env file
cp .env.example .env

# Add your API keys (optional)
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

**4. Run the application:**
```bash
python app.py
```

**5. Access the app:**
```
Open http://localhost:5000 in your browser
```

---

## 📖 How to Use

### **Basic Usage**

1. **Enter YouTube URL**: Paste any YouTube video link
2. **Click Analyze**: Wait for transcript extraction and analysis
3. **View Results**: See prompts, topics, and statistics
4. **Copy Prompts**: Click copy buttons to save prompts

### **Advanced Usage with API Key**

1. **Get API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Enter Key**: Paste in the API key field
3. **Verify**: Click "Verify" button to validate the key
4. **Analyze**: Get enhanced AI-powered results

### **SEO Optimization**

1. **Analyze Video**: Enter URL and click Analyze
2. **Check SEO Score**: View the 0-100 optimization score
3. **Copy Titles**: Click any suggested title to copy
4. **Use Description**: Copy the formatted SEO description
5. **Add Tags**: Copy all recommended tags for YouTube

---

## 🎯 Use Cases

### **For Content Creators**
- 📝 Reverse-engineer AI prompts from successful videos
- 🔍 Analyze competitor content strategies
- 📊 Understand what prompts generate specific content
- 🚀 Improve your own prompt engineering skills

### **For Marketers**
- 🎯 Extract content frameworks from top videos
- 💡 Generate SEO-optimized titles and descriptions
- 🏷️ Get relevant tags for better discoverability
- 📈 Optimize video metadata for YouTube algorithm

### **For Learners**
- 📚 Understand AI prompt structures
- 🧠 Learn prompt engineering techniques
- 💡 Study how AI generates different content types
- 🎓 Practice with real-world examples

### **For Developers**
- 🔧 Integrate with your own applications
- 🌐 Deploy as a standalone service
- 📦 Use as a template for similar tools
- 🚀 Build on top of the existing codebase

---

## ⚙️ Configuration

### **Environment Variables**

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | No | None (uses built-in AI) |
| `SECRET_KEY` | Flask secret key | No | Auto-generated |
| `PORT` | Server port | No | 5000 |
| `FLASK_ENV` | Environment mode | No | development |

### **API Key Setup**

**Get Free Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Create new API key
4. Copy and paste in the app
5. Click "Verify" to test

**Enable Gemini API (if needed):**
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com)
2. Select your project
3. Click "Enable API"
4. Wait 1-2 minutes for propagation

---

### **Test URLs**
Try analyzing these types of videos:
- ✅ Tutorial videos (usually have captions)
- ✅ AI-generated content videos
- ✅ Educational content
- ✅ How-to guides
- ⚠️ Music videos (no transcripts)
- ⚠️ Videos without captions

---

## 📊 Project Structure

```
AI-Prompt-Reconstructor/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
├── Procfile              # Gunicorn server config
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── .vercelignore         # Vercel ignore rules
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # Custom CSS (dark theme)
│   └── script.js         # Frontend JavaScript
└── README.md             # This file
```

## 🔒 Privacy & Security

### **Data Storage**
- 📍 **Transcripts**: Processed in memory, not stored
- 📍 **API Keys**: Saved in browser localStorage (your device only)
- 📍 **Analysis Results**: Not stored on server
- 📍 **No Database**: Everything is stateless

### **Privacy Guarantee**
- ✅ No user data collection
- ✅ No analytics or tracking
- ✅ No cookies
- ✅ No account required
- ✅ Complete control over your data
- ✅ API keys stored locally only

### **Security Features**
- 🔐 SSL/TLS certificate support
- 🔐 Environment variable configuration
- 🔐 Secret key for Flask sessions
- 🔐 Input validation and sanitization

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### **Ideas for Contributions**
- 🌍 Multi-language support
- 🎨 More themes/customization
- 📊 Advanced analytics dashboard
- 🔌 API integrations (OpenAI, Claude, etc.)
- 📱 Mobile app version
- 🎙️ Voice input support
- 📥 Batch video analysis
- 🔄 Prompt versioning

---
## 📦 Testing

> 🧪 **Live Demo**: https://ai-prompt-reconstructor.vercel.app

---

## 👨‍💻 Developed By

**Developed with ❤️ by Subhan Kashif**

