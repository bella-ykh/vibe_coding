from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import os
import yt_dlp
import tempfile
import threading
import time
from urllib.parse import urlparse, parse_qs
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# 다운로드 진행 상황을 저장할 딕셔너리
download_progress = {}

def is_valid_youtube_url(url):
    """유튜브 URL이 유효한지 확인"""
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return youtube_regex.match(url) is not None

def get_video_info(url):
    """동영상 정보 가져오기"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'thumbnail': info.get('thumbnail', ''),
                'formats': [
                    {
                        'format_id': fmt.get('format_id'),
                        'ext': fmt.get('ext'),
                        'resolution': fmt.get('resolution', 'Unknown'),
                        'filesize': fmt.get('filesize', 0),
                        'quality': fmt.get('quality', 0)
                    }
                    for fmt in info.get('formats', [])
                    if fmt.get('vcodec') != 'none' or fmt.get('acodec') != 'none'
                ]
            }
    except Exception as e:
        return None

def progress_hook(d):
    """다운로드 진행 상황 업데이트"""
    if d['status'] == 'downloading':
        if 'total_bytes' in d:
            percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            download_progress[d['filename']] = {
                'status': 'downloading',
                'percent': round(percent, 2),
                'speed': d.get('speed', 0),
                'eta': d.get('eta', 0)
            }
    elif d['status'] == 'finished':
        download_progress[d['filename']] = {
            'status': 'finished',
            'percent': 100,
            'filename': d['filename']
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info', methods=['POST'])
def get_video_info_route():
    url = request.json.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL을 입력해주세요.'}), 400
    
    if not is_valid_youtube_url(url):
        return jsonify({'error': '유효한 유튜브 URL을 입력해주세요.'}), 400
    
    info = get_video_info(url)
    if not info:
        return jsonify({'error': '동영상 정보를 가져올 수 없습니다.'}), 400
    
    return jsonify(info)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url', '').strip()
    format_id = request.json.get('format_id', 'best')
    
    if not url or not is_valid_youtube_url(url):
        return jsonify({'error': '유효한 유튜브 URL을 입력해주세요.'}), 400
    
    # 임시 디렉토리 생성
    temp_dir = tempfile.mkdtemp()
    
    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'format': format_id,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # 실제 다운로드된 파일 찾기
            for file in os.listdir(temp_dir):
                if file.endswith(('.mp4', '.webm', '.mkv', '.avi')):
                    file_path = os.path.join(temp_dir, file)
                    return send_file(file_path, as_attachment=True, download_name=file)
            
            return jsonify({'error': '다운로드된 파일을 찾을 수 없습니다.'}), 400
            
    except Exception as e:
        return jsonify({'error': f'다운로드 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/progress/<filename>')
def get_progress(filename):
    """다운로드 진행 상황 조회"""
    progress = download_progress.get(filename, {'status': 'not_found'})
    return jsonify(progress)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
