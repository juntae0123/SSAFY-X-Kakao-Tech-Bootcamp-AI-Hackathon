"""
한국농수산식품유통공사 - 연월별 도,소매가격정보
EP: https://apis.data.go.kr/B552845/perYearMonth
"""
import requests
import pandas as pd
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import AT_KEY, EP_MONTHLY, ITEMS, START_YM, END_YM

def fetch(start=START_YM, end=END_YM):
    rows = []
    for item in ITEMS:
        print(f"  [연월별] {item['name']} 조회중...")
        params = {
            "serviceKey": AT_KEY,
            "pageNo": "1",
            "numOfRows": "500",
            "returnType": "json",
            "startYearMonth": start,
            "endYearMonth": end,
            "itemCategoryCode": item["category_code"],
            "itemCode": item["item_code"],
        }
        try:
            r = requests.get(EP_MONTHLY + "/selectMonthPriceList", params=params, timeout=15)
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
    print(f"  ✅ 연월별 총 {len(df)}건")
    return df

if __name__ == "__main__":
    df = fetch()
    print(df.head())
