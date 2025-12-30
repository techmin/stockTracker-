from server import predict_trend
import inspect

print(f"Type of predict_trend: {type(predict_trend)}")
print(f"Is coroutine: {inspect.iscoroutinefunction(predict_trend)}")

try:
    # Try calling it synchronously
    print("Calling synchronously...")
    res = predict_trend("AAPL")
    print(f"Result: {res}")
except Exception as e:
    print(f"Sync call failed: {e}")
    
    # Try calling it asynchronously
    import asyncio
    try:
        print("Calling asynchronously...")
        res = asyncio.run(predict_trend("AAPL"))
        print(f"Result: {res}")
    except Exception as e2:
        print(f"Async call failed: {e2}")
