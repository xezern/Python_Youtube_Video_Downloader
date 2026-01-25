#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import sys
import subprocess
import shutil

# Yüklənəcək qovluq
DOWNLOAD_DIR = "downloads"

# Maksimum keyfiyyət (1080, 720, 480, 360)
MAX_RESOLUTION = 720

video_urls = [
    "https://www.youtube.com/watch?v=zD5Ee99Gy8I&start_radio=1"
    
]

def check_ffmpeg():
    """ffmpeg-in quraşdırılıb-quraşdırılmadığını yoxlayır"""
    return shutil.which('ffmpeg') is not None

def get_resolution_value(stream):
    """Stream-dən resolution dəyərini alır"""
    if stream.resolution:
        try:
            return int(stream.resolution.replace('p', ''))
        except:
            return 0
    return 0

def find_best_video_stream(yt, max_res=None):
    """Ən yüksək keyfiyyətli video stream-i tapır (audio olmadan)"""
    streams = yt.streams.filter(
        adaptive=True,
        file_extension='mp4',
        only_video=True
    ).order_by('resolution').desc()
    
    if max_res:
        for stream in streams:
            res = get_resolution_value(stream)
            if res <= max_res:
                return stream
    
    return streams.first()

def find_best_audio_stream(yt):
    """Ən yüksək keyfiyyətli audio stream-i tapır"""
    return yt.streams.filter(
        adaptive=True,
        only_audio=True
    ).order_by('abr').desc().first()

def find_best_progressive_stream(yt, max_res=None):
    """Progressive stream tapır (video+audio birlikdə, ffmpeg lazım deyil)"""
    streams = yt.streams.filter(
        progressive=True,
        file_extension='mp4'
    ).order_by('resolution').desc()
    
    if max_res:
        for stream in streams:
            res = get_resolution_value(stream)
            if res <= max_res:
                return stream
    
    return streams.first()

def format_size(bytes):
    """Bayt ölçüsünü oxunaqlı formata çevirir"""
    if bytes is None:
        return "N/A"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} TB"

def merge_video_audio(video_path, audio_path, output_path):
    """ffmpeg ilə video və audio-nu birləşdirir"""
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-y', 
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        # Müvəqqəti faylları sil
        os.remove(video_path)
        os.remove(audio_path)
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️ ffmpeg xətası: {e.stderr.decode()[:200]}")
        return False

def sanitize_filename(filename):
    """Fayl adından xüsusi simvolları silir"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_video(url, output_dir=DOWNLOAD_DIR, max_res=MAX_RESOLUTION):
    """
    Tək videonu ən yüksək keyfiyyətdə yükləyir
    
    Args:
        url: YouTube video URL-i
        output_dir: Yüklənəcək qovluq
        max_res: Maksimum keyfiyyət (None = ən yüksək)
    
    Returns:
        True əgər uğurlu, False əgər xəta
    """
    try:
        print(f"\n{'─' * 60}")
        print(f"🔗 URL: {url}")
        
        # YouTube obyekti yarat (progress callback ilə)
        yt = YouTube(url, on_progress_callback=on_progress)
        
        title = sanitize_filename(yt.title)
        print(f"📹 Başlıq: {yt.title}")
        print(f"⏱️  Uzunluq: {yt.length // 60}:{yt.length % 60:02d}")
        print(f"👁️  Baxış: {yt.views:,}")
        
        has_ffmpeg = check_ffmpeg()
        
        if has_ffmpeg:
            # ffmpeg var - ən yüksək keyfiyyət üçün adaptive streams istifadə et
            video_stream = find_best_video_stream(yt, max_res)
            audio_stream = find_best_audio_stream(yt)
            
            if video_stream and audio_stream:
                print(f"📊 Video keyfiyyəti: {video_stream.resolution}")
                print(f"🔊 Audio keyfiyyəti: {audio_stream.abr}")
                print(f"📦 Video ölçüsü: {format_size(video_stream.filesize)}")
                print(f"📥 Video yüklənir...")
                
                # Video yüklə
                video_path = video_stream.download(
                    output_path=output_dir,
                    filename=f"{title}_video.mp4"
                )
                
                print(f"📥 Audio yüklənir...")
                # Audio yüklə
                audio_path = audio_stream.download(
                    output_path=output_dir,
                    filename=f"{title}_audio.mp4"
                )
                
                print(f"🔄 Birləşdirilir...")
                output_path = os.path.join(output_dir, f"{title}.mp4")
                
                if merge_video_audio(video_path, audio_path, output_path):
                    print(f"\n✅ Uğurla yükləndi! ({video_stream.resolution})")
                    return True
                else:
                    print(f"\n⚠️ Birləşdirmə uğursuz, progressive stream sınaqdan keçirilir...")
        
        # ffmpeg yoxdur və ya birləşdirmə uğursuz - progressive stream istifadə et
        if not has_ffmpeg:
            print(f"⚠️ ffmpeg tapılmadı - 720p+ üçün ffmpeg quraşdırın!")
            print(f"   Quraşdırma: winget install ffmpeg")
            print(f"   Progressive stream istifadə edilir (max 360-480p)...")
        
        stream = find_best_progressive_stream(yt, max_res)
        
        if not stream:
            print(f"❌ Uyğun stream tapılmadı!")
            return False
        
        print(f"📊 Keyfiyyət: {stream.resolution}")
        print(f"📦 Ölçü: {format_size(stream.filesize)}")
        print(f"📥 Yüklənir...")
        
        stream.download(output_path=output_dir, filename=f"{title}.mp4")
        
        print(f"\n✅ Uğurla yükləndi!")
        return True
        
    except Exception as e:
        print(f"\n❌ Xəta: {str(e)}")
        return False

def download_all_videos(urls, output_dir=DOWNLOAD_DIR, max_res=MAX_RESOLUTION):
    """
    Bütün videoları yükləyir
    """
    # Qovluğu yarat
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("   🎬 YOUTUBE VİDEO YÜKLƏYİCİ")
    print("   pytubefix ilə - ffmpeg tələb etmir!")
    print("=" * 60)
    print(f"📁 Yükləmə qovluğu: {os.path.abspath(output_dir)}")
    print(f"📊 Maksimum keyfiyyət: {max_res}p")
    print(f"📋 Video sayı: {len(urls)}")
    
    successful = 0
    failed = 0
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Video yüklənir...")
        
        if download_video(url, output_dir, max_res):
            successful += 1
        else:
            failed += 1
    
    # Nəticə
    print("\n" + "=" * 60)
    print("📊 NƏTİCƏ:")
    print(f"   ✅ Uğurlu: {successful}")
    print(f"   ❌ Uğursuz: {failed}")
    print(f"   📁 Qovluq: {os.path.abspath(output_dir)}")
    print("=" * 60)
    
    return successful, failed

# ═══════════════════════════════════════════════════════════════════════════
# ƏSAS PROQRAM
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if not video_urls:
        print("⚠️  Xəbərdarlıq: video_urls siyahısı boşdur!")
        print("   Lütfən youtube_downloader.py faylında video_urls array-inə linklərinizi əlavə edin.")
        print("\n   Nümunə:")
        print('   video_urls = [')
        print('       "https://www.youtube.com/watch?v=dQw4w9WgXcQ",')
        print('       "https://www.youtube.com/watch?v=VIDEO_ID_2",')
        print('   ]')
        sys.exit(1)
    
    download_all_videos(video_urls)

