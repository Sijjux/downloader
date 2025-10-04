import os
import sys
import subprocess
import time
from flask import Flask, render_template, request, send_file, after_this_request, jsonify
import yt_dlp

# Get port from environment variable or default to 5000
port = int(os.environ.get('PORT', 5000))

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'

# Simple cache for video info (in production, use Redis or similar)
video_info_cache = {}

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def check_ffmpeg():
    """Check if ffmpeg is installed and accessible."""
    try:
        # Try to run ffmpeg command
        result = subprocess.run(['ffmpeg', '-version'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True,
                               check=True)
        # Extract version from output
        version_line = result.stdout.split('\n')[0]
        return True, version_line
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        return False, str(e)

def get_video_info(url):
    """Get video information using yt-dlp with caching and optimization."""
    # Check cache first
    cache_key = url
    if cache_key in video_info_cache:
        cached_info, timestamp = video_info_cache[cache_key]
        # Cache for 5 minutes
        if time.time() - timestamp < 300:
            return cached_info
    
    try:
        # Optimized ydl options for faster info retrieval
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'extract_flat': 'in_playlist',  # Faster for single videos
            'force_generic_extractor': False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_info = {
                'title': info_dict.get('title', 'Unknown Title'),
                'thumbnail': info_dict.get('thumbnail', ''),
                'duration': info_dict.get('duration', 0),
                'uploader': info_dict.get('uploader', 'Unknown Uploader'),
            }
            
            # Cache the result
            video_info_cache[cache_key] = (video_info, time.time())
            return video_info
    except Exception as e:
        raise Exception(f"Could not fetch video info: {str(e)}")

@app.route('/')
def index():
    """Render the main page with the URL input form."""
    # Check for ffmpeg on initial page load and pass to template
    ffmpeg_available, ffmpeg_info = check_ffmpeg()
    return render_template('index.html', 
                         ffmpeg_available=ffmpeg_available,
                         ffmpeg_info=ffmpeg_info if ffmpeg_available else None)

@app.route('/health')
def health():
    """Health check endpoint for deployment monitoring."""
    ffmpeg_available, ffmpeg_info = check_ffmpeg()
    return jsonify({
        'status': 'healthy',
        'ffmpeg_available': ffmpeg_available,
        'timestamp': time.time()
    })

@app.route('/preview', methods=['POST'])
def preview():
    """Display video info before downloading."""
    url = request.form['url']
    format_choice = request.form['format']
    
    # Check if ffmpeg is available
    ffmpeg_available, ffmpeg_info = check_ffmpeg()
    
    # Validate URL
    if not url or ('youtube.com' not in url and 'youtu.be' not in url):
        return render_template('index.html', 
                             error="Please enter a valid YouTube URL",
                             ffmpeg_available=ffmpeg_available,
                             ffmpeg_info=ffmpeg_info if ffmpeg_available else None)
    
    try:
        video_info = get_video_info(url)
        return render_template('index.html', 
                             video_title=video_info['title'], 
                             thumbnail=video_info['thumbnail'], 
                             url=url, 
                             format=format_choice,
                             uploader=video_info['uploader'],
                             ffmpeg_available=ffmpeg_available,
                             ffmpeg_info=ffmpeg_info if ffmpeg_available else None)
    except Exception as e:
        return render_template('index.html', 
                             error=f"Error: {str(e)}",
                             ffmpeg_available=ffmpeg_available,
                             ffmpeg_info=ffmpeg_info if ffmpeg_available else None)

@app.route('/download', methods=['POST'])
def download():
    """Handle the download request."""
    url = request.form['url']
    format_choice = request.form['format']
    video_title = request.form['title']
    quality = request.form.get('quality', 'best')  # Default to 'best'
    
    # Check if ffmpeg is available
    ffmpeg_available, ffmpeg_info = check_ffmpeg()
    if not ffmpeg_available:
        return render_template('index.html', 
                             error="FFmpeg is required for both video and audio downloads but not found.",
                             ffmpeg_available=False,
                             ffmpeg_info=None)
    
    try:
        # Sanitize filename
        safe_title = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c.isspace() or c in "._-"]).rstrip()
        # Replace spaces with underscores
        safe_title = safe_title.replace(' ', '_')
        
        if format_choice == 'video':
            file_extension = 'mp4'
            # Build format string based on quality selection
            if quality == 'best':
                format_string = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            else:
                # For specific resolutions, we specify the maximum height
                format_string = f'bestvideo[ext=mp4][height<={quality}]+bestaudio[ext=m4a]/best[ext=mp4][height<={quality}]/best[height<={quality}]'
            
            ydl_opts = {
                'format': format_string,
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{safe_title}.%(ext)s'),
                'merge_output_format': 'mp4',
                'quiet': True,  # Reduce output for faster processing
            }
        else:  # audio
            file_extension = 'mp3'
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{safe_title}.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,  # Reduce output for faster processing
            }

        # Download the file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find the actual downloaded file (yt-dlp may add suffixes)
        downloaded_file = None
        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.startswith(safe_title) and file.endswith(file_extension):
                downloaded_file = os.path.join(DOWNLOAD_FOLDER, file)
                break
        
        if not downloaded_file or not os.path.exists(downloaded_file):
            # Try without extension check
            for file in os.listdir(DOWNLOAD_FOLDER):
                if file.startswith(safe_title):
                    downloaded_file = os.path.join(DOWNLOAD_FOLDER, file)
                    break
        
        if not downloaded_file or not os.path.exists(downloaded_file):
            raise Exception("Download failed - file not found")

        @after_this_request
        def cleanup(response):
            try:
                os.remove(downloaded_file)
            except OSError as e:
                print(f"Error cleaning up file {downloaded_file}: {e}")
            return response

        return send_file(downloaded_file, as_attachment=True)

    except Exception as e:
        return render_template('index.html', 
                             error=f"An error occurred during download: {str(e)}",
                             ffmpeg_available=check_ffmpeg()[0],
                             ffmpeg_info=check_ffmpeg()[1] if check_ffmpeg()[0] else None)

if __name__ == '__main__':
    # Check dependencies
    print("Checking dependencies...")
    
    # Check yt-dlp
    try:
        import yt_dlp
        print("✓ yt-dlp is installed")
    except ImportError:
        print("✗ yt-dlp is not installed. Please install it with: pip install yt-dlp")
        sys.exit(1)
    
    # Check ffmpeg
    ffmpeg_available, ffmpeg_info = check_ffmpeg()
    if ffmpeg_available:
        print(f"✓ ffmpeg is installed and accessible")
    else:
        print("! Warning: ffmpeg not found. For online deployment, ensure ffmpeg is available.")
    
    print(f"\nStarting server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)