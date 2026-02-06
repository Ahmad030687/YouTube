from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - YouTube Unlimited Downloader Active!"

@app.route('/api/ytdl', methods=['GET'])
def downloader():
    # 1. URL lena
    video_url = request.args.get('url')
    # Hum 'type' parameter ko ignore kar rahe hain taake koi restriction na ho
    # Bas jo best milega wo uthayenge
    
    if not video_url:
        return jsonify({"status": False, "error": "URL missing!"}), 400

    # 2. Cookies Check
    cookie_file = 'cookies.txt'
    if not os.path.exists(cookie_file):
        return jsonify({"status": False, "error": "cookies.txt file missing on server! Upload it."}), 500

    # 3. "Grab Anything" Settings
    ydl_opts = {
        # Format Logic:
        # 'bestaudio' = Sabse achi audio dhoondo.
        # '/best' = Agar audio alag se na mile, to jo bhi best video/audio combo hai wo utha lo.
        'format': 'bestaudio/best', 
        
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': cookie_file, # Cookies lazmi hain
        'noplaylist': True,
        'geo_bypass': True,
        'ignoreerrors': True, # Agar choti moti error aaye to ignore karo
        
        # User Agent (Desktop wala taake mobile restriction na aaye)
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Info Extract
            info = ydl.extract_info(video_url, download=False)
            
            # Direct Link Nikaalne ka "Jugaad"
            download_url = info.get('url')
            
            # Agar direct URL null hai, to formats list mein se pehla zinda link uthao
            if not download_url:
                formats = info.get('formats', [])
                # Reverse loop: Kyunke last wale formats usually high quality hote hain
                for f in reversed(formats):
                    if f.get('url'): # Jisme bhi URL ho, wo le lo
                        download_url = f['url']
                        break
            
            # Agar ab bhi URL nahi mila (boht rare case)
            if not download_url:
                 return jsonify({"status": False, "error": "No download link found in any format."}), 404

            return jsonify({
                "status": True,
                "title": info.get('title', 'Unknown Title'),
                "duration": info.get('duration_string', 'N/A'),
                "download_url": download_url,
                "author": "Ahmad RDX"
            })

    except Exception as e:
        # Error wapis bhejo taake pata chale kya hua
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
