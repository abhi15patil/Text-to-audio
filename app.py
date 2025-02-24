from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/audio'

# Supported languages (add more as needed)
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'mr': 'Marathi'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        lang = request.form.get('language', 'en')  # Default to English
        
        # Generate unique filename with language code
        filename = f"audio_{lang}_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Convert text to speech with selected language
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filepath)
        
        return render_template('index.html', 
                             audio_file=filename,
                             languages=SUPPORTED_LANGUAGES,
                             selected_lang=lang)
    
    return render_template('index.html', 
                          languages=SUPPORTED_LANGUAGES,
                          selected_lang='en')

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
