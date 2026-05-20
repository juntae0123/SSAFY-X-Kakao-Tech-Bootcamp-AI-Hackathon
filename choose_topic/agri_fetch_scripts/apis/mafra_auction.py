import requests, pandas as pd, time, sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import AT_KEY, START_DATE, END_DATE
from datetime import datetime, timedelta

URL_ORIGIN   = "https://apis.data.go.kr/B552845/katOrigin/trades"
URL_REALTIME = "https://apis.data.go.kr/B552845/katRealTime2/trades2"

WHSL_CODES = [
    "110001",
    "110008",
    "210001",
    "210009",
    "220001",
    "230001",
    "240001",
    "250001",
]

def _date_range(start, end):
    s = datetime.strptime(start, "%Y%m%d")
    e = datetime.strptime(end, "%Y%m%d")
    s = max(s, e - timedelta(days=30))
    dates = []
    cur = s
    while cur <= e:
        dates.append(cur.strftime("%Y-%m-%d"))
        cur += timedelta(days=1)
    return dates

def _fetch_by_date(url, date, whsl_cd):
    # cond[] 파라미터 인코딩 문제 → URL 직접 조립
    full_url = (
        f"{url}"
        f"?serviceKey={AT_KEY}"
        f"&returnType=json"
        f"&pageNo=1"
        f"&numOfRows=1000"
        f"&cond[whsl_mrkt_cd::EQ]={whsl_cd}"
        f"&cond[trd_clcln_ymd::EQ]={date}"
    )
    try:
        r = requests.get(full_url, timeout=15)
        r.raise_for_status()
        data = r.json()
        items = data.get("response", {}).get("body", {}).get("items", {})
        if not items:
            return []
        items = items.get("item", [])
        if isinstance(items, dict):
            items = [items]
        return items if isinstance(items, list) else []
    except Exception as e:
        print(f"    ❌ {whsl_cd} {date} 오류: {e}")
        return []

def fetch(start=START_DATE, end=END_DATE):
    rows = []
    dates = _date_range(start, end)
    for whsl in WHSL_CODES:
        print(f"  [경매원천] 도매시장:{whsl} ({len(dates)}일치) 조회중...")
        for date in dates:
            result = _fetch_by_date(URL_ORIGIN, date, whsl)
            for d in result:
                d["도매시장코드"] = whsl
            rows.extend(result)
            time.sleep(0.2)
    df = pd.DataFrame(rows)
    print(f"  ✅ 경매원천 총 {len(df)}건")
    return df

def fetch_realtime(start=START_DATE, end=END_DATE):
    rows = []
    dates = _date_range(start, end)
    for whsl in WHSL_CODES:
        print(f"  [실시간경매] 도매시장:{whsl} ({len(dates)}일치) 조회중...")
        for date in dates:
            result = _fetch_by_date(URL_REALTIME, date, whsl)
            for d in result:
                d["도매시장코드"] = whsl
            rows.extend(result)
            time.sleep(0.2)
    df = pd.DataFrame(rows)
    print(f"  ✅ 실시간경매 총 {len(df)}건")
    return df

if __name__ == "__main__":
    print(fetch().head())