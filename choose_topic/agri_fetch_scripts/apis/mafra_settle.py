import pandas as pd

def fetch_settle():
    print("  [정산정보] 이관 API 없음 → 스킵")
    return pd.DataFrame()

def fetch_market():
    print("  [도매시장별] 이관 API 없음 → 스킵")
    return pd.DataFrame()

def fetch_origin():
    print("  [산지공판장] 이관 API 없음 → 스킵")
    return pd.DataFrame()