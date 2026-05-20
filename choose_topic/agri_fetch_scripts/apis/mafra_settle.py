"""
농림축산식품부 - 정산정보 3종
  - 전국 공영도매시장 정산정보
  - 정산가격 기간별 도매시장별 총물량 총금액
  - 도매시장 산지공판장 정산 가격
"""
import requests
import pandas as pd
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import MAFRA_KEY, START_DATE, END_DATE

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

def _call(url, params, item_name):
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        rows = data.get("data", [])
        if isinstance(rows, list):
            for d in rows:
                d["품목명"] = item_name
        return rows if isinstance(rows, list) else []
    except Exception as e:
        print(f"    ❌ {item_name} 오류: {e}")
        return []

def fetch_settle(start=START_DATE, end=END_DATE):
    """전국 공영도매시장 정산정보 - 최저/최고/평균가"""
    rows = []
    url = "https://at.agromarket.kr/openApi/price/settleList.do"
    for item in MAFRA_ITEMS:
        print(f"  [정산정보] {item['name']} 조회중...")
        params = {
            "apiKey": MAFRA_KEY,
            "pageNo": "1",
            "pageSize": "1000",
            "saleDate": start[:6],
            "itemCode": item["item_code"],
        }
        rows.extend(_call(url, params, item["name"]))
        time.sleep(0.3)
    df = pd.DataFrame(rows)
    print(f"  ✅ 정산정보 총 {len(df)}건")
    return df

def fetch_market(start=START_DATE, end=END_DATE):
    """도매시장별 총물량 총금액"""
    rows = []
    url = "https://at.agromarket.kr/openApi/price/settleMarketList.do"
    for item in MAFRA_ITEMS:
        print(f"  [도매시장별] {item['name']} 조회중...")
        params = {
            "apiKey": MAFRA_KEY,
            "pageNo": "1",
            "pageSize": "500",
            "startDate": start[:6],
            "endDate": end[:6],
            "itemCode": item["item_code"],
        }
        rows.extend(_call(url, params, item["name"]))
        time.sleep(0.3)
    df = pd.DataFrame(rows)
    print(f"  ✅ 도매시장별 총 {len(df)}건")
    return df

def fetch_origin(start=START_DATE, end=END_DATE):
    """산지공판장 정산가격"""
    rows = []
    url = "https://at.agromarket.kr/openApi/price/originList.do"
    for item in MAFRA_ITEMS:
        print(f"  [산지공판장] {item['name']} 조회중...")
        params = {
            "apiKey": MAFRA_KEY,
            "pageNo": "1",
            "pageSize": "500",
            "saleDate": start[:6],
            "itemCode": item["item_code"],
        }
        rows.extend(_call(url, params, item["name"]))
        time.sleep(0.3)
    df = pd.DataFrame(rows)
    print(f"  ✅ 산지공판장 총 {len(df)}건")
    return df

if __name__ == "__main__":
    print(fetch_settle().head())
