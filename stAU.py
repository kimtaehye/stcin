import time
import pyupbit
import datetime

access = ""
secret = ""

# def get_target_price(ticker, k):
#     """변동성 돌파 전략으로 매수 목표가 조회"""
#     df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
#     target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
#     return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1) #ohlcv: open, high, low, close, volume 당일 시가, 고가, 저가, 종가, 거래량
    start_time = df.index[0] #첫번째 값이 시간값이므로 index[시간값] 받아옴
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def select_coin():
    for i in range(101):
        df = pyupbit.get_ohlcv(tickers[i], interval="day", count=1)
        if pyupbit.get_orderbook(tickers=tickers[i])[0]["orderbook_units"][0]["ask_price"]/df.iloc[0]['open'] >= 1.018:
            slt_list.append(tickers[i])
        time.sleep(0.01)

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC") # 9:00
        end_time = start_time + datetime.timedelta(minutes=4) # 9:04

        tickers=pyupbit.get_tickers(fiat="KRW")
        slt_list=[]

        if start_time:
            while len(slt_list())==0:
                select_coin()
                

            # target_price = get_target_price("KRW-BTC", 0.5)
            # current_price = get_current_price("KRW-BTC")
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order(slt_list[0], krw*0.995)

            df = pyupbit.get_ohlcv(slt_list[0], interval="day", count=1)
            # while get_balance(slt_list[0])>=1 and pyupbit.get_orderbook(ticksers=slt_list[0])["orderbook_units"][0]["ask_price"]/df.iloc[0]['open'] >= 1.05:
            #     if pyupbit.get_orderbook(ticksers=slt_list[0])["orderbook_units"][0]["ask_price"]/df.iloc[0]['open'] >= 1.07:

        if pyupbit.get_orderbook(ticksers=slt_list[0])["orderbook_units"][0]["ask_price"]/df.iloc[0]['open'] >= 1.15:
            upbit.sell_market_order(slt_list[0], slt_list[0]*0.9995)
        time.sleep(0.1)
    except Exception as e:
        print(e)
        time.sleep(1)
