# Railway.app Deployment Guide

This guide explains how to deploy the YouTube Downloader application to Railway.app.

## Prerequisites

1. Railway.app account (free tier available)
2. This project folder

## Deployment Steps

### Method 1: Deploy from GitHub (Recommended)

1. Fork this repository to your GitHub account
2. Sign in to Railway.app
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your forked repository
6. Railway will automatically detect the project and deploy it

### Method 2: Deploy from CLI

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Initialize a new Railway project:
   ```bash
   railway init
   ```

4. Deploy the application:
   ```bash
   railway up
   ```

### Method 3: Deploy from Dashboard (Manual Upload)

1. Sign in to Railway.app
2. Click "New Project"
3. Select "Empty Project"
4. Click "Add Service"
5. Choose "Deploy from GitHub" or "Deploy from Local Directory"
6. If deploying from local directory, upload all files from this project folder

## Configuration

Railway will automatically:
- Detect the Python application
- Install dependencies from requirements.txt
- Install ffmpeg using the Nixpacks configuration
- Start the application using Gunicorn

## Environment Variables

Railway automatically provides a `PORT` environment variable. The application is configured to use this.

## Custom Domain (Optional)

1. In your Railway project dashboard, go to Settings
2. Click "Custom Domains"
3. Add your custom domain
4. Follow Railway's instructions to configure DNS

## Scaling

Railway automatically scales your application based on traffic. For manual scaling:

1. Go to your service in the Railway dashboard
2. Click "Settings"
3. Adjust the "Sleep Mode" and "Instance Size" as needed

## Monitoring

Railway provides built-in monitoring:
- Logs: View real-time logs in the Railway dashboard
- Metrics: CPU, memory, and network usage
- Health checks: Automatic health monitoring

## Troubleshooting

### Common Issues

1. **Build Failures**: Check the build logs in Railway dashboard
2. **Runtime Errors**: Check the application logs
3. **FFmpeg Issues**: Ensure ffmpeg is properly installed via Nixpacks

### Checking Logs

1. Go to your Railway project
2. Select your service
3. Click "Logs" to view real-time logs

### Restarting the Application

1. Go to your Railway project
2. Select your service
3. Click "Restart" in the top right corner

## Updating the Application

### From GitHub

1. Push changes to your GitHub repository
2. Railway will automatically redeploy

### From CLI

1. Make changes to your local files
2. Run `railway up` to deploy changes

## Support

For issues with Railway deployment:
- Check Railway documentation: https://docs.railway.app
- Visit Railway Discord: https://discord.gg/railway