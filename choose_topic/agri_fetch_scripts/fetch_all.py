import sys
import os
sys.path.append(os.path.dirname(__file__))

from apis.at_daily    import fetch as fetch_daily
from apis.at_recent   import fetch as fetch_recent
from apis.at_monthly  import fetch as fetch_monthly
from apis.at_regional import fetch as fetch_regional
from apis.mafra_auction import fetch as fetch_auction, fetch_realtime
from apis.weather       import fetch as fetch_weather
from save import save, make_embeddings

def main():
    print("=" * 50)
    print("🌾 농산물 데이터 수집 시작")
    print("=" * 50)

    results = {}

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

    print("\n🏪 [5/6] 전국 공영도매시장 경매원천정보")
    results["mafra_auction"] = fetch_auction()
    save(results["mafra_auction"], "mafra_auction")

    print("\n🏪 [6/6] 전국 공영도매시장 실시간 경매정보")
    results["mafra_realtime"] = fetch_realtime()
    save(results["mafra_realtime"], "mafra_realtime")

    print("\n🌤️  [+] 기상청 단기예보 (주요 농산지 5개)")
    results["weather"] = fetch_weather()
    save(results["weather"], "weather")

    print("\n🧠 임베딩 생성중...")
    make_embeddings(results)

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