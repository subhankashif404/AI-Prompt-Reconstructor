# 🚀 AI Prompt Reconstructor & Enhancer

**AI Prompt Reconstructor** is an advanced AI-powered tool that analyzes YouTube videos, extracts their transcripts, and reverse-engineers the prompt engineering behind the content. It generates high-quality prompts you can use with any LLM like ChatGPT, Claude, or Gemini.

---

## 🌟 Features

- 🎥 **YouTube Transcript Extraction** — Supports standard URLs, shortened links (`youtu.be`), and YouTube Shorts
- 🤖 **AI Prompt Reconstruction** — Intelligently analyzes video content to discover its underlying "prompt logic"
- ⚡ **Power Prompt Enhancement** — Generates supercharged prompt versions for maximum output quality
- 🔑 **Flexible API Configuration** — Persistent Gemini API key entry with real-time server-side validation
- 🔄 **Gemini REST Fallback** — Works even without the Gemini SDK installed
- 🎨 **Premium UI/UX** — Glassmorphic dashboard with smooth animations and responsive design

---

## 🛠️ Technology Stack

- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Flask (Python 3.11)
- **AI Engine**: Google Gemini 1.5 Flash (SDK + REST fallback)
- **YouTube**: `youtube-transcript-api`
- **Icons & Fonts**: FontAwesome, Google Fonts (Inter, JetBrains Mono)

---

## 🚀 Local Setup

```bash
git clone https://github.com/your-username/AI-Prompt-Reconstructor.git
cd AI-Prompt-Reconstructor
pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000** and optionally enter your Gemini API key to unlock the Pro Engine.

### Environment Variables (optional)

Create a `.env` file:

```env
GEMINI_API_KEY=your_key_here
```

---

## ☁️ Deploy to Vercel

### One-click deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/AI-Prompt-Reconstructor)

### Manual deploy

```bash
npm i -g vercel
vercel login
vercel --prod
```

Set your Gemini API key in the Vercel dashboard:
**Project → Settings → Environment Variables → Add `GEMINI_API_KEY`**

> **Note**: YouTube transcript fetching may occasionally be rate-limited in serverless environments.
> The built-in AI engine works without any API key.

---

## 🔄 GitHub Actions CI/CD

The `.github/workflows/deploy.yml` workflow automatically:
1. Runs smoke tests on every push / PR
2. Deploys to Vercel on every push to `main`/`master`

### Required GitHub Secrets

Go to **Repo → Settings → Secrets and variables → Actions** and add:

| Secret | How to get it |
|--------|--------------|
| `VERCEL_TOKEN` | [vercel.com/account/tokens](https://vercel.com/account/tokens) |
| `VERCEL_ORG_ID` | Run `vercel whoami` or check Project Settings |
| `VERCEL_PROJECT_ID` | Run `vercel link` in the project directory |

---

## 👨‍💻 Developed By

Developed with ❤️ by **Subhan Kashif**
