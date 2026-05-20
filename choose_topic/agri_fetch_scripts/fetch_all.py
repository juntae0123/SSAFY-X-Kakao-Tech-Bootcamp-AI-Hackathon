"""
fetch_all.py - 전체 API 호출 및 데이터 저장 진입점

실행:
    python fetch_all.py

결과:
    data/
    ├── at_daily.csv / .pkl
    ├── at_recent.csv / .pkl
    ├── at_monthly.csv / .pkl
    ├── at_regional.csv / .pkl
    ├── mafra_auction.csv / .pkl
    ├── mafra_settle.csv / .pkl
    ├── mafra_market.csv / .pkl
    ├── mafra_origin.csv / .pkl
    ├── weather.csv / .pkl
    └── embeddings/items_embedding.pkl
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from apis.at_daily    import fetch as fetch_daily
from apis.at_recent   import fetch as fetch_recent
from apis.at_monthly  import fetch as fetch_monthly
from apis.at_regional import fetch as fetch_regional
from apis.mafra_auction import fetch as fetch_auction
from apis.mafra_settle  import fetch_settle, fetch_market, fetch_origin
from apis.weather       import fetch as fetch_weather
from save import save, make_embeddings

def main():
    print("=" * 50)
    print("🌾 농산물 데이터 수집 시작")
    print("=" * 50)

    results = {}

    # ── aT 농수산식품유통공사 ──────────────────────────
    print("\n📦 [1/4] aT 일별 도·소매 가격")
    results["at_daily"] = fetch_daily()
    save(results["at_daily"], "at_daily")

    print("\n📦 [2/4] aT 최근일자 가격")
    results["at_recent"] = fetch_recent()
    save(results["at_recent"], "at_recent")

    print("\n📦 [3/4] aT 연월별 가격")
    results["at_monthly"] = fetch_monthly()
    save(results["at_monthly"], "at_monthly")

    print("\n📦 [4/4] aT 지역별 품목별 가격")
    results["at_regional"] = fetch_regional()
    save(results["at_regional"], "at_regional")

    # ── 농림축산식품부 도매시장 ──────────────────────────
    print("\n🏪 [5/8] 전국 공영도매시장 경매원천정보")
    results["mafra_auction"] = fetch_auction()
    save(results["mafra_auction"], "mafra_auction")

    print("\n🏪 [6/8] 전국 공영도매시장 정산정보")
    results["mafra_settle"] = fetch_settle()
    save(results["mafra_settle"], "mafra_settle")

    print("\n🏪 [7/8] 도매시장별 총물량 총금액")
    results["mafra_market"] = fetch_market()
    save(results["mafra_market"], "mafra_market")

    print("\n🏪 [8/8] 산지공판장 정산가격")
    results["mafra_origin"] = fetch_origin()
    save(results["mafra_origin"], "mafra_origin")

    # ── 기상청 ──────────────────────────────────────────
    print("\n🌤️  [+] 기상청 단기예보 (주요 농산지 5개)")
    results["weather"] = fetch_weather()
    save(results["weather"], "weather")

    # ── 임베딩 ──────────────────────────────────────────
    print("\n🧠 임베딩 생성중...")
    make_embeddings(results)

    # ── 요약 ────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("✅ 수집 완료 요약")
    print("=" * 50)
    for name, df in results.items():
        if df is not None and not df.empty:
            print(f"  {name:20s}: {len(df):>6,}행  {list(df.columns[:4])}")
        else:
            print(f"  {name:20s}: ❌ 데이터 없음")

if __name__ == "__main__":
    main()
