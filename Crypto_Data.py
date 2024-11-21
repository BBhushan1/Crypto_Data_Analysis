import requests
import pandas as pd
import time


# API 
API_KEY = "CoinMarketApi_Key"  
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"


PARAMS = {
    "start": 1,          
    "limit": 50,         
    "convert": "USD"    
}

HEADERS = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY
}


# Function to fetch cryptocurrency data
def fetch_crypto_data():
    try:
        response = requests.get(URL, headers=HEADERS, params=PARAMS)
        response.raise_for_status()  
        data = response.json()["data"]

        crypto_data = [
            {
                "Name": item["name"],
                "Symbol": item["symbol"],
                "Current Price (USD)": item["quote"]["USD"]["price"],
                "Market Cap (USD)": item["quote"]["USD"]["market_cap"],
                "24h Volume (USD)": item["quote"]["USD"]["volume_24h"],
                "24h Price Change (%)": item["quote"]["USD"]["percent_change_24h"]
            }
            for item in data
        ]

        return pd.DataFrame(crypto_data)

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    


# Function to perform analysis
def analyze_data(df):
    print("\n--- Analysis ---")
    
  
    top_5 = df.nlargest(5, "Market Cap (USD)")
    print("Top 5 Cryptocurrencies by Market Cap:")
    print(top_5[["Name", "Market Cap (USD)"]])

   
    avg_price = df["Current Price (USD)"].mean()
    print(f"\nAverage Price of Top 50 Cryptocurrencies: ${avg_price:.2f}")

   
    highest_change = df.loc[df["24h Price Change (%)"].idxmax()]
    lowest_change = df.loc[df["24h Price Change (%)"].idxmin()]
    print(f"\nHighest 24h Price Change: {highest_change['Name']} ({highest_change['24h Price Change (%)']:.2f}%)")
    print(f"Lowest 24h Price Change: {lowest_change['Name']} ({lowest_change['24h Price Change (%)']:.2f}%)")


# Function to save data to Excel
def save_to_excel(df, file_name="live_crypto_data.xlsx"):
    try:
        df.to_excel(file_name, index=False)
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error saving to Excel: {e}")

def main():
    while True:
        print("\nFetching cryptocurrency data...")
        df = fetch_crypto_data()
        
        if df is not None:
            analyze_data(df)
            
            save_to_excel(df)
        
        print("\nWaiting for 5 minutes before the next update...\n")
        time.sleep(300)  


if __name__ == "__main__":
    main()
