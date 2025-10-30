import time
import random
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# --- Flask Initialization ---
app = Flask(__name__)
CORS(app)

# --- MongoDB Connection ---
MONGO_CONNECTION_STRING = "mongodb+srv://rjbijumass:lj5cMiQDHJcLBvnq@cluster0.bktha79.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
try:
    client = MongoClient(MONGO_CONNECTION_STRING)
    db = client.market_db
    commodity_collection = db.commodity_prices
    client.admin.command('ping')
    print("✅ MongoDB connection successful.")
except Exception as e:
    print(f"⚠️ MongoDB connection error: {e}")
    plants_collection = None


# --- Helper Functions ---
def script(state, commodity, market):
    """Scrape Agmarknet using Selenium."""
    url = "https://agmarknet.gov.in/SearchCmmMkt.aspx"
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        Select(driver.find_element("id", 'ddlCommodity')).select_by_visible_text(commodity)
        Select(driver.find_element("id", 'ddlState')).select_by_visible_text(state)

        date_input = driver.find_element(By.ID, "txtDate")
        date_input.clear()
        date_input.send_keys((datetime.now() - timedelta(days=7)).strftime('%d-%b-%Y'))
        driver.find_element("id", 'btnGo').click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ddlMarket')))
        Select(driver.find_element("id", 'ddlMarket')).select_by_visible_text(market)
        driver.find_element("id", 'btnGo').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cphBody_GridPriceData')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        data_list, jsonList = [], []
        for row in soup.find_all("tr"):
            data_list.append(row.text.replace("\n", "_").replace("\xa0", "").split("__"))

        if len(data_list) > 5:
            for i in data_list[4:-1]:
                try:
                    jsonList.append({
                        "S.No": i[1],
                        "City": i[2],
                        "Commodity": i[4],
                        "Min Price": i[7],
                        "Max Price": i[8],
                        "Model Price": i[9],
                        "Date": i[10]
                    })
                except IndexError:
                    continue
        return jsonList
    finally:
        driver.quit()


def scrape_agmarknet():
    """Scrapes agmarknet.gov.in using requests."""
    try:
        url = 'https://agmarknet.gov.in/PriceAndArrivals/DatewiseCommodityReport.aspx'
        headers = {'User-Agent': 'Mozilla/5.0'}
        soup = BeautifulSoup(requests.get(url, headers=headers, timeout=20).text, 'html.parser')
        tables = soup.find_all('table')

        for table in tables:
            header_row = table.find('tr')
            if header_row and 'commodity' in header_row.text.lower():
                target = table
                break
        else:
            return []

        data = []
        for row in target.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) > 7:
                try:
                    min_price, max_price = float(cols[5].text.strip()), float(cols[6].text.strip())
                except ValueError:
                    continue
                data.append({
                    "commodity_name": cols[2].text.strip(),
                    "market": cols[1].text.strip(),
                    "price_text": f"₹{min_price} - ₹{max_price}/Quintal",
                    "avg_price": (min_price + max_price) / 2
                })
        return data
    except Exception as e:
        print("Scraping error:", e)
        return []


def get_mock_weather_data(city):
    weather = {
        "delhi": {"temp": 34, "condition": "Hazy Sunshine"},
        "mumbai": {"temp": 30, "condition": "Cloudy with Showers"},
        "bengaluru": {"temp": 28, "condition": "Partly Cloudy"}
    }
    return weather.get(city.lower())


# --- API Routes ---
@app.route('/')
def home():
    return jsonify({"message": "Market Scraper API", "status": "OK"})


@app.route('/request', methods=['GET'])
def request_data():
    commodity = request.args.get('commodity')
    state = request.args.get('state')
    market = request.args.get('market')
    if not all([commodity, state, market]):
        return jsonify({"error": "Missing query parameters"}), 400
    return jsonify(script(state, commodity, market))


@app.route('/get_prices', methods=['GET'])
def get_prices():
    """Fetch all commodity price data from MongoDB (market_db.commodity_prices)."""
    if commodity_collection is None:
        return jsonify({"error": "Database not connected"}), 503

    try:
        # Fetch everything except MongoDB's _id field
        data = list(commodity_collection.find({}, {"_id": 0}))
        random.shuffle(data)
        return jsonify(data[:20])  # send first 20 records
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'delhi')
    weather = get_mock_weather_data(city)
    return jsonify(weather if weather else {"error": "No data"})


@app.route('/calculate_profit', methods=['POST'])
def calculate_profit():
    data = request.get_json()
    try:
        commodity = data['commodity_name']
        cost = float(data['cost_price'])
        qty = float(data['quantity'])
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

    live_prices = scrape_agmarknet()
    market_data = next((p for p in live_prices if p['commodity_name'] == commodity), None)
    if not market_data:
        return jsonify({"error": "Commodity not found"}), 404

    market_price = market_data['avg_price']
    total_profit = (market_price - cost) * qty

    return jsonify({
        "commodity": commodity,
        "market_price": f"₹{market_price:.2f}/Quintal",
        "profit_per_quintal": f"₹{market_price - cost:.2f}",
        "total_profit": f"₹{total_profit:.2f}"
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
