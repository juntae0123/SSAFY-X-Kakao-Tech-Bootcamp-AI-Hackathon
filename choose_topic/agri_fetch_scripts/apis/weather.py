"""
기상청 - 단기예보 조회서비스
EP: https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0
주요 농산지 격자 좌표 기준으로 기온/강수량 수집
"""
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import AT_KEY, EP_WEATHER

# 주요 농산지 격자 좌표 (기상청 기준)
REGIONS = [
    {"name": "서울",   "nx": 60, "ny": 127},
    {"name": "전남해남", "nx": 54, "ny": 68},   # 배추 주산지
    {"name": "강원평창", "nx": 73, "ny": 134},  # 고랭지 채소
    {"name": "경북안동", "nx": 91, "ny": 106},  # 마늘 주산지
    {"name": "전북김제", "nx": 63, "ny": 89},   # 쌀·감자
]

def fetch(days_back=3):
    """최근 days_back일 단기예보 수집"""
    rows = []
    base_times = ["0200", "0500", "0800", "1100", "1400", "1700", "2000", "2300"]

    for region in REGIONS:
        print(f"  [기상청] {region['name']} 조회중...")
        # 오늘 기준 최근 발표 시각 사용
        now = datetime.now()
        base_date = now.strftime("%Y%m%d")
        # 가장 최근 발표시각 선택 (현재 시각 기준)
        cur_hour = now.hour
        base_time = "0500"
        for bt in base_times:
            if int(bt[:2]) <= cur_hour:
                base_time = bt

        params = {
            "serviceKey": AT_KEY,
            "pageNo": "1",
            "numOfRows": "1000",
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": region["nx"],
            "ny": region["ny"],
        }
        try:
            r = requests.get(EP_WEATHER + "/getVilageFcst", params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            for d in items:
                d["지역명"] = region["name"]
                d["nx"] = region["nx"]
                d["ny"] = region["ny"]
            rows.extend(items)
            time.sleep(0.3)
        except Exception as e:
            print(f"    ❌ {region['name']} 오류: {e}")

    df = pd.DataFrame(rows)
    print(f"  ✅ 기상청 총 {len(df)}건")
    return df

if __name__ == "__main__":
    df = fetch()
    print(df.head())
