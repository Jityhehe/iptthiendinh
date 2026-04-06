import requests
from datetime import datetime, timedelta

# Cấu hình
API_URL = "https://sv.thiendinhtv.xyz/api/v1/external/fixtures/unfinished"
FILENAME = "thiendinh.m3u"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def generate_thiendinh():
    fixtures = []
    try:
        res = requests.get(API_URL, headers=HEADERS, timeout=15).json()
        for item in res.get('data', []):
            # Xử lý giờ UTC + 7
            dt_vn = datetime.max
            if item.get('startTime'):
                dt_vn = datetime.strptime(item['startTime'][:19], '%Y-%m-%dT%H:%M:%S') + timedelta(hours=7)
            
            # Lọc link FHD
            for comm_entry in item.get('fixtureCommentators', []):
                comm_data = comm_entry.get('commentator', {})
                nickname = comm_data.get('nickname', 'BLV')
                for s in comm_data.get('streams', []):
                    if "FHD" in s.get('name', '').upper() or "FULLHD" in s.get('name', '').upper():
                        fixtures.append({
                            'time': dt_vn,
                            'title': f"{dt_vn.strftime('%H:%M')} [{item.get('league',{}).get('name','TD')}] {item.get('title')} ({nickname})",
                            'logo': item.get('homeTeam', {}).get('logoUrl', ''),
                            'url': s.get('sourceUrl')
                        })
                        break
        
        # Ghi file M3U
        with open(FILENAME, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            fixtures.sort(key=lambda x: x['time'])
            for item in fixtures:
                f.write(f"#EXTINF:-1 tvg-logo='{item['logo']}' group-title='ThienDinhTV', {item['title']}\n")
                f.write(f"{item['url']}|User-Agent={HEADERS['User-Agent']}\n")
        print(f"Thành công! Đã quét được {len(fixtures)} trận.")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    generate_thiendinh()
