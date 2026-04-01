#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import certifi
import os
import sys

os.environ['SSL_CERT_FILE'] = certifi.where()

from pytubefix import YouTube
from pytubefix.cli import on_progress

DOWNLOAD_DIR = "downloads"

video_urls = [
    "https://www.youtube.com/watch?v=ErfTdRDDqHg&list=RDErfTdRDDqHg&start_radio=1"
]


def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def get_best_720p_stream(yt):
    """720p progressive stream məcburi seç"""
    
    # 🔥 birbaşa 720p axtar
    stream_720 = yt.streams.filter(
        progressive=True,
        file_extension='mp4',
        res="720p"
    ).first()

    if stream_720:
        return stream_720

    # ⚠️ fallback (əgər 720 yoxdursa)
    print("⚠️ 720p tapılmadı, fallback istifadə olunur...")

    return yt.streams.filter(
        progressive=True,
        file_extension='mp4'
    ).order_by('resolution').desc().first()


def download_video(url):
    try:
        print("\n" + "─"*50)
        print(f"🔗 {url}")

        yt = YouTube(url, on_progress_callback=on_progress)
        title = sanitize_filename(yt.title)

        print(f"📹 {yt.title}")

        stream = get_best_720p_stream(yt)

        if not stream:
            print("❌ stream tapılmadı")
            return False

        print(f"📊 Seçilən keyfiyyət: {stream.resolution}")

        if stream.resolution != "720p":
            print("⚠️ BU VIDEO 720P DEYİL!")

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        print("📥 Yüklənir...")
        stream.download(
            output_path=DOWNLOAD_DIR,
            filename=f"{title}.mp4"
        )

        print("✅ DONE")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def download_all_videos(urls):
    print("="*50)
    print("🎬 720P LOCKED DOWNLOADER")
    print("="*50)

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}]")
        download_video(url)


if __name__ == "__main__":
    if not video_urls:
        print("⚠️ Video siyahısı boşdur")
        sys.exit(1)

    download_all_videos(video_urls)