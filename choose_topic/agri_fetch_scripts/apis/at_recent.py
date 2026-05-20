"""
한국농수산식품유통공사 - 최근일자 도,소매가격정보
EP: https://apis.data.go.kr/B552845/recent
기준일로부터 1일/1주/1개월/1년 전 평균가격 제공
"""
import requests
import pandas as pd
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import AT_KEY, EP_RECENT, ITEMS

def fetch():
    rows = []
    for item in ITEMS:
        print(f"  [최근일자] {item['name']} 조회중...")
        params = {
            "serviceKey": AT_KEY,
            "pageNo": "1",
            "numOfRows": "100",
            "returnType": "json",
            "itemCategoryCode": item["category_code"],
            "itemCode": item["item_code"],
        }
        try:
            r = requests.get(EP_RECENT + "/selectRecentPriceList", params=params, timeout=15)
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
    print(f"  ✅ 최근일자 총 {len(df)}건")
    return df

if __name__ == "__main__":
    df = fetch()
    print(df.head())
