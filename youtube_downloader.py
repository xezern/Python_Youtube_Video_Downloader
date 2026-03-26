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
    "https://www.youtube.com/watch?v=KBMtW8JEQRs&list=RDKBMtW8JEQRs&start_radio=1&pp=ygUTdGFsaWIgdGFsZSBpbGtiYWhhcqAHAQ%3D%3D",
    "https://www.youtube.com/watch?v=BoMrp_oerDc&list=RDBoMrp_oerDc&start_radio=1&pp=ygUPbmlnYXIgbmV5bGVzZW4goAcB",
    "https://www.youtube.com/watch?v=DKGuEU5SEdg&list=RDDKGuEU5SEdg&start_radio=1&pp=ygUWYWwgcWlybWl6aSB5YW5hcWxhcmluIKAHAQ%3D%3D",
    "https://www.youtube.com/watch?v=-7ClRrEjPJQ&list=RD-7ClRrEjPJQ&start_radio=1&pp=ygUqYXh0YXLEsSBiYXJhbcSxc2FuICBiYcWfxLFtxLFuIGLJmWxhc8Sxc2FuoAcB",
    "https://www.youtube.com/watch?v=1mp9C-4L8VI&list=RD1mp9C-4L8VI&start_radio=1&pp=ygUQbWVoaW4gYcSfYWxhcm92YaAHAQ%3D%3D",
    "https://www.youtube.com/watch?v=TkJRmlOVwi8&list=RDTkJRmlOVwi8&start_radio=1&pp=ygUQbWVoaW4gYcSfYWxhcm92YaAHAQ%3D%3D",
    "https://www.youtube.com/watch?v=V5JdeAXUj9Y&list=RDV5JdeAXUj9Y&start_radio=1&pp=ygUQbWVoaW4gYcSfYWxhcm92YaAHAQ%3D%3D",
    "https://www.youtube.com/watch?v=NnXju1p36eA&list=RDNnXju1p36eA&start_radio=1&pp=ygUPaWxraW4gyZlobcmZZG92oAcB",
    "https://www.youtube.com/watch?v=7zYTFD-yHQ0&list=RD7zYTFD-yHQ0&start_radio=1&pp=ygUPaWxraW4gyZlobcmZZG92oAcB",
    "https://www.youtube.com/watch?v=9wO7dYSdfPI&list=RD9wO7dYSdfPI&start_radio=1&pp=ygUPaWxraW4gyZlobcmZZG92oAcB",
    "https://www.youtube.com/watch?v=WdzCI0a_4Uw&list=RDWdzCI0a_4Uw&start_radio=1&pp=ygUPaWxraW4gyZlobcmZZG92oAcB"
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