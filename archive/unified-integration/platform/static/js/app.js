// Tab functionality
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        
        // Update active tab button
        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        // Update active tab content
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        document.getElementById(tabName).classList.add('active');
    });
});

// API base URL - use relative path to work with any host
const API_URL = '/api';

// Show loading
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

// Hide loading
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

// Show results
function showResults(data) {
    hideLoading();
    document.getElementById('results').style.display = 'block';
    
    // Show preview section for successful optimizations
    if (data.success && data.confidence > 0.7) {
        document.getElementById('preview-section').style.display = 'block';
    }
    
    // Set original prompt
    document.getElementById('original-prompt').textContent = data.original;
    
    // Set optimized prompt
    document.getElementById('optimized-prompt').textContent = data.optimized;
    
    // Set metadata
    if (data.confidence !== undefined) {
        let confidenceText = `${(data.confidence * 100).toFixed(1)}%`;
        if (data.ai_enhanced) {
            confidenceText += ` (AI Enhanced with ${data.service_used})`;
        }
        document.getElementById('confidence').textContent = confidenceText;
    }
    
    if (data.template_used) {
        document.getElementById('context-applied').textContent = data.template_used;
    } else if (data.cultural_context) {
        document.getElementById('context-applied').textContent = data.cultural_context;
    } else if (data.auto_detected_context) {
        document.getElementById('context-applied').textContent = data.auto_detected_context;
    }
    
    // Show AI suggestions if available
    if (data.ai_enhanced && data.ai_suggestions && data.ai_suggestions.length > 0) {
        let suggestionsHtml = '<div style="margin-top: 15px; padding: 15px; background: #1a1a1a; border-radius: 8px;">';
        suggestionsHtml += '<h4 style="color: #4ade80; margin-bottom: 10px;">🤖 AI Suggestions for Further Enhancement:</h4>';
        suggestionsHtml += '<ul style="margin: 0; padding-left: 20px;">';
        data.ai_suggestions.forEach(suggestion => {
            suggestionsHtml += `<li style="color: #888; margin-bottom: 5px;">${suggestion}</li>`;
        });
        suggestionsHtml += '</ul></div>';
        
        document.getElementById('optimized-prompt').innerHTML += suggestionsHtml;
    }
    
    // Show suggestions if available
    if (data.suggestions && data.suggestions.length > 0) {
        document.getElementById('suggestions').style.display = 'block';
        const suggestionsList = document.getElementById('suggestions-list');
        suggestionsList.innerHTML = '';
        
        data.suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            if (typeof suggestion === 'object') {
                li.innerHTML = `<strong>${suggestion.issue}:</strong> ${suggestion.suggestion}`;
            } else {
                li.textContent = suggestion;
            }
            suggestionsList.appendChild(li);
        });
    } else {
        document.getElementById('suggestions').style.display = 'none';
    }
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show variations
function showVariations(variations) {
    if (variations && variations.length > 0) {
        document.getElementById('variations').style.display = 'block';
        const variationsList = document.getElementById('variations-list');
        variationsList.innerHTML = '';
        
        variations.forEach((variation, index) => {
            const div = document.createElement('div');
            div.className = 'variation-item';
            div.innerHTML = `
                <div class="variation-number">Variation ${index + 1}</div>
                <p class="prompt-text">${variation}</p>
                <button class="copy-btn" onclick="copyText('${variation.replace(/'/g, "\\'")}')">Copy</button>
            `;
            variationsList.appendChild(div);
        });
    } else {
        document.getElementById('variations').style.display = 'none';
    }
}

// Optimize prompt
async function optimizePrompt() {
    const prompt = document.getElementById('optimize-prompt').value.trim();
    if (!prompt) {
        alert('Please enter a prompt to optimize');
        return;
    }
    
    const context = document.getElementById('optimize-context').value;
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/optimize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                type: 'standard',
                theme: context
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResults(data);
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
            hideLoading();
        }
    } catch (error) {
        alert('Error: ' + error.message);
        hideLoading();
    }
}

// Elaborate prompt
async function elaboratePrompt() {
    const prompt = document.getElementById('elaborate-prompt').value.trim();
    if (!prompt) {
        alert('Please enter a theme to elaborate');
        return;
    }
    
    const theme = document.getElementById('elaborate-theme').value;
    const depth = document.getElementById('elaborate-depth').value;
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/optimize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                type: 'elaborate',
                theme: theme,
                depth: depth
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResults(data);
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
            hideLoading();
        }
    } catch (error) {
        alert('Error: ' + error.message);
        hideLoading();
    }
}

// Show generation feedback
function showGenFeedback(icon, text) {
    const feedbackEl = document.getElementById('generate-feedback');
    const feedbackItem = feedbackEl.querySelector('.feedback-item');
    feedbackItem.querySelector('.feedback-icon').textContent = icon;
    feedbackItem.querySelector('.feedback-text').textContent = text;
    feedbackEl.style.display = 'block';
}

// Hide generation feedback
function hideGenFeedback() {
    document.getElementById('generate-feedback').style.display = 'none';
}

// Update live preview
function updateGeneratePreview() {
    const subject = document.getElementById('generate-subject').value.trim();
    const action = document.getElementById('generate-action').value.trim();
    const setting = document.getElementById('generate-setting').value.trim();
    
    if (subject || action || setting) {
        const preview = document.getElementById('generate-preview');
        const previewText = document.getElementById('preview-text');
        
        let text = '';
        if (subject) text += subject;
        if (action) text += (text ? ' ' : '') + action;
        if (setting) text += (text ? ' in ' : '') + setting;
        
        previewText.textContent = text || 'Start typing to see preview...';
        preview.style.display = 'block';
        
        // Show suggestions based on input
        showGenerateSuggestions(subject, action, setting);
    } else {
        document.getElementById('generate-preview').style.display = 'none';
        document.getElementById('generate-suggestions').style.display = 'none';
    }
}

