# YouTube Audio/Video Downloader

A simple and user-friendly web application for downloading YouTube videos and audio using yt-dlp and ffmpeg.

## Features

- Download YouTube videos in MP4 format
- Extract audio from YouTube videos in MP3 format
- Select video quality from 360p up to 4K (Best quality by default)
- Modern, responsive web interface
- Video preview before download
- Real-time download progress indication
- Caching for faster repeated requests

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.7 or higher**
2. **ffmpeg** - Required for video merging and audio extraction

## Installation

1. Clone or download this repository
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Installing ffmpeg

### Automatic Installation (Windows)

1. Run the `install_ffmpeg.bat` file included in this repository
2. Follow the on-screen instructions
3. Restart your command prompt or PowerShell after installation

### Manual Installation (All Platforms)

#### Windows:
1. Download ffmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Or download directly from: https://github.com/BtbN/FFmpeg-Builds/releases/latest (Recommended)
   - Download the "win64-gpl" version
2. Extract the downloaded file to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH:
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Go to "Advanced" tab → "Environment Variables"
   - Under "System Variables", find and select "Path", click "Edit"
   - Click "New" and add `C:\ffmpeg\bin`
   - Click "OK" to save all changes

#### macOS:
```bash
# Using Homebrew
brew install ffmpeg
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg
```

## Usage

### Quick Start (Windows)
Double-click the `start.bat` file to automatically set up and start the application.

### Quick Start (macOS/Linux)
Run the `start.sh` script:
```bash
chmod +x start.sh
./start.sh
```

### Manual Start
1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Paste a YouTube URL, select your desired format (video or audio) and quality, and click "Get Video Info"

4. Preview the video information and click "Download" to start the download

## Deployment

This application can be deployed to various hosting platforms:

### Railway.app Deployment (Recommended)

1. Sign up for a free account at [Railway.app](https://railway.app)
2. Fork this repository to your GitHub account or upload the files directly
3. Connect Railway to your repository or upload the project files
4. Railway will automatically detect and deploy the application
5. The app will be available at the URL provided by Railway

See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed deployment instructions.

### Other Deployment Options

- Heroku deployment (with and without Git)
- Docker deployment
- Traditional server deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Easy Heroku Deployment (No Git Required)

For Windows users, you can deploy to Heroku without installing Git:

1. Install Heroku CLI from [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
2. Run the `deploy_heroku.bat` script (Windows) or `deploy_heroku.ps1` script (PowerShell)
3. Follow the on-screen instructions

### Git Installation (If Required)

If you choose a deployment method that requires Git, install it from:
- Windows: [https://git-scm.com/downloads](https://git-scm.com/downloads)
- macOS: `brew install git` (requires Homebrew)
- Linux (Ubuntu/Debian): `sudo apt install git`

## How It Works

This application uses:
- **Flask** - Web framework for the user interface
- **yt-dlp** - Advanced YouTube video downloader
- **ffmpeg** - Multimedia processing library for video merging and audio extraction
- **Gunicorn** - WSGI server for production deployment

## Troubleshooting

### "FFmpeg not found" error
Ensure ffmpeg is installed and added to your system PATH. You can verify by running:
```bash
ffmpeg -version
```

If the command is not recognized:
1. Check that ffmpeg is installed
2. Verify that the bin directory is in your PATH
3. Restart your terminal/command prompt

### Download issues
- Make sure you're using a valid YouTube URL
- Some videos may have restrictions that prevent downloading
- Check your internet connection

### Performance issues
- The first request for a video will be slower as metadata needs to be fetched
- Subsequent requests for the same video are cached for 5 minutes
- Selecting "Best Available" quality is typically faster than specific resolutions

## Disclaimer

This tool is for personal use only. Please respect copyright laws and YouTube's terms of service. Do not use this tool to download copyrighted content without permission.