import time
from datetime import datetime, timedelta

import ccxt
from config import *

# ฟังก์ชันดึงยอดคงเหลือของ BTC
def get_btc_balance(symbol):

    asset = symbol.replace("USDT", "")
    bal = exchange_spot.fetch_balance()
    assets = bal["info"]["balances"]
    for i in range(0, len(assets)):
        if assets[i]["asset"] == asset:
            print("Balance", ":", assets[i]["free"], assets[i]["asset"])

# ฟังก์ชันดึงราคาปัจจุบันของ BTC
def get_btc_current_price(symbol):

    ticker = exchange_spot.fetch_ticker(symbol)

    return ticker["last"]

# ฟังก์ชันสร้างคำสั่งซื้อ BTC
def binance_buy_spot(symbol, usdt_amount):

    # ดึงราคาปัจจุบันของ BTC
    current_price = get_btc_current_price(symbol)

    # คำนวณจำนวน BTC ที่จะซื้อ
    btc_amount = round(usdt_amount / current_price, 8)

    # สร้างคำสั่งซื้อ BTC แบบราคาตลาด
    exchange_spot.create_order(symbol=symbol,
                               type="market",
                               side="buy",
                               amount=btc_amount)

    # แสดงยอดคงเหลือของ BTC
    get_btc_balance(symbol)

# ฟังก์ชันคำนวณเวลาในการรันโปรแกรม
def get_next_run_time(start_time, interval_minutes):

    # คำนวณเวลาถัดไปที่ควรรัน โดยเริ่มต้นจาก start_time และเพิ่มทีละ interval_minutes
    now = datetime.now()
    next_run = start_time

    # เพิ่มรอบเวลาจนกว่าจะแน่ใจว่า next_run อยู่ในอนาคต
    while next_run <= now:
        next_run += timedelta(minutes=interval_minutes)
    return next_run

if __name__ == "__main__":

    try:
        # กำหนดเวลาเริ่มต้น (เริ่มที่ 7:00) โดยเลือกใช้เวลาตามนาฬิกาไทยคือ 0-23 น.
        start_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)

        # กำหนดรอบเวลาที่จะรัน (1440 นาที)
        interval_minutes = 1440
        next_run_time = get_next_run_time(start_time, interval_minutes)

        while True:
            # เช็คเวลาปัจจุบัน
            now = datetime.now()

            # รอจนถึงเวลาถัดไป
            if now >= next_run_time:
                print(f"เริ่มงานที่ {now.strftime('%Y-%m-%d %H:%M:%S')}")

                exchange_spot = ccxt.binance({"apiKey": BINANCE_SPOT_API_KEY,
                                              "secret": BINANCE_SPOT_API_SECRET,
                                              "options": {"defaultType": "spot"}
                                              }
                                            )

                # สร้างออเดอร์ไปที่ Binance Exchange #
                SYMBOL = "BTCUSDT"
                USDT_AMOUNT = 10
                binance_buy_spot(SYMBOL, USDT_AMOUNT)

                # อัปเดตเวลาถัดไป
                next_run_time += timedelta(minutes=interval_minutes)

            # รอจนถึงเวลาถัดไป
            sleep_duration = (next_run_time - datetime.now()).total_seconds()
            if sleep_duration > 0:
                time.sleep(sleep_duration)

    except Exception as e:
        print(f"Error: {e}")