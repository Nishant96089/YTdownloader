from django.shortcuts import render
from .forms import URLForm
import yt_dlp as youtube_dl
import ffmpeg
import os
import shutil
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path

# Temporary directory for downloads
TEMP_DOWNLOAD_DIR = 'temp_downloads'

# Ensure temporary download directory exists
os.makedirs(TEMP_DOWNLOAD_DIR, exist_ok=True)

def index(request):
    form = URLForm()
    video_info = None

    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('video_url')
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best'
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_info = {
                    'title': info_dict.get('title', None),
                    'thumbnail': info_dict.get('thumbnail', None),
                    'duration': info_dict.get('duration', None),
                    'views': info_dict.get('view_count', None),
                    'likes': info_dict.get('like_count', None),
                    'formats': []
                }

                # Collect all video formats with the best audio
                for fmt in info_dict.get('formats', []):
                    filesize = fmt.get('filesize', 0) / 1024 / 1024  # Convert filesize to MB
                    if fmt.get('vcodec') != 'none' and filesize > 0:
                        video_info['formats'].append({
                            'resolution': fmt.get('format_note', None) or f"{fmt.get('height', 'Unknown')}p",
                            'ext': fmt.get('ext', None),
                            'filesize_mb': round(filesize),
                            'format_id': fmt.get('format_id', None)
                        })

    return render(request, 'download/index.html', {'form': form, 'video_info': video_info})

@csrf_exempt
def download(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        format_id = request.POST.get('format_id')

        # Temporary filenames
        temp_video_path = os.path.join(TEMP_DOWNLOAD_DIR, 'video')
        temp_audio_path = os.path.join(TEMP_DOWNLOAD_DIR, 'audio')

        video_opts = {
            'format': format_id,
            'outtmpl': temp_video_path + '/%(title)s.%(ext)s',
        }

        audio_opts = {
            'format': 'bestaudio',
            'outtmpl': temp_audio_path + '/%(title)s.%(ext)s',
        }

        try:
            # Ensure directories exist
            os.makedirs(temp_video_path, exist_ok=True)
            os.makedirs(temp_audio_path, exist_ok=True)

            # Download the video
            with youtube_dl.YoutubeDL(video_opts) as ydl:
                video_info = ydl.extract_info(url, download=True)
                video_filename = ydl.prepare_filename(video_info)

            # Download the audio
            with youtube_dl.YoutubeDL(audio_opts) as ydl:
                audio_info = ydl.extract_info(url, download=True)
                audio_filename = ydl.prepare_filename(audio_info)

            # Define the output filename for the merged file
            merged_filename = os.path.basename(video_filename)
            merged_filepath = os.path.join(TEMP_DOWNLOAD_DIR, merged_filename)

            # Merging video and audio correctly
            video_input = ffmpeg.input(video_filename)
            audio_input = ffmpeg.input(audio_filename)
            ffmpeg.concat(video_input, audio_input, v=1, a=1).output(merged_filepath).run()

            # Clean up temporary files
            os.remove(video_filename)
            os.remove(audio_filename)

            # Move the merged file to the user's download directory
            user_download_dir = str(Path.home() / 'Downloads')
            final_filepath = os.path.join(user_download_dir, merged_filename)
            shutil.move(merged_filepath, final_filepath)

            # Clean up the temporary directory
            shutil.rmtree(TEMP_DOWNLOAD_DIR)

            # Send the merged file as a response
            return FileResponse(open(final_filepath, 'rb'), as_attachment=True, filename=merged_filename)
        except Exception as e:
            # Clean up any files that were downloaded if an error occurs
            if os.path.exists(video_filename):
                os.remove(video_filename)
            if os.path.exists(audio_filename):
                os.remove(audio_filename)
            if os.path.exists(merged_filepath):
                os.remove(merged_filepath)
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
