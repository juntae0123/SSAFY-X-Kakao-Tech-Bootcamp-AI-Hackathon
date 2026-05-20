"""
한국농수산식품유통공사 - 지역별 품목별 도,소매 가격정보
EP: https://apis.data.go.kr/B552845/perRegion
전국 시군구별 가격 비교 → 최적 구매처 핵심
"""
import requests
import pandas as pd
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import AT_KEY, EP_REGIONAL, ITEMS, START_DATE, END_DATE

def fetch(start=START_DATE, end=END_DATE):
    rows = []
    for item in ITEMS:
        print(f"  [지역별] {item['name']} 조회중...")
        params = {
            "serviceKey": AT_KEY,
            "pageNo": "1",
            "numOfRows": "1000",
            "returnType": "json",
            "startDay": start,
            "endDay": end,
            "itemCategoryCode": item["category_code"],
            "itemCode": item["item_code"],
        }
        try:
            r = requests.get(EP_REGIONAL + "/selectRegionPriceList", params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
            items_data = data.get("data", {}).get("item", [])
            for d in items_data:
                d["품목명"] = item["name"]
            rows.extend(items_data)
            time.sleep(0.3)
        except Exception as e:
            print(f"    ❌ {item['name']} 오류: {e}")
    df = pd.DataFrame(rows)
    print(f"  ✅ 지역별 총 {len(df)}건")
    return df

if __name__ == "__main__":
    df = fetch()
    print(df.head())
