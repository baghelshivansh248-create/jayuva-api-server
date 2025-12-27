import os  # Ye cloud port detect karne ke liye zaroori hai
from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# --- 1. Background Remover ---
@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        if 'image' not in request.files:
            return {"error": "Image select kijiye bhai"}, 400
        file = request.files['image'].read()
        output = remove(file)
        return send_file(io.BytesIO(output), mimetype='image/png')
    except Exception as e:
        return {"error": str(e)}, 500

# --- 2. Image Studio (Compress, Resize, 8K) ---
@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return {"error": "Image select kijiye bhai"}, 400
        file = request.files['image']
        quality = int(request.form.get('quality', 95)) 
        width = request.form.get('width')
        height = request.form.get('height')
        target_format = request.form.get('format', 'JPEG').upper()

        img = Image.open(file.stream)

        if width and height:
            img = img.resize((int(width), int(height)), Image.Resampling.LANCZOS)

        img_io = io.BytesIO()
        if target_format == "JPEG":
            img = img.convert("RGB")
            
        img.save(img_io, format=target_format, quality=quality, optimize=True)
        img_io.seek(0)
        
        return send_file(img_io, mimetype=f'image/{target_format.lower()}')
    except Exception as e:
        return {"error": str(e)}, 500

# --- Welcome Route (Browser check ke liye) ---
@app.route('/')
def home():
    return "<h1>Jayuva Studio API is LIVE!</h1>"

if __name__ == '__main__':
    # Cloud server environment se port uthayega, nahi toh 5000 use karega
    server_port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Jayuva Studio API starting on port {server_port}")
    app.run(host='0.0.0.0', port=server_port)