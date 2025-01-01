import websocket
import json
import subprocess

notification_count=0
alert_price=92350

def on_message(ws, message):
    global notification_count
    data = json.loads(message)
    current_price = data['k']['c']
    if float(current_price)>alert_price and notification_count==0:
        subprocess.run(["notify-send", "BTCUSD Alert", f"Price crossed {alert_price} and current price is {current_price}."])
        subprocess.run(["mpg123", "alert.mp3"])
        notification_count=1
    print(data['k']['c'])

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    # Subscribe to the real-time price updates for the given symbol
    symbol = 'btcusdt'
    ws.send(json.dumps({"method": "SUBSCRIBE", "params": [f"{symbol}@kline_1m"], "id": 1}))

def main():
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws", on_message = on_message, on_error = on_error, on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    
main()
