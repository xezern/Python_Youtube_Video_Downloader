# 🎬 YouTube Video Downloader

Bu proqram YouTube videolarını **720p keyfiyyətdə** (və ya mövcud ən yüksək ≤720p) yükləyir.

## ✨ Xüsusiyyətlər

- ✅ **Tamamilə pulsuz** - heç bir API açarı tələb etmir
- ✅ **ffmpeg tələb etmir** - video+audio artıq birləşdirilmiş şəkildə yüklənir
- ✅ **720p keyfiyyət** - və ya 720p-ə qədər ən yüksək
- ✅ **Çoxlu video dəstəyi** - siyahıdan birdəfəlik yükləyin
- ✅ **Progress bar** - yükləmə prosesini görün
- ✅ **pytubefix** - ən sabit və aktiv dəstəklənən kitabxana

## 🚀 Quraşdırma

```bash
pip install -r requirements.txt
```

## 📖 İstifadə

1. `youtube_downloader.py` faylını açın
2. `video_urls` array-inə YouTube linklərinizi əlavə edin:

```python
video_urls = [
    'https://www.youtube.com/watch?v=VIDEO_ID_1',
    'https://www.youtube.com/watch?v=VIDEO_ID_2',
    'https://www.youtube.com/watch?v=VIDEO_ID_3',
]
```

3. Proqramı işə salın:

```bash
python youtube_downloader.py
```

Videolar `downloads` qovluğuna yüklənəcək.

## ⚙️ Konfiqurasiya

Faylın yuxarısında bu parametrləri dəyişə bilərsiniz:

```python
DOWNLOAD_DIR = "downloads"  # Yükləmə qovluğu
MAX_RESOLUTION = 720        # Maksimum keyfiyyət (720, 480, 360, etc.)
```

## 📋 Nümunə Çıxış

```
============================================================
   🎬 YOUTUBE VİDEO YÜKLƏYİCİ
   pytubefix ilə - ffmpeg tələb etmir!
============================================================
📁 Yükləmə qovluğu: C:\Users\...\downloads
📊 Maksimum keyfiyyət: 720p
📋 Video sayı: 3

[1/3] Video yüklənir...
────────────────────────────────────────────────────────────
🔗 URL: https://www.youtube.com/watch?v=...
📹 Başlıq: Video Title
⏱️  Uzunluq: 4:32
👁️  Baxış: 1,234,567
📊 Keyfiyyət: 720p
📦 Ölçü: 45.2 MB
📥 Yüklənir...
███████████████████████████████████████ 100%
✅ Uğurla yükləndi!
```

## 🔧 Problemlər və Həllər

### "No suitable stream found" xətası
Video müəyyən ölkələrdə məhdudlaşdırıla bilər. VPN sınaqdan keçirin.

### Yavaş yükləmə
Bu YouTube-un server sürətindən asılıdır, proqramla əlaqəli deyil.

## 📝 Qeyd

Bu proqram yalnız şəxsi istifadə üçündür. YouTube-un xidmət şərtlərinə riayət edin.
