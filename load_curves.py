import ccxt
import pandas as pd


def load_historical_data(sym: str, timeframe: str = '5m') -> pd.DataFrame:
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
                # print('Fetched', len(ohlcvs), symbol, timeframe, 'candles from', exchange.iso8601(ohlcvs[0][0]))
                since = ohlcvs[-1][0] + 1
            else:
                break
        except Exception as e:
            print(type(e).__name__, str(e))

    if len(all_ohlcvs):
        ohlcv_df = pd.DataFrame(all_ohlcvs, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        ohlcv_df['datetime'] = pd.to_datetime(ohlcv_df['datetime'], unit='ms')
        ohlcv_df['date'] = ohlcv_df['datetime'].dt.date
        ohlcv_df['time'] = ohlcv_df['datetime'].dt.time
        return ohlcv_df


def generate_curves(df: pd.DataFrame) -> pd.DataFrame:
    cum_curve_list = []
    bin_curve_list = []
    for obs_date, date_df in df.groupby(by='date'):
        date_df.index = date_df['time']

        cum_curve = date_df['volume'].cumsum() / date_df['volume'].sum()
        cum_curve.name = obs_date
        cum_curve_list.append(cum_curve)

    cum_curve_df = pd.concat(cum_curve_list, axis=1)

    return cum_curve_df


if __name__ == '__main__':
    hist_df = load_historical_data('BTC/USDT')
    cum_curve_df = generate_curves(hist_df)
