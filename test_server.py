from server import predict_trend, get_stock_price, get_stock_info
import asyncio

async def main():
    print("--- Testing predict_trend ---")
    # FastMCP tools are often async or wrapped, but let's try calling them directly first.
    # If they are async, we await them. If they are sync, we call them.
    try:
        res = await predict_trend("AAPL") if asyncio.iscoroutinefunction(predict_trend) else predict_trend("AAPL")
        print(res)
    except Exception as e:
        print(f"Error calling predict_trend: {e}")

    print("\n--- Testing get_stock_price ---")
    try:
        res = await get_stock_price("AAPL") if asyncio.iscoroutinefunction(get_stock_price) else get_stock_price("AAPL")
        print(res)
    except Exception as e:
        print(f"Error calling get_stock_price: {e}")
        
    print("\n--- Testing get_stock_info ---")
    try:
        # Resources might be different, they usually take a URI.
        # But here we defined the function get_stock_info.
        # FastMCP resources might not be directly callable as functions with the URI template logic handled automatically.
        # We will try calling the underlying function if possible.
        res = await get_stock_info("AAPL") if asyncio.iscoroutinefunction(get_stock_info) else get_stock_info("AAPL")
        print(res)
    except Exception as e:
        print(f"Error calling get_stock_info: {e}")

if __name__ == "__main__":
    asyncio.run(main())
