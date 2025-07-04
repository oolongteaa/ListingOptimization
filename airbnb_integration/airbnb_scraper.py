import pyairbnb
import json

def fetch_airbnb_listing(room_url, json_file_path="details_data.json", currency="USD", adults=2, language="en"):
    print("\nFetching data from Airbnb...")
    data = pyairbnb.get_details(
        room_url=room_url,
        currency=currency,
        adults=adults,
        language=language
    )

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Raw listing data saved to {json_file_path}")
    return json_file_path