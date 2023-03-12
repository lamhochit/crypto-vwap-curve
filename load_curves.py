import ccxt
import pandas as pd


def load_historical_data(sym: str, timeframe: str = '5m'):
    """load historical data pagination"""
    exchange = ccxt.binance()
    markets = exchange.load_markets()
    since = exchange.parse8601('2022-01-01T00:00:00Z')
    symbol = sym
    timeframe = timeframe
    all_ohlcvs = []
    while True:
        try:
            ohlcvs = exchange.fetch_ohlcv(symbol, timeframe, since)
            all_ohlcvs += ohlcvs
            if len(ohlcvs):
                print('Fetched', len(ohlcvs), symbol, timeframe, 'candles from', exchange.iso8601(ohlcvs[0][0]))
                since = ohlcvs[-1][0] + 1
            else:
                break
        except Exception as e:
            print(type(e).__name__, str(e))

    if len(all_ohlcvs):
        ohlcv_df = pd.DataFrame(all_ohlcvs, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        ohlcv_df['datetime'] = pd.to_datetime(ohlcv_df['datetime'], unit='ms')
        return ohlcv_df


def generate_curves():
    pass


if __name__ == '__main__':
    x = load_historical_data('BTC/USDT')
