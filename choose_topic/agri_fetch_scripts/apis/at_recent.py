import requests, pandas as pd, time, sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import AT_KEY

URL = "https://apis.data.go.kr/B552845/recent/price"

ITEMS_FIXED = [
    {"category_code": "200", "item_code": "211", "name": "배추"},
    {"category_code": "200", "item_code": "231", "name": "무"},
    {"category_code": "200", "item_code": "245", "name": "양파"},
    {"category_code": "200", "item_code": "246", "name": "대파"},
    {"category_code": "100", "item_code": "152", "name": "감자"},
    {"category_code": "100", "item_code": "151", "name": "고구마"},
    {"category_code": "200", "item_code": "244", "name": "마늘"},
    {"category_code": "200", "item_code": "232", "name": "당근"},
    {"category_code": "200", "item_code": "223", "name": "오이"},
    {"category_code": "200", "item_code": "225", "name": "토마토"},
]

def fetch():
    rows = []
    for item in ITEMS_FIXED:
        print(f"  [최근일자] {item['name']} 조회중...")
        params = {
            "serviceKey": AT_KEY,
            "returnType": "json",
            "pageNo": "1",
            "numOfRows": "100",
            "cond[ctgry_cd::EQ]": item["category_code"],
            "cond[item_cd::EQ]": item["item_code"],
        }
        try:
            r = requests.get(URL, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
            items_data = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            if isinstance(items_data, dict):
                items_data = [items_data]
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
    print(fetch().head())