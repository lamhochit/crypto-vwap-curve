# :moneybag: Crypto VWAP Curves

## Motivation
VWAP curve plays an important role in TradFi as it is the basis of many trading algorithms, with VWAP being one of the most common benchmark for execution algorithms. Being able to anticipate volumes going through intraday allows traders to be in line with the market and also take advantage of liquitidy.

Due to TradFi's open/close mechanisms, a "Volume Smile" is using formed, meaning there will be more liquidity at the ends of the open and close auction, forming a smile shape.
<p align="center">
  <img width="500" src='https://github.com/lamhochit/crypto-vwap-curve/blob/main/img/volume_smile.jpg' alt="Volume Smile">
</p>
Traders are expected to participate heavily during the start of the AM session and towards the end of the PM session in order to achieve an average price similar to the market VWAP.

As crypto trades 24/7, we try to explore how the volume profile behaves in crypto.

## Getting Started
The package allows you to easily retrieve historical volumes from Binance and construct their volume profile. `load_historical_data` pulls historical candlesticks from the exchange, `generate_curves` construct curves daily and aggregate them into an average curve.

The below code shows how we construct the cumulative curve for BTC Spot from Binance
```python3
from load_curves import load_historical_data, generate_curves

hist_df = load_historical_data('BTC/USDT')
cum_curve_df = generate_curves(hist_df)
```

## Analysis
Intuitively, without open and close auctions, it is unlikely that a volume smile will be formed in crypto markets. However, it is worth noting that the first bin (UTC 0) stands out. Initial guess for the behavior is that similar to TradFi markets, there is often a fixing for portfolios and people often choose 00:00 as the rebalance time, which leads to a spike in volume.

<img width="500" src='https://github.com/lamhochit/crypto-vwap-curve/blob/main/img/btc_spot_bin.png' alt="BTC Spot Bin Curve"> <img width="500" src='https://github.com/lamhochit/crypto-vwap-curve/blob/main/img/btc_spot_cum.png' alt="BTC Spot Cum Curve">

<img width="500" src='https://github.com/lamhochit/crypto-vwap-curve/blob/main/img/eth_spot_bin.png' alt="ETH Spot Bin Curve"> <img width="500" src='https://github.com/lamhochit/crypto-vwap-curve/blob/main/img/eth_spot_cum.png' alt="ETH Spot Cum Curve">

A similar pattern is also observed for Perps.

<img width="500" src='https://github.com/lamhochit/crypto-vwap-curve/blob/main/img/btc_fut_bin.png' alt="BTC Futures Bin Curve"> <img width="500" src='https://github.com/lamhochit/crypto-vwap-curve/blob/main/img/btc_fut_cum.png' alt="BTC Futures Cum Curve">

<img width="500" src='https://github.com/lamhochit/crypto-vwap-curve/blob/main/img/eth_fut_bin.png' alt="ETH Futures Bin Curve"> <img width="500" src='https://github.com/lamhochit/crypto-vwap-curve/blob/main/img/eth_fut_cum.png' alt="ETH Futures Cum Curve">

However, the volume profile seems to exhibit weak seasonality in 8 hour intervals. Which is likely to be related to the settlement mechanism of perpetual futures (funding rates are paid out every 8 hours).
