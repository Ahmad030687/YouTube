from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - YouTube Downloader API (with Cookies) Active!"

@app.route('/api/ytdl', methods=['GET'])
def downloader():
    # 1. URL aur Type lena
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'audio') # audio or video
    
    if not video_url:
        return jsonify({"status": False, "error": "URL missing!"}), 400

    # 2. Check agar cookies file majood hai
    cookie_file = 'cookies.txt'
    if not os.path.exists(cookie_file):
        return jsonify({"status": False, "error": "cookies.txt file missing on server!"}), 500

    # 3. yt-dlp Options (Anti-Block + Cookies)
    ydl_opts = {
        'format': 'bestaudio/best' if req_type == 'audio' else 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': cookie_file,  # 🍪 Cookies yahan load hongi
        'noplaylist': True,
        'geo_bypass': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios'], # Mobile Spoofing
                'skip': ['hls', 'dash']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Info Extract
            info = ydl.extract_info(video_url, download=False)
            
            # Direct Link Logic
            download_url = info.get('url')
            if not download_url:
                formats = info.get('formats', [])
                for f in reversed(formats):
                    if f.get('url'):
                        download_url = f['url']
                        break

            return jsonify({
                "status": True,
                "title": info.get('title'),
                "duration": info.get('duration_string'),
                "quality": "High",
                "download_url": download_url,
                "author": "Ahmad RDX"
            })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
  
