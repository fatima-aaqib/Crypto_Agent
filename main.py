import chainlit as cl # type: ignore
import requests


@cl.on_chat_start
async def start():
    await cl.Message(content="🪙 **Welcome to Crypto Agent**\nType `TOP 10` or `BTC` to get live prices!").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.strip().upper()
    
    # Immediate response to avoid loading
    if user_input == "TOP 10":
        await handle_top_10()
    elif user_input in ["BTC", "ETH", "BNB", "XRP", "ADA", "DOT", "LINK", "LTC", "BCH", "MATIC"]:
        await handle_single_coin(user_input + "USDT")
    elif user_input.endswith("USDT"):
        await handle_single_coin(user_input)
    else:
        await cl.Message(content="❌ Invalid input. Try:\n• `TOP 10` for top coins\n• `BTC` for Bitcoin\n• `ETH` for Ethereum\n• Or any symbol like `BTCUSDT`").send()

async def handle_top_10():
    try:
        # Quick hardcoded popular coins for faster response
        popular_coins = {
            "BTCUSDT": "Bitcoin",
            "ETHUSDT": "Ethereum", 
            "BNBUSDT": "Binance Coin",
            "XRPUSDT": "XRP",
            "ADAUSDT": "Cardano",
            "DOTUSDT": "Polkadot",
            "LINKUSDT": "Chainlink",
            "LTCUSDT": "Litecoin",
            "BCHUSDT": "Bitcoin Cash",
            "MATICUSDT": "Polygon"
        }
        
        result = "🔟 **Top 10 Popular Coins:**\n\n"
        
        for i, (symbol, name) in enumerate(popular_coins.items(), 1):
            try:
                # Quick API call with short timeout
                response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=2)
                
                if response.status_code == 200:
                    data = response.json()
                    price = float(data['price'])
                    result += f"{i}. **{name}**: ${price:,.2f}\n"
                else:
                    result += f"{i}. **{name}**: Price unavailable\n"
            except:
                result += f"{i}. **{name}**: Error fetching price\n"
        
        await cl.Message(content=result).send()
        
    except Exception as e:
        await cl.Message(content="❌ Error fetching top 10 coins. Please try again.").send()

async def handle_single_coin(symbol):
    try:
        # Quick API call
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            price = float(data['price'])
            coin_name = symbol.replace('USDT', '')
            
            await cl.Message(content=f"💰 **{coin_name}**: ${price:,.4f} USDT").send()
        else:
            await cl.Message(content=f"⚠️ Symbol `{symbol}` not found. Try BTC, ETH, BNB, etc.").send()
            
    except requests.exceptions.Timeout:
        await cl.Message(content="⏱️ Request timeout. API is slow, try again.").send()
    except requests.exceptions.ConnectionError:
        await cl.Message(content="🌐 No internet connection. Check your network.").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error: API might be down. Try again later.").send()

