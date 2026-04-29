// YouTube Prompt Reconstructor - Clean JavaScript

// DOM Elements
const youtubeUrl = document.getElementById('youtubeUrl');
const analyzeBtn = document.getElementById('analyzeBtn');
const geminiApiKey = document.getElementById('geminiApiKey');
const verifyBtn = document.getElementById('verifyBtn');
const apiStatus = document.getElementById('apiStatus');
const videoSection = document.getElementById('videoSection');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');
const resultsSection = document.getElementById('resultsSection');

// Event Listeners
analyzeBtn.addEventListener('click', startAnalysis);
verifyBtn.addEventListener('click', verifyApiKey);

youtubeUrl.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startAnalysis();
});

geminiApiKey.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') verifyApiKey();
});

// Main Analysis Function
async function startAnalysis() {
    const url = youtubeUrl.value.trim();
    
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }

    // Show loading
    hideAll();
    loadingSection.style.display = 'block';
    analyzeBtn.disabled = true;

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                url: url,
                api_key: geminiApiKey.value.trim()
            })
        });

        const data = await response.json();

        if (data.success) {
            loadingSection.style.display = 'none';
            showVideoPreview(data.video_id);
            displayResults(data);
        } else {
            loadingSection.style.display = 'none';
            showError(data.error);
        }
    } catch (error) {
        loadingSection.style.display = 'none';
        showError('Network error. Please try again.');
        console.error('Error:', error);
    } finally {
        analyzeBtn.disabled = false;
    }
}

// Show Video Preview
function showVideoPreview(videoId) {
    videoSection.style.display = 'block';
    document.getElementById('videoThumbnail').src = `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;
    document.getElementById('videoId').textContent = `Video ID: ${videoId}`;
    document.getElementById('videoTitle').textContent = 'YouTube Video';
}

// Display Results
function displayResults(data) {
    resultsSection.style.display = 'flex';

    // Stats
    document.getElementById('transcriptLength').textContent = formatNumber(data.transcript_length);
    document.getElementById('segmentCount').textContent = data.segments || '—';
    document.getElementById('contentType').textContent = data.analysis.content_type || '—';
    document.getElementById('complexity').textContent = data.analysis.complexity || '—';

    // Topics
    const topics = data.analysis.main_topics || [];
    if (topics.length > 0) {
        document.getElementById('topicsSection').style.display = 'block';
        const topicsList = document.getElementById('topicsList');
        topicsList.innerHTML = '';
        topics.forEach(topic => {
            const tag = document.createElement('span');
            tag.className = 'topic-tag';
            tag.textContent = typeof topic === 'string' ? topic : topic.name;
            topicsList.appendChild(tag);
        });
    }

    // SEO Section
    if (data.seo_data) {
        displaySEOData(data.seo_data);
    }

    // Reconstructed Prompts
    const promptsContainer = document.getElementById('reconstructedPrompts');
    promptsContainer.innerHTML = '';
    data.reconstructed_prompts.forEach((prompt, index) => {
        promptsContainer.appendChild(createPromptCard(prompt, index, false));
    });

    // Enhanced Prompts
    const enhancedContainer = document.getElementById('enhancedPrompts');
    enhancedContainer.innerHTML = '';
    data.enhanced_prompts.forEach((prompt, index) => {
        enhancedContainer.appendChild(createPromptCard(prompt, index, true));
    });

    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 200);
}

// Create Prompt Card
function createPromptCard(prompt, index, isEnhanced) {
    const card = document.createElement('div');
    card.className = 'prompt-card';
    
    const id = `prompt-${index}`;
    const confidence = prompt.confidence || (isEnhanced ? 95 : 85);
    const text = isEnhanced ? prompt.enhanced : prompt.prompt;

    card.innerHTML = `
        <div class="prompt-header">
            <span class="prompt-type">${prompt.type}</span>
            <span class="prompt-confidence">${confidence}% Match</span>
        </div>
        <div class="prompt-text">${escapeHtml(text)}</div>
        <div class="prompt-actions">
            <button class="btn-copy" onclick="copyText(this, '${id}')">
                <i class="fas fa-copy"></i> Copy
            </button>
        </div>
        <textarea id="${id}" style="display:none">${escapeHtml(text)}</textarea>
    `;

    return card;
}

// Copy Text
function copyText(button, textId) {
    const textarea = document.getElementById(textId);
    if (!textarea) return;

    navigator.clipboard.writeText(textarea.value).then(() => {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Copied!';
        button.classList.add('copied');

        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        console.error('Copy error:', err);
    });
}

// Verify API Key
async function verifyApiKey() {
    const key = geminiApiKey.value.trim();
    
    if (!key) {
        apiStatus.textContent = 'Please enter an API key';
        apiStatus.className = 'api-status error';
        return;
    }

    verifyBtn.disabled = true;
    verifyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...';
    apiStatus.textContent = '';

    try {
        const response = await fetch('/validate_api_key', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: key })
        });

        const data = await response.json();

        if (data.success) {
            apiStatus.textContent = '✓ API key is valid and working!';
            apiStatus.className = 'api-status success';
            localStorage.setItem('gemini_api_key', key);
        } else {
            apiStatus.textContent = '✕ ' + data.error;
            apiStatus.className = 'api-status error';
        }
    } catch (error) {
        apiStatus.textContent = '✕ Network error';
        apiStatus.className = 'api-status error';
    } finally {
        verifyBtn.disabled = false;
        verifyBtn.innerHTML = '<i class="fas fa-check"></i> Verify';
    }
}

// Show Error
function showError(message) {
    errorSection.style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
}

// Hide All Sections
function hideAll() {
    videoSection.style.display = 'none';
    loadingSection.style.display = 'none';
    errorSection.style.display = 'none';
    resultsSection.style.display = 'none';
}

// Display SEO Data
function displaySEOData(seoData) {
    const seoSection = document.getElementById('seoSection');
    seoSection.style.display = 'block';

    // SEO Score
    const score = seoData.seo_score || 0;
    document.getElementById('seoScore').textContent = score + '/100';
    document.getElementById('seoBarFill').style.width = score + '%';

    // Title Suggestions
    const titlesContainer = document.getElementById('titleSuggestions');
    titlesContainer.innerHTML = '';
    if (seoData.title_suggestions && seoData.title_suggestions.length > 0) {
        seoData.title_suggestions.forEach(title => {
            const titleDiv = document.createElement('div');
            titleDiv.className = 'title-suggestion';
            titleDiv.innerHTML = `
                <span>${escapeHtml(title)}</span>
                <i class="fas fa-copy" style="color: var(--text-secondary);"></i>
            `;
            titleDiv.onclick = () => {
                navigator.clipboard.writeText(title);
                titleDiv.style.borderColor = 'var(--success)';
                setTimeout(() => {
                    titleDiv.style.borderColor = '';
                }, 1000);
            };
            titlesContainer.appendChild(titleDiv);
        });
    }

    // SEO Description
    if (seoData.seo_description) {
        document.getElementById('seoDescription').textContent = seoData.seo_description;
    }

    // Tags
    const tagsContainer = document.getElementById('tagsContainer');
    tagsContainer.innerHTML = '';
    if (seoData.tags && seoData.tags.length > 0) {
        seoData.tags.forEach(tag => {
            const tagDiv = document.createElement('span');
            tagDiv.className = 'tag';
            tagDiv.textContent = '#' + tag;
            tagsContainer.appendChild(tagDiv);
        });
    }

    // SEO Tips
    const tipsList = document.getElementById('seoTips');
    tipsList.innerHTML = '';
    if (seoData.seo_tips && seoData.seo_tips.length > 0) {
        seoData.seo_tips.forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            tipsList.appendChild(li);
        });
    }
}

// Copy Tags
function copyTags() {
    const tagsContainer = document.getElementById('tagsContainer');
    const tags = Array.from(tagsContainer.querySelectorAll('.tag'))
        .map(tag => tag.textContent)
        .join(', ');
    
    navigator.clipboard.writeText(tags).then(() => {
        // Show feedback
        const btn = event.target.closest('button');
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(() => {
            btn.innerHTML = originalHTML;
        }, 2000);
    });
}

// Copy Text (for description)
function copyText(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const text = element.textContent || element.value;
    navigator.clipboard.writeText(text).then(() => {
        // Find the button and show feedback
        const btn = element.parentElement.querySelector('.btn-copy');
        if (btn) {
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(() => {
                btn.innerHTML = originalHTML;
            }, 2000);
        }
    });
}

// Utility Functions
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
}

// Initialize on load
window.addEventListener('load', () => {
    const savedKey = localStorage.getItem('gemini_api_key');
    if (savedKey) {
        geminiApiKey.value = savedKey;
    }
    
    setTimeout(() => youtubeUrl.focus(), 500);
});
