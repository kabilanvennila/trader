from nsepython import nse_optionchain_scrapper

def get_option_ltp(symbol="NIFTY", expiry=None, strike=None, option_type="CE"):
    """
    symbol: e.g. "NIFTY", "BANKNIFTY"
    expiry: exact expiry date string, e.g. "10-Oct-2025"
    strike: int (strike price)
    option_type: "CE" or "PE"
    """
    data = nse_optionchain_scrapper(symbol)
    records = data['records']['data']

    for record in records:
        if record.get("strikePrice") == strike and record.get("expiryDate") == expiry:
            if option_type in record:
                option_data = record[option_type]
                return {
                    "symbol": symbol,
                    "expiry": record["expiryDate"],
                    "strike": strike,
                    "optionType": option_type,
                    "ltp": option_data.get("lastPrice"),
                    "change": option_data.get("change"),
                    "bidQty": option_data.get("bidQty"),
                    "askQty": option_data.get("askQty"),
                    "openInterest": option_data.get("openInterest"),
                    "iv": option_data.get("impliedVolatility")
                }
    return None

def get_expiries(symbol="NIFTY"):
    data = nse_optionchain_scrapper(symbol)
    return data["records"]["expiryDates"]

def get_strikes(symbol="NIFTY", expiry=None):
    data = nse_optionchain_scrapper(symbol)
    strikes = []
    for rec in data['records']['data']:
        if rec['expiryDate'] == expiry:
            strikes.append(rec['strikePrice'])
    return sorted(list(set(strikes)))