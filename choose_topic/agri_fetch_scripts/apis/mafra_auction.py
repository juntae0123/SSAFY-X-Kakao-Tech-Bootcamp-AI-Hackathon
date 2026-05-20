"""
농림축산식품부 - 전국 공영도매시장 경매원천정보
EP: https://at.agromarket.kr/openApi/price/auctionList.do
품목·등급·거래량·경락가격 원천 데이터
"""
import requests
import pandas as pd
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import MAFRA_KEY, START_DATE, END_DATE

# mafra 품목코드 (aT 코드와 다름)
MAFRA_ITEMS = [
    {"item_code": "1001", "name": "배추"},
    {"item_code": "1002", "name": "무"},
    {"item_code": "1004", "name": "양파"},
    {"item_code": "1003", "name": "대파"},
    {"item_code": "2001", "name": "감자"},
    {"item_code": "2002", "name": "고구마"},
    {"item_code": "1005", "name": "마늘"},
    {"item_code": "1008", "name": "당근"},
    {"item_code": "1010", "name": "오이"},
    {"item_code": "3001", "name": "토마토"},
]

BASE_URL = "https://at.agromarket.kr/openApi/price/auctionList.do"

def fetch(start=START_DATE, end=END_DATE):
    rows = []
    for item in MAFRA_ITEMS:
        print(f"  [경매원천] {item['name']} 조회중...")
        params = {
            "apiKey": MAFRA_KEY,
            "pageNo": "1",
            "pageSize": "1000",
            "saleDate": start[:6],  # YYYYMM
            "itemCode": item["item_code"],
        }
        try:
            r = requests.get(BASE_URL, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
            items_data = data.get("data", [])
            if isinstance(items_data, list):
                for d in items_data:
                    d["품목명"] = item["name"]
                rows.extend(items_data)
            time.sleep(0.3)
        except Exception as e:
            print(f"    ❌ {item['name']} 오류: {e}")
    df = pd.DataFrame(rows)
    print(f"  ✅ 경매원천 총 {len(df)}건")
    return df

if __name__ == "__main__":
    df = fetch()
    print(df.head())
