# Django YouTube Downloader

A simple Django web application for downloading YouTube videos by fetching video details and allowing users to select resolution before downloading.

## Features

- Fetches video details from YouTube
- Allows users to select video resolution
- Downloads video in the selected resolution
- Responsive design for mobile screens
- No database required

## Requirements

- Python 3.x
- Django 3.x
- `pytube` for YouTube video downloads
- `gunicorn` for running the server

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/youtube-downloader.git
   cd youtube-downloader
2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install the required packages:

   ```sh
   pip install -r requirements.txt
4. Run migrations:

   ```sh
   python manage.py migrate
5. Create a superuser:

   ```sh
   python manage.py createsuperuser
6. Run the development server:

   ```sh
   python manage.py runserver

## Usage

1. Navigate to `http://127.0.0.1:8000/` in your web browser.
2. Enter the YouTube video URL and click "Fetch Video Details".
3. Select the desired video resolution.
4. Click the "Download" button to start downloading the video.

## Project Structure

youtube_downloader/
├── youtube_downloader/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── downloader/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
│       └── downloader/
│           ├── index.html
│           └── video_details.html
├── static/
│   └── downloader/
│       ├── css/
│       ├── js/
│       └── images/
├── media/
├── manage.py
└── requirements.txt

## Common Issues
# Internal Server Error
If you encounter an internal server error while fetching the video details, it might be due to the application running out of memory.

## Worker Killed (SIGKILL)
If you see a log message indicating that a worker was killed (SIGKILL), it is likely due to the application running out of memory. Ensure your application is running on a machine with sufficient memory, and consider optimizing your code to use less memory.

## Contact
For any questions or feedback, please reach out to nishantsinha96089@gmail.com

```sh
This `README.md` file should provide a comprehensive overview and guidance for your project. Make sure to update the placeholders with your actual repository URL, contact information, and any other specific details relevant to your project.



   