// Show context-aware suggestions
function showGenerateSuggestions(subject, action, setting) {
    const suggestionsBox = document.getElementById('generate-suggestions');
    const chipsContainer = suggestionsBox.querySelector('.suggestion-chips');
    
    let suggestions = [];
    
    // Smart suggestions based on input
    if (subject && subject.includes('couple')) {
        suggestions = ['romantic moment', 'tender embrace', 'sunset scene', 'intimate conversation'];
    } else if (subject && subject.includes('people')) {
        suggestions = ['group interaction', 'celebration', 'deep conversation', 'shared experience'];
    } else if (!action) {
        suggestions = ['walking gracefully', 'contemplating quietly', 'interacting naturally', 'expressing emotion'];
    } else if (!setting) {
        suggestions = ['cozy interior', 'natural landscape', 'urban environment', 'abstract space'];
    }
    
    if (suggestions.length > 0) {
        chipsContainer.innerHTML = suggestions.map(s => 
            `<span class="suggestion-chip" onclick="applySuggestion('${s}')">${s}</span>`
        ).join('');
        suggestionsBox.style.display = 'block';
    }
}

// Apply suggestion to appropriate field
function applySuggestion(suggestion) {
    const action = document.getElementById('generate-action');
    const setting = document.getElementById('generate-setting');
    
    if (!action.value && (suggestion.includes('ing') || suggestion.includes('moment'))) {
        action.value = suggestion;
    } else if (!setting.value && (suggestion.includes('interior') || suggestion.includes('landscape') || suggestion.includes('environment'))) {
        setting.value = suggestion;
    }
    
    updateGeneratePreview();
}

// Generate prompt with smart optimization
async function generatePrompt() {
    const subject = document.getElementById('generate-subject').value.trim();
    if (!subject) {
        showGenFeedback('❌', 'Please enter at least a subject');
        setTimeout(hideGenFeedback, 3000);
        return;
    }
    
    const formData = {
        prompt: subject,  // Add the required prompt field
        subject: subject,
        action: document.getElementById('generate-action').value.trim(),
        setting: document.getElementById('generate-setting').value.trim(),
        camera: document.getElementById('generate-camera').value,
        style: document.getElementById('generate-style').value,
        variations: parseInt(document.getElementById('generate-variations').value)
    };
    
    // Disable button and show progress
    const btn = event.target.closest('button');
    const btnText = btn.querySelector('#gen-btn-text');
    const originalText = btnText.textContent;
    btn.disabled = true;
    
    // Step 1: Generating base prompt
    showGenFeedback('🎨', 'Generating creative prompt...');
    btnText.textContent = 'Generating...';
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Step 2: Optimizing with AI
            showGenFeedback('🧠', 'Applying Claude AI optimization...');
            btnText.textContent = 'Optimizing...';
            
            // Use Claude enhancement for maximum quality
            const optimizeResponse = await fetch(`${API_URL}/claude-enhance`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    prompt: data.prompt,
                    mode: 'comprehensive'  // Full Claude AI enhancement
                })
            });
            
            const optimizeData = await optimizeResponse.json();
            
            if (optimizeData.success) {
                // Success!
                showGenFeedback('✅', 'Generation complete!');
                btnText.textContent = 'Complete!';
                
                // Show super smart results
                showSuperResults({
                    ...optimizeData,
                    original: `Generated: ${data.prompt}`,
                    generated_variations: data.variations  // Keep original variations
                });
                
                // Reset button
                setTimeout(() => {
                    btn.disabled = false;
                    btnText.textContent = originalText;
                    hideGenFeedback();
                }, 2000);
                
                // Also optimize variations if they exist
                if (data.variations && data.variations.length > 0) {
                    const optimizedVariations = [];
                    for (const variation of data.variations) {
                        try {
                            const varResponse = await fetch(`${API_URL}/unified-optimize`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({ 
                                    prompt: variation,
                                    strategy: 'adaptive'
                                })
                            });
                            const varData = await varResponse.json();
                            if (varData.success) {
                                optimizedVariations.push(varData.optimized);
                            }
                        } catch (e) {
                            console.error('Error optimizing variation:', e);
                        }
                    }
                    if (optimizedVariations.length > 0) {
                        showVariations(optimizedVariations);
                    }
                }
            } else {
                // Fallback to showing just generated prompt
                showGenFeedback('⚠️', 'Using basic optimization (Claude unavailable)');
                btnText.textContent = 'Optimizing...';
                
                showResults({
                    original: `Subject: ${subject}`,
                    optimized: data.prompt,
                    confidence: 0.9,
                    template_used: 'Generated Prompt'
                });
                showVariations(data.variations);
                
                // Reset button
                setTimeout(() => {
                    btn.disabled = false;
                    btnText.textContent = originalText;
                    hideGenFeedback();
                }, 2000);
            }
        } else {
            showGenFeedback('❌', 'Generation failed: ' + (data.error || 'Unknown error'));
            btn.disabled = false;
            btnText.textContent = originalText;
            hideLoading();
        }
    } catch (error) {
        showGenFeedback('❌', 'Error: ' + error.message);
        btn.disabled = false;
        btnText.textContent = originalText;
        hideLoading();
    }
}

// Copy to clipboard
function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).textContent;
    copyText(text);
}

function copyText(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show feedback
        const button = event.target;
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.style.background = '#4ade80';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '';
        }, 2000);
    }).catch(err => {
        alert('Failed to copy text');
    });
}

// Auto-resize textareas
document.querySelectorAll('textarea').forEach(textarea => {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});

