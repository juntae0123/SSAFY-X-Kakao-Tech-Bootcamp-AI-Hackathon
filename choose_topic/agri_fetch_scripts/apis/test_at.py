import requests, json

KEY = "bc40b706eef57d664eb33632db53b63155d7006c16106c09b9e5edafec1d063c"

url = "https://apis.data.go.kr/B552845/perDay/price"
params = {
    "serviceKey": KEY,
    "returnType": "json",
    "pageNo": "1",
    "numOfRows": "5",
    "cond[exmn_ymd::GTE]": "20260501",
    "cond[exmn_ymd::LTE]": "20260520",
    "cond[ctgry_cd::EQ]": "200",
    "cond[item_cd::EQ]": "211",
}

r = requests.get(url, params=params, timeout=15)
print("STATUS:", r.status_code)
print(json.dumps(r.json(), ensure_ascii=False, indent=2))