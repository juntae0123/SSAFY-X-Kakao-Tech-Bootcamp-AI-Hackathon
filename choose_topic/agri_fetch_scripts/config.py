# ============================================================
# 설정값 로더 - .env 파일에서 읽어옴
# ============================================================
import os
from dotenv import load_dotenv

load_dotenv()

# ── 인증키 ──────────────────────────────────────────────────
AT_KEY    = os.getenv("DATA_GO_KR_KEY", "")
MAFRA_KEY = os.getenv("MAFRA_KEY", "")
KAMIS_KEY = os.getenv("KAMIS_KEY", "")
KAMIS_ID  = os.getenv("KAMIS_ID", "")

# ── 엔드포인트 ───────────────────────────────────────────────
EP_DAILY    = "https://apis.data.go.kr/B552845/perDay"
EP_RECENT   = "https://apis.data.go.kr/B552845/recent"
EP_MONTHLY  = "https://apis.data.go.kr/B552845/perYearMonth"
EP_REGIONAL = "https://apis.data.go.kr/B552845/perRegion"

EP_MAFRA_AUCTION = "https://at.agromarket.kr/openApi/price/auctionList.do"
EP_MAFRA_SETTLE  = "https://at.agromarket.kr/openApi/price/settleList.do"
EP_MAFRA_MARKET  = "https://at.agromarket.kr/openApi/price/settleMarketList.do"
EP_MAFRA_ORIGIN  = "https://at.agromarket.kr/openApi/price/originList.do"

EP_WEATHER = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"

# ── 기간 ─────────────────────────────────────────────────────
START_DATE = os.getenv("START_DATE", "20250520")
END_DATE   = os.getenv("END_DATE",   "20260520")
START_YM   = os.getenv("START_YM",   "202505")
END_YM     = os.getenv("END_YM",     "202605")

# ── 품목 10개 ────────────────────────────────────────────────
ITEMS = [
    {"category_code": "200", "item_code": "211", "name": "배추"},
    {"category_code": "200", "item_code": "212", "name": "무"},
    {"category_code": "200", "item_code": "215", "name": "양파"},
    {"category_code": "200", "item_code": "216", "name": "대파"},
    {"category_code": "100", "item_code": "112", "name": "감자"},
    {"category_code": "100", "item_code": "113", "name": "고구마"},
    {"category_code": "200", "item_code": "214", "name": "마늘"},
    {"category_code": "200", "item_code": "233", "name": "당근"},
    {"category_code": "200", "item_code": "251", "name": "오이"},
    {"category_code": "400", "item_code": "411", "name": "토마토"},
]

# ── 기상청 서울 격자 ─────────────────────────────────────────
WEATHER_NX = 60
WEATHER_NY = 127

# ── 저장 경로 ────────────────────────────────────────────────
DATA_DIR = os.getenv("DATA_DIR", "data")

# ── 키 누락 경고 ─────────────────────────────────────────────
if not AT_KEY:
    print("⚠️  DATA_GO_KR_KEY 없음 → .env 확인하세요")
if not MAFRA_KEY:
    print("⚠️  MAFRA_KEY 없음 → .env 확인하세요")
