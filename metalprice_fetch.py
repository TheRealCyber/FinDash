import requests

API_KEY = "17b8c24671b6199a906d981296df4a29"
BASE_URL = "https://api.metalpriceapi.com/v1/latest"

def fetch_metal_prices(base="INR", currencies="USD,EUR"):
    """
    Fetch latest metal & currency prices from MetalPriceAPI.
    Returns a dict of rates relative to the given base currency.
    """
    params = {"api_key": API_KEY, "base": base, "currencies": currencies}
    response = requests.get(BASE_URL, params=params, timeout=30)
    data = response.json()

    if not data.get("success", False):
        print("❌ API Error:", data.get("error", {}).get("info", "Unknown error"))
        return None
    return data


if __name__ == "__main__":
    result = fetch_metal_prices(base="INR", currencies="USD,EUR")

    if not result:
        exit()

    print("\n💰 Latest Currency Prices (Base: INR)\n")

    rates = result.get("rates", {})

    for code, val in rates.items():
        # skip synthetic or malformed keys like 'INREUR', 'INRUSD'
        if not code.isalpha() or len(code) != 3:
            continue
        if val == 0:
            continue

        # Flip rate so we show 1 target = ? INR
        inr_value = 1 / val
        print(f"1 {code:<3} ≈ ₹ {inr_value:,.2f}")