// Auto-optimize function
async function autoOptimize() {
    const prompt = document.getElementById('auto-prompt').value.trim();
    if (!prompt) {
        alert('Please enter a prompt to analyze and optimize');
        return;
    }
    
    showLoading();
    
    try {
        // First analyze the prompt
        const analysisResponse = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt })
        });
        
        const analysisData = await analysisResponse.json();
        
        if (analysisData.success) {
            // Show analysis preview
            showAnalysisPreview(analysisData.analysis);
            
            // Auto-optimize
            const optimizeResponse = await fetch(`${API_URL}/auto-optimize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt })
            });
            
            const optimizeData = await optimizeResponse.json();
            
            if (optimizeData.success) {
                // Add analysis info to results
                optimizeData.analysis_info = analysisData.analysis;
                showResults(optimizeData);
            } else {
                alert('Error: ' + (optimizeData.error || 'Unknown error'));
                hideLoading();
            }
        } else {
            alert('Error: ' + (analysisData.error || 'Unknown error'));
            hideLoading();
        }
    } catch (error) {
        alert('Error: ' + error.message);
        hideLoading();
    }
}

// Show analysis preview
function showAnalysisPreview(analysis) {
    const preview = document.getElementById('analysis-preview');
    const content = document.getElementById('analysis-content');
    
    // Build analysis HTML
    let html = '<div class="analysis-grid">';
    
    // Detected themes
    html += '<div class="analysis-item">';
    html += '<span class="analysis-label">Detected Themes:</span>';
    html += '<span class="analysis-value">';
    if (analysis.detected_themes.length > 0) {
        analysis.detected_themes.forEach(theme => {
            html += `<span class="theme-tag">${theme.replace(/_/g, ' ')}</span>`;
        });
    } else {
        html += 'None detected';
    }
    html += '</span></div>';
    
    // Sensitivity level
    html += '<div class="analysis-item">';
    html += '<span class="analysis-label">Sensitivity Level:</span>';
    html += `<span class="analysis-value sensitivity-${analysis.sensitivity_level}">${analysis.sensitivity_level.toUpperCase()}</span>`;
    html += '</div>';
    
    // Recommended strategy
    html += '<div class="analysis-item">';
    html += '<span class="analysis-label">Strategy:</span>';
    html += `<span class="analysis-value">${analysis.recommended_strategy.replace(/_/g, ' ')}</span>`;
    html += '</div>';
    
    // Auto-detected context
    html += '<div class="analysis-item">';
    html += '<span class="analysis-label">Auto Context:</span>';
    html += `<span class="analysis-value">${analysis.auto_context}</span>`;
    html += '</div>';
    
    // Recommendations
    if (analysis.recommendations.length > 0) {
        html += '<div class="analysis-item" style="flex-direction: column; align-items: flex-start;">';
        html += '<span class="analysis-label" style="margin-bottom: 8px;">Recommendations:</span>';
        html += '<ul style="margin: 0; padding-left: 20px; color: #888;">';
        analysis.recommendations.forEach(rec => {
            html += `<li style="margin-bottom: 4px;">${rec}</li>`;
        });
        html += '</ul></div>';
    }
    
    html += '</div>';
    
    content.innerHTML = html;
    preview.style.display = 'block';
}

// Simulate video generation
function simulateGeneration() {
    const button = event.target;
    const originalText = button.textContent;
    const previewContent = document.getElementById('preview-content');
    
    // Show loading state
    button.textContent = 'Generating...';
    button.disabled = true;
    previewContent.innerHTML = '<div class="spinner"></div><p>Simulating video generation...</p>';
    
    // Get the optimized prompt
    const prompt = document.getElementById('optimized-prompt').textContent;
    
    // Simulate API call
    setTimeout(() => {
        // Show simulated result
        previewContent.innerHTML = `
            <div class="video-placeholder">
                <div class="play-icon">▶</div>
            </div>
        `;
        
        // Add metadata
        const metadata = document.createElement('div');
        metadata.style.marginTop = '20px';
        metadata.innerHTML = `
            <p><strong>Prompt used:</strong> ${prompt.substring(0, 100)}...</p>
            <p><strong>Duration:</strong> 5 seconds</p>
            <p><strong>Resolution:</strong> 1920x1080</p>
            <p><strong>Status:</strong> <span style="color: #4ade80;">Ready (Simulated)</span></p>
            <br>
            <p style="color: #888; font-size: 0.9em;">
                Note: This is a simulation. When Sora API becomes available, 
                real videos will be generated here using your optimized prompts.
            </p>
        `;
        previewContent.appendChild(metadata);
        
        // Reset button
        button.textContent = 'Simulate Again';
        button.disabled = false;
    }, 3000);
}

// Start auto-improvement mode
async function startInteractiveMode() {
    const prompt = document.getElementById('auto-prompt').value.trim();
    if (!prompt) {
        alert('Please enter a prompt to improve');
        return;
    }
    
    showLoading();
    
    try {
        // Get smart questions
        const response = await fetch(`${API_URL}/get-questions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt })
        });
        
        const data = await response.json();
        
        if (data.success && data.questions.length > 0) {
            // Auto-apply improvements with default answers
            let improvedPrompt = prompt;
            
            for (const question of data.questions) {
                // Use the first option as default answer, or generate a sensible default
                let defaultAnswer = '';
                
                if (question.options && question.options.length > 0) {
                    // For multiple choice, pick the most cinematic/dramatic option
                    if (question.category === 'visual_details' && question.question.includes('time of day')) {
                        defaultAnswer = question.options.find(opt => opt.includes('Golden Hour') || opt.includes('Sunset')) || question.options[0];
                    } else if (question.category === 'emotional_tone') {
                        defaultAnswer = question.options.find(opt => opt.includes('Dramatic') || opt.includes('Romantic')) || question.options[0];
                    } else if (question.category === 'artistic_style') {
                        defaultAnswer = question.options.find(opt => opt.includes('Cinematic')) || question.options[0];
                    } else {
                        defaultAnswer = question.options[0];
                    }
                } else {
                    // For open-ended questions, provide smart defaults
                    if (question.category === 'narrative_elements') {
                        defaultAnswer = 'capturing a pivotal emotional moment';
                    } else {
                        defaultAnswer = 'with professional quality';
                    }
                }
                
                // Apply the answer
                try {
                    const applyResponse = await fetch(`${API_URL}/apply-answer`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            prompt: improvedPrompt,
                            question: question,
                            answer: defaultAnswer
                        })
                    });
                    
                    const applyData = await applyResponse.json();
                    if (applyData.success) {
                        improvedPrompt = applyData.improved_prompt;
                    }
                } catch (e) {
                    console.error('Error applying answer:', e);
                }
            }
            
            // Now optimize the improved prompt
            const optimizeResponse = await fetch(`${API_URL}/unified-optimize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    prompt: improvedPrompt,
                    strategy: 'adaptive'
                })
            });
            
            const optimizeData = await optimizeResponse.json();
            
            if (optimizeData.success) {
                // Show results with auto-improvement info
                showSuperResults({
                    ...optimizeData,
                    original: prompt,
                    auto_improvements: {
                        questions_answered: data.questions.length,
                        improvements_applied: data.questions.map((q, i) => ({
                            question: q.question,
                            answer: q.options ? q.options[0] : 'auto-generated'
                        }))
                    }
                });
            } else {
                hideLoading();
                alert('Optimization failed');
            }
        } else {
            // No improvements needed, just optimize
            hideLoading();
            superOptimize();
        }
    } catch (error) {
        hideLoading();
        alert('Error: ' + error.message);
    }
}

// Show questions dialog
function showQuestionsDialog(prompt, questions, suggestions) {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'questions-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    `;
    
    // Create dialog
    const dialog = document.createElement('div');
    dialog.className = 'questions-dialog';
    dialog.style.cssText = `
        background: #1a1a1a;
        border-radius: 12px;
        padding: 30px;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        position: relative;
    `;
    
    // Create content
    let html = `
        <h2 style="color: #fff; margin-bottom: 10px;">💬 Let's Improve Your Prompt</h2>
        <p style="color: #888; margin-bottom: 20px;">Answer these questions to add missing details:</p>
        
        <div id="questions-container">
    `;
    
    // Add questions
    questions.forEach((question, index) => {
        html += `
            <div class="question-item" style="margin-bottom: 25px; padding: 20px; background: #0a0a0a; border-radius: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                    <h4 style="color: #4ade80; margin: 0;">${question.question}</h4>
                    <span style="color: #666; font-size: 0.8em;">${question.category.replace(/_/g, ' ')}</span>
                </div>
                <p style="color: #666; font-size: 0.9em; margin-bottom: 10px;">${question.why_asking}</p>
        `;
        
        if (question.options && question.options.length > 0) {
            // Multiple choice
            html += '<div style="display: flex; flex-wrap: wrap; gap: 10px;">';
            question.options.forEach(option => {
                html += `
                    <label style="display: flex; align-items: center; cursor: pointer;">
                        <input type="radio" name="question_${index}" value="${option}" style="margin-right: 8px;">
                        <span style="color: #ccc;">${option}</span>
                    </label>
                `;
            });
            html += '</div>';
        } else {
            // Text input
            html += `<input type="text" id="answer_${index}" style="width: 100%; padding: 10px; background: #222; border: 1px solid #444; border-radius: 4px; color: #fff;">`;
        }
        
        html += `
                <p style="color: #666; font-size: 0.8em; margin-top: 10px;">Impact: ${question.impact}</p>
            </div>
        `;
    });
    
    // Add suggestions if available
    if (suggestions && suggestions.length > 0) {
        html += `
            <div style="margin-top: 20px; padding: 15px; background: #0a0a0a; border-radius: 8px;">
                <h4 style="color: #fbbf24; margin-bottom: 10px;">💡 Additional Suggestions:</h4>
                <ul style="margin: 0; padding-left: 20px;">
        `;
        suggestions.forEach(suggestion => {
            html += `<li style="color: #888; margin-bottom: 5px;">${suggestion}</li>`;
        });
        html += '</ul></div>';
    }
    
    html += `
        </div>
        
        <div style="display: flex; gap: 10px; margin-top: 25px;">
            <button onclick="applyInteractiveAnswers('${prompt.replace(/'/g, "\\'")}')" style="flex: 1; padding: 12px; background: #4ade80; color: #000; border: none; border-radius: 6px; font-weight: 600; cursor: pointer;">
                Apply Improvements
            </button>
            <button onclick="closeQuestionsDialog()" style="padding: 12px 20px; background: #444; color: #fff; border: none; border-radius: 6px; cursor: pointer;">
                Cancel
            </button>
        </div>
    `;
    
    dialog.innerHTML = html;
    overlay.appendChild(dialog);
    document.body.appendChild(overlay);
    
    // Store questions data for later use
    window.currentQuestions = questions;
}

// Close questions dialog
function closeQuestionsDialog() {
    const overlay = document.querySelector('.questions-overlay');
    if (overlay) {
        overlay.remove();
    }
    window.currentQuestions = null;
}

// Apply interactive answers
async function applyInteractiveAnswers(originalPrompt) {
    const questions = window.currentQuestions;
    if (!questions) return;
    
    let improvedPrompt = originalPrompt;
    
    // Process each question
    for (let i = 0; i < questions.length; i++) {
        const question = questions[i];
        let answer = '';
        
        if (question.options && question.options.length > 0) {
            // Get selected radio button
            const selected = document.querySelector(`input[name="question_${i}"]:checked`);
            if (selected) {
                answer = selected.value;
            }
        } else {
            // Get text input
            const input = document.getElementById(`answer_${i}`);
            if (input && input.value.trim()) {
                answer = input.value.trim();
            }
        }
        
        if (answer) {
            try {
                const response = await fetch(`${API_URL}/apply-answer`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: improvedPrompt,
                        question: question,
                        answer: answer
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    improvedPrompt = data.improved_prompt;
                }
            } catch (error) {
                console.error('Error applying answer:', error);
            }
        }
    }
    
    // Close dialog
    closeQuestionsDialog();
    
    // Update the prompt input with improved version
    document.getElementById('auto-prompt').value = improvedPrompt;
    
    // Auto-resize the textarea
    const textarea = document.getElementById('auto-prompt');
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
    
    // Show success message
    const successMsg = document.createElement('div');
    successMsg.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4ade80;
        color: #000;
        padding: 15px 20px;
        border-radius: 8px;
        font-weight: 600;
        z-index: 1001;
        animation: slideIn 0.3s ease-out;
    `;
    successMsg.textContent = '✓ Prompt improved! Click "Analyze & Auto-Optimize" to see the results.';
    document.body.appendChild(successMsg);
    
    // Remove success message after 3 seconds
    setTimeout(() => {
        successMsg.remove();
    }, 3000);
}

// Smart Optimize function
async function smartOptimize() {
    const prompt = document.getElementById('auto-prompt').value.trim();
    if (!prompt) {
        alert('Please enter a prompt to optimize');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/smart-optimize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show enhanced results with smart optimization details
            showSmartResults(data);
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
            hideLoading();
        }
    } catch (error) {
        alert('Error: ' + error.message);
        hideLoading();
    }
}

// Show smart optimization results
function showSmartResults(data) {
    hideLoading();
    document.getElementById('results').style.display = 'block';
    
    // Set original prompt
    document.getElementById('original-prompt').textContent = data.original;
    
    // Set optimized prompt
    document.getElementById('optimized-prompt').textContent = data.optimized;
    
    // Show scores
    const confidenceEl = document.getElementById('confidence');
    confidenceEl.innerHTML = `
        Overall: ${(data.confidence_score * 100).toFixed(1)}%<br>
        <span style="font-size: 0.9em; color: #888;">
            Semantic: ${(data.semantic_score * 100).toFixed(0)}% | 
            Style: ${(data.style_score * 100).toFixed(0)}%
        </span>
    `;
    
    // Show optimization profile
    document.getElementById('context-applied').innerHTML = `
        Smart AI Mode: ${data.optimization_mode}<br>
        <span style="font-size: 0.9em; color: #888;">
            Transformations: ${data.transformations.length} stages applied
        </span>
    `;
    
    // Show alternatives if available
    if (data.alternatives && data.alternatives.length > 0) {
        showVariations(data.alternatives);
    }
    
    // Show patterns detected
    if (data.patterns_detected && data.patterns_detected.length > 0) {
        const patternsHtml = `
            <div style="margin-top: 15px; padding: 15px; background: #1a1a1a; border-radius: 8px;">
                <h4 style="color: #9333ea; margin-bottom: 10px;">🧠 Smart AI Analysis:</h4>
                <p style="color: #888; margin-bottom: 10px;">Patterns detected and enhanced:</p>
                <ul style="margin: 0; padding-left: 20px; color: #888;">
                    ${data.patterns_detected.map(p => 
                        `<li style="margin-bottom: 5px;">${p.type}: "${p.match}" (${(p.confidence * 100).toFixed(0)}% confidence)</li>`
                    ).join('')}
                </ul>
                <p style="margin-top: 10px; color: #666; font-size: 0.9em;">
                    Transformations applied: ${data.transformations.join(' → ')}
                </p>
            </div>
        `;
        document.getElementById('optimized-prompt').innerHTML += patternsHtml;
    } else {
        // No patterns, show transformations
        const transformHtml = `
            <div style="margin-top: 15px; padding: 15px; background: #1a1a1a; border-radius: 8px;">
                <h4 style="color: #9333ea; margin-bottom: 10px;">🧠 Smart AI Enhancements:</h4>
                <p style="color: #888;">Multi-stage optimization pipeline applied:</p>
                <p style="margin-top: 10px; color: #666; font-size: 0.9em;">
                    ${data.transformations.join(' → ')}
                </p>
            </div>
        `;
        document.getElementById('optimized-prompt').innerHTML += transformHtml;
    }
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Super Smart Optimize - combines both approaches
async function superOptimize() {
    const prompt = document.getElementById('auto-prompt').value.trim();
    if (!prompt) {
        alert('Please enter a prompt to optimize');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/unified-optimize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                prompt: prompt,
                strategy: 'adaptive'  // Let the system choose the best approach
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show enhanced results with unified optimization
            showSuperResults(data);
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
            hideLoading();
        }
    } catch (error) {
        alert('Error: ' + error.message);
        hideLoading();
    }
}

// Show super optimization results
function showSuperResults(data) {
    hideLoading();
    document.getElementById('results').style.display = 'block';
    
    // Set original prompt
    document.getElementById('original-prompt').textContent = data.original;
    
    // Set optimized prompt
    document.getElementById('optimized-prompt').textContent = data.optimized;
    
    // Show comprehensive scores
    const confidenceEl = document.getElementById('confidence');
    const unifiedScore = data.scores?.unified_confidence || data.unified_score || 0.85;
    const safetyScore = data.scores?.safety_score || data.safety_score;
    const qualityScore = data.scores?.quality_score || data.quality_score;
    
    let scoreHtml = `Overall: ${(unifiedScore * 100).toFixed(1)}%`;
    
    if (safetyScore !== undefined && qualityScore !== undefined) {
        scoreHtml += `<br><span style="font-size: 0.9em; color: #888;">`;
        scoreHtml += `Safety: ${(safetyScore * 100).toFixed(0)}% | `;
        scoreHtml += `Quality: ${(qualityScore * 100).toFixed(0)}%`;
        scoreHtml += `</span>`;
    }
    
    confidenceEl.innerHTML = scoreHtml;
    
    // Show optimization strategy used
    document.getElementById('context-applied').innerHTML = `
        Strategy: ${data.strategy_used || 'Adaptive'}<br>
        <span style="font-size: 0.9em; color: #888;">
            ${data.guideline_handling ? '✓ Guideline-safe' : ''} 
            ${data.ai_enhanced ? '✓ AI-enhanced' : ''}
        </span>
    `;
    
    // Show alternatives if available
    if (data.alternatives && data.alternatives.length > 0) {
        showVariations(data.alternatives.map(alt => 
            typeof alt === 'string' ? alt : alt.prompt
        ));
    }
    
    // Show comprehensive analysis
    let analysisHtml = '<div style="margin-top: 15px; padding: 15px; background: #1a1a1a; border-radius: 8px;">';
    
    // Check if Claude AI was used
    if (data.ai_enhanced && data.service_used === 'Claude AI') {
        analysisHtml += '<h4 style="color: #10b981; margin-bottom: 10px;">🧠 Claude AI Enhanced Analysis:</h4>';
        
        // Show Claude insights if available
        if (data.claude_insights) {
            if (data.claude_insights.themes) {
                analysisHtml += '<p style="color: #4ade80; margin-bottom: 5px;">Detected themes:</p>';
                analysisHtml += '<p style="color: #888; margin: 0 0 10px 20px; font-size: 0.9em;">' + data.claude_insights.themes.join(', ') + '</p>';
            }
            if (data.claude_insights.enhancements) {
                analysisHtml += '<p style="color: #4ade80; margin-bottom: 5px;">AI enhancements applied:</p>';
                analysisHtml += '<ul style="margin: 0 0 10px 20px; color: #888; font-size: 0.9em;">';
                data.claude_insights.enhancements.forEach(enh => {
                    analysisHtml += `<li>${enh}</li>`;
                });
                analysisHtml += '</ul>';
            }
        }
        
        // Show creativity score if available
        if (data.scores && data.scores.creativity_score) {
            analysisHtml += '<p style="color: #9333ea; margin-top: 10px;">Creativity Score: ' + (data.scores.creativity_score * 100).toFixed(0) + '%</p>';
        }
    } else {
        analysisHtml += '<h4 style="color: #a78bfa; margin-bottom: 10px;">✨ Super Smart Analysis:</h4>';
    }
    
    // Show what was detected and handled
    if (data.analysis && data.analysis.sensitive_terms && data.analysis.sensitive_terms.length > 0) {
        analysisHtml += '<p style="color: #fbbf24; margin-bottom: 10px;">⚠️ Sensitive content handled professionally:</p>';
        analysisHtml += '<ul style="margin: 0 0 10px 20px; color: #888;">';
        data.analysis.sensitive_terms.forEach(term => {
            analysisHtml += `<li style="margin-bottom: 5px;">"${term}" reframed appropriately</li>`;
        });
        analysisHtml += '</ul>';
    }
    
    if (data.analysis && data.analysis.ai_opportunities && data.analysis.ai_opportunities.length > 0) {
        analysisHtml += '<p style="color: #4ade80; margin-bottom: 10px;">🎨 Creative enhancements applied:</p>';
        analysisHtml += '<ul style="margin: 0 0 10px 20px; color: #888;">';
        data.analysis.ai_opportunities.forEach(opp => {
            analysisHtml += `<li style="margin-bottom: 5px;">${opp}</li>`;
        });
        analysisHtml += '</ul>';
    }
    
    // Show optimization path
    if (data.optimization_path) {
        analysisHtml += '<p style="margin-top: 10px; color: #666; font-size: 0.9em;">';
        analysisHtml += `Optimization path: ${data.optimization_path.join(' → ')}`;
        analysisHtml += '</p>';
    }
    
    // Show auto-improvements if applied
    if (data.auto_improvements) {
        analysisHtml += '<p style="color: #60a5fa; margin: 15px 0 10px 0;">🤖 Auto-improvements applied:</p>';
        analysisHtml += '<ul style="margin: 0 0 10px 20px; color: #888; font-size: 0.9em;">';
        data.auto_improvements.improvements_applied.forEach(imp => {
            analysisHtml += `<li style="margin-bottom: 5px;">${imp.question} → <strong>${imp.answer}</strong></li>`;
        });
        analysisHtml += '</ul>';
    }
    
    analysisHtml += '</div>';
    document.getElementById('optimized-prompt').innerHTML += analysisHtml;
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show live feedback
function showFeedback(icon, text) {
    const feedbackEl = document.getElementById('live-feedback');
    const feedbackItem = feedbackEl.querySelector('.feedback-item');
    feedbackItem.querySelector('.feedback-icon').textContent = icon;
    feedbackItem.querySelector('.feedback-text').textContent = text;
    feedbackEl.style.display = 'block';
}

// Hide live feedback
function hideFeedback() {
    document.getElementById('live-feedback').style.display = 'none';
}

// Ultimate Optimize - combines auto-improvement with smart optimization
async function ultimateOptimize() {
    const prompt = document.getElementById('auto-prompt').value.trim();
    if (!prompt) {
        showFeedback('❌', 'Please enter a prompt to optimize');
        setTimeout(hideFeedback, 3000);
        return;
    }
    
    // Disable button and show progress
    const btn = event.target.closest('button');
    const btnText = btn.querySelector('#btn-text');
    const originalText = btnText.textContent;
    btn.disabled = true;
    
    // Step 1: Analyzing
    showFeedback('🔍', 'Analyzing your prompt...');
    btnText.textContent = 'Analyzing...';
    
    showLoading();
    
    try {
        // First, try to get improvement questions
        const questionsResponse = await fetch(`${API_URL}/get-questions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt })
        });
        
        const questionsData = await questionsResponse.json();
        let finalPrompt = prompt;
        let autoImprovements = null;
        
        // If there are improvements to make, apply them automatically
        if (questionsData.success && questionsData.questions && questionsData.questions.length > 0) {
            // Step 2: Improving
            showFeedback('🤖', `Found ${questionsData.questions.length} areas to improve...`);
            btnText.textContent = 'Improving...';
            
            let improvedPrompt = prompt;
            const appliedImprovements = [];
            
            for (const question of questionsData.questions) {
                let defaultAnswer = '';
                
                if (question.options && question.options.length > 0) {
                    // Smart selection of best options
                    if (question.category === 'visual_details' && question.question.includes('time of day')) {
                        defaultAnswer = question.options.find(opt => opt.includes('Golden Hour') || opt.includes('Sunset')) || question.options[0];
                    } else if (question.category === 'emotional_tone') {
                        defaultAnswer = question.options.find(opt => opt.includes('Dramatic') || opt.includes('Romantic')) || question.options[0];
                    } else if (question.category === 'artistic_style') {
                        defaultAnswer = question.options.find(opt => opt.includes('Cinematic')) || question.options[0];
                    } else {
                        defaultAnswer = question.options[0];
                    }
                } else {
                    // Smart defaults for open-ended questions
                    if (question.category === 'narrative_elements') {
                        defaultAnswer = 'capturing a pivotal emotional moment';
                    } else {
                        defaultAnswer = 'with professional quality';
                    }
                }
                
                // Apply the answer
                try {
                    const applyResponse = await fetch(`${API_URL}/apply-answer`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            prompt: improvedPrompt,
                            question: question,
                            answer: defaultAnswer
                        })
                    });
                    
                    const applyData = await applyResponse.json();
                    if (applyData.success) {
                        improvedPrompt = applyData.improved_prompt;
                        appliedImprovements.push({
                            question: question.question,
                            answer: defaultAnswer
                        });
                    }
                } catch (e) {
                    console.error('Error applying answer:', e);
                }
            }
            
            finalPrompt = improvedPrompt;
            autoImprovements = {
                questions_answered: appliedImprovements.length,
                improvements_applied: appliedImprovements
            };
        }
        
        // Step 3: Optimizing with AI
        showFeedback('🧠', 'Applying Claude AI enhancement...');
        btnText.textContent = 'Optimizing...';
        
        // Try Claude enhancement first, fallback to unified optimization
        const optimizeResponse = await fetch(`${API_URL}/claude-enhance`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                prompt: finalPrompt,
                mode: 'comprehensive'
            })
        });
        
        const optimizeData = await optimizeResponse.json();
        
        if (optimizeData.success) {
            // Success!
            showFeedback('✅', 'Optimization complete!');
            btnText.textContent = 'Complete!';
            
            // Show results with all enhancements
            showSuperResults({
                ...optimizeData,
                original: prompt,  // Show the original input
                auto_improvements: autoImprovements
            });
            
            // Reset button after delay
            setTimeout(() => {
                btn.disabled = false;
                btnText.textContent = originalText;
                hideFeedback();
            }, 2000);
        } else {
            showFeedback('❌', 'Optimization failed: ' + (optimizeData.error || 'Unknown error'));
            btn.disabled = false;
            btnText.textContent = originalText;
            hideLoading();
        }
    } catch (error) {
        showFeedback('❌', 'Error: ' + error.message);
        btn.disabled = false;
        btnText.textContent = originalText;
        hideLoading();
    }
}

// Check Claude API status
async function checkClaudeStatus() {
    try {
        const response = await fetch('/api/claude-status');
        const status = await response.json();
        
        // Update UI based on status
        if (!status.available) {
            // Show banner
            const banner = document.createElement('div');
            banner.id = 'claude-status-banner';
            banner.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: #fbbf24;
                color: #000;
                padding: 10px;
                text-align: center;
                z-index: 1000;
                font-weight: 600;
            `;
            banner.innerHTML = `
                ⚠️ ${status.message} - Using optimized local processing instead
            `;
            document.body.prepend(banner);
            
            // Update button texts
            document.querySelectorAll('button').forEach(btn => {
                if (btn.textContent.includes('Claude')) {
                    btn.innerHTML = btn.innerHTML.replace('Claude AI', 'Smart Local');
                }
            });
        }
        
        return status;
    } catch (error) {
        console.error('Failed to check Claude status:', error);
        return { available: false, message: 'Status check failed' };
    }
}

// Auto-resize textarea and show character count
document.addEventListener('DOMContentLoaded', function() {
    // Check Claude status on page load
    checkClaudeStatus();
    
    // Load account data if on account tab
    if (window.location.hash === '#account' || document.querySelector('.tab-button[data-tab="account"]')?.classList.contains('active')) {
        loadAccountData();
    }
    
    // Load account data when account tab is clicked
    document.querySelector('.tab-button[data-tab="account"]')?.addEventListener('click', function() {
        setTimeout(loadAccountData, 100); // Small delay to ensure tab is active
    });
    const textarea = document.getElementById('auto-prompt');
    const container = textarea.parentElement;
    
    // Setup generate tab interactivity
    const generateInputs = ['generate-subject', 'generate-action', 'generate-setting'];
    generateInputs.forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.addEventListener('input', updateGeneratePreview);
            input.addEventListener('focus', () => {
                showGenFeedback('💡', 'Type to see suggestions...');
            });
            input.addEventListener('blur', () => {
                setTimeout(hideGenFeedback, 1000);
            });
        }
    });
    
    // Create character counter
    const counter = document.createElement('div');
    counter.className = 'char-counter';
    counter.textContent = '0 / 500';
    container.insertBefore(counter, textarea.nextSibling);
    
    // Update on input
    textarea.addEventListener('input', function() {
        // Auto-resize
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        
        // Update counter
        const length = this.value.length;
        counter.textContent = `${length} / 500`;
        
        // Color coding
        if (length > 400) {
            counter.classList.add('error');
            counter.classList.remove('warning');
        } else if (length > 300) {
            counter.classList.add('warning');
            counter.classList.remove('error');
        } else {
            counter.classList.remove('warning', 'error');
        }
        
        // Live suggestions while typing (debounced)
        clearTimeout(window.suggestionTimeout);
        window.suggestionTimeout = setTimeout(() => {
            if (length > 10) {
                showQuickSuggestions(this.value);
            }
        }, 500);
    });
});

// Show quick suggestions while typing
async function showQuickSuggestions(prompt) {
    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt })
        });
        
        const data = await response.json();
        
        if (data.success && data.analysis) {
            const preview = document.getElementById('analysis-preview');
            const content = document.getElementById('analysis-content');
            
            // Show detected themes
            if (data.analysis.detected_themes && data.analysis.detected_themes.length > 0) {
                content.innerHTML = `
                    <p style="color: #888; font-size: 0.9em;">Detected: ${data.analysis.detected_themes.join(', ')}</p>
                    <p style="color: #666; font-size: 0.85em; margin-top: 5px;">Ready to optimize for ${data.analysis.sensitivity_level} content</p>
                `;
                preview.style.display = 'block';
            }
        }
    } catch (error) {
        // Silent fail for suggestions
    }
}

// Account Management Functions

// Load account data on page load
async function loadAccountData() {
    try {
        // Load user profile
        const profileResponse = await fetch('/api/user-profile');
        const profileData = await profileResponse.json();
        
        if (profileData.success) {
            updateUserProfile(profileData.profile);
        }
        
        // Load cost tracking data
        const costResponse = await fetch('/api/cost-tracking');
        const costData = await costResponse.json();
        
        if (costData.success) {
            updateCostTracking(costData.costs);
        }
        
        // Load analytics
        const analyticsResponse = await fetch('/api/user-analytics');
        const analyticsData = await analyticsResponse.json();
        
        if (analyticsData.success) {
            updateAnalytics(analyticsData.analytics);
        }
        
    } catch (error) {
        console.error('Error loading account data:', error);
        showAccountError('Failed to load account data');
    }
}

// Update user profile display
function updateUserProfile(profile) {
    const elements = {
        'user-segment': profile.user_segment || 'Casual User',
        'user-tier': profile.user_tier || 'Basic',
        'trust-level': profile.trust_level || 'Medium',
        'total-requests': profile.total_requests || '0',
        'success-rate': profile.success_rate ? `${(profile.success_rate * 100).toFixed(1)}%` : '0%'
    };
    
    // Add status indicators
    const trustLevel = document.getElementById('trust-level');
    const statusClass = profile.trust_level === 'High' ? 'status-active' : 
                       profile.trust_level === 'Medium' ? 'status-warning' : 'status-blocked';
    
    for (const [id, value] of Object.entries(elements)) {
        const element = document.getElementById(id);
        if (element) {
            if (id === 'trust-level') {
                element.innerHTML = `<span class="status-indicator ${statusClass}"></span>${value}`;
            } else {
                element.textContent = value;
            }
        }
    }
}

// Update cost tracking display
function updateCostTracking(costs) {
    const elements = {
        'daily-budget': `$${costs.daily_budget?.toFixed(2) || '10.00'}`,
        'spent-today': `$${costs.spent_today?.toFixed(2) || '0.00'}`,
        'remaining-budget': `$${costs.remaining_budget?.toFixed(2) || '10.00'}`,
        'current-strategy': costs.current_strategy || 'Conservative'
    };
    
    for (const [id, value] of Object.entries(elements)) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
            
            // Add appropriate classes
            if (id === 'daily-budget') element.className = 'cost-value budget';
            else if (id === 'spent-today') element.className = 'cost-value spent';
            else if (id === 'remaining-budget') element.className = 'cost-value remaining';
            else element.className = 'cost-value';
        }
    }
    
    // Update budget bar
    const budgetBar = document.getElementById('budget-used');
    if (budgetBar && costs.daily_budget && costs.spent_today) {
        const percentage = Math.min((costs.spent_today / costs.daily_budget) * 100, 100);
        budgetBar.style.width = `${percentage}%`;
    }
}

// Update analytics display
function updateAnalytics(analytics) {
    const elements = {
        'primary-categories': analytics.primary_categories?.join(', ') || 'None yet',
        'content-consistency': analytics.content_consistency || 'Building profile...',
        'skill-level': analytics.skill_level || 'Beginner',
        'peak-hours': analytics.peak_hours || 'Not enough data'
    };
    
    for (const [id, value] of Object.entries(elements)) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }
    
    // Update recommendations
    const recommendationsList = document.getElementById('recommendations-list');
    if (recommendationsList && analytics.recommendations) {
        recommendationsList.innerHTML = '';
        analytics.recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            recommendationsList.appendChild(li);
        });
    } else if (recommendationsList) {
        recommendationsList.innerHTML = '<li>Keep using the system to get personalized recommendations!</li>';
    }
}

// Refresh account data
async function refreshAccountData() {
    const btn = event.target;
    const originalText = btn.textContent;
    
    btn.disabled = true;
    btn.textContent = '🔄 Refreshing...';
    
    try {
        await loadAccountData();
        
        // Show success feedback
        btn.textContent = '✅ Updated!';
        btn.style.background = '#4ade80';
        
        setTimeout(() => {
            btn.disabled = false;
            btn.textContent = originalText;
            btn.style.background = '';
        }, 2000);
        
    } catch (error) {
        btn.textContent = '❌ Failed';
        btn.style.background = '#ef4444';
        
        setTimeout(() => {
            btn.disabled = false;
            btn.textContent = originalText;
            btn.style.background = '';
        }, 2000);
    }
}

// Test model selection
async function testModelSelection() {
    const btn = event.target;
    const originalText = btn.textContent;
    
    btn.disabled = true;
    btn.textContent = '🧪 Testing...';
    
    try {
        const testPrompts = [
            'Simple test prompt',
            'More complex creative scenario with detailed cinematic requirements and sophisticated artistic elements',
            'Extremely sophisticated artistic vision requiring premium processing with ultra-high quality demands and complex narrative elements'
        ];
        
        const results = [];
        
        // Test each prompt individually
        for (let i = 0; i < testPrompts.length; i++) {
            const prompt = testPrompts[i];
            btn.textContent = `🧪 Testing ${i + 1}/${testPrompts.length}...`;
            
            const response = await fetch('/api/test-model-selection', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt,
                    force_quality: i === testPrompts.length - 1  // Force quality for last test
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                results.push({
                    prompt: prompt,
                    selected_model: data.model_selection.model,
                    reasoning: data.model_selection.reasoning || 'Smart selection based on complexity',
                    estimated_cost: data.model_info.cost_per_request || '$0.001',
                    quality_score: data.model_selection.quality_expected || 0.85,
                    budget_safe: data.budget_info.safe_to_use,
                    user_segment: data.user_info.segment
                });
            } else {
                results.push({
                    prompt: prompt,
                    selected_model: 'Error',
                    reasoning: data.error || 'Test failed',
                    estimated_cost: '$0.000',
                    quality_score: 0,
                    budget_safe: false,
                    user_segment: 'unknown'
                });
            }
        }
        
        // Show test results
        showModelSelectionResults(results);
        
        btn.textContent = '✅ Test Complete!';
        btn.style.background = '#4ade80';
        
    } catch (error) {
        console.error('Model selection test failed:', error);
        btn.textContent = '❌ Test Failed';
        btn.style.background = '#ef4444';
    }
    
    setTimeout(() => {
        btn.disabled = false;
        btn.textContent = originalText;
        btn.style.background = '';
    }, 3000);
}

// Show model selection test results
function showModelSelectionResults(results) {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    `;
    
    const dialog = document.createElement('div');
    dialog.style.cssText = `
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 30px;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
    `;
    
    let html = `
        <h2 style="color: #4ade80; margin-bottom: 20px;">🧪 Model Selection Test Results</h2>
        <div style="margin-bottom: 20px;">
    `;
    
    results.forEach((result, index) => {
        html += `
            <div style="background: #0a0a0a; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h4 style="color: #667eea; margin-bottom: 10px;">Test ${index + 1}</h4>
                <p style="color: #888; margin-bottom: 8px;"><strong>Prompt:</strong> ${result.prompt}</p>
                <p style="color: #888; margin-bottom: 8px;"><strong>Selected Model:</strong> ${result.selected_model}</p>
                <p style="color: #888; margin-bottom: 8px;"><strong>Reasoning:</strong> ${result.reasoning}</p>
                <p style="color: #888; margin-bottom: 8px;"><strong>Estimated Cost:</strong> $${result.estimated_cost}</p>
                <p style="color: #888;"><strong>Quality Score:</strong> ${(result.quality_score * 100).toFixed(1)}%</p>
            </div>
        `;
    });
    
    html += `
        </div>
        <button onclick="this.parentElement.parentElement.remove()" 
                style="width: 100%; padding: 12px; background: #667eea; color: white; 
                       border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">
            Close
        </button>
    `;
    
    dialog.innerHTML = html;
    overlay.appendChild(dialog);
    document.body.appendChild(overlay);
}

// Show account error
function showAccountError(message) {
    const elements = ['user-segment', 'user-tier', 'trust-level', 'total-requests', 'success-rate',
                     'daily-budget', 'spent-today', 'remaining-budget', 'current-strategy',
                     'primary-categories', 'content-consistency', 'skill-level', 'peak-hours'];
    
    elements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = 'Error loading';
            element.style.color = '#ef4444';
        }
    });
    
    // Show error in recommendations
    const recommendationsList = document.getElementById('recommendations-list');
    if (recommendationsList) {
        recommendationsList.innerHTML = `<li style="color: #ef4444;">❌ ${message}</li>`;
    }
}