import pyairbnb
import parser
import json
import poeIntegration

POE_API_KEY = "wcK0nNN_liw1Q1YLfa7GnIjGY-h1mv_0ORnr3c7S6Ms"

def main():
    print("==Airbnb Listing Details Fetcher==\n")

    # User input
    room_url = input("Enter the Airbnb room URL: ").strip()
    currency = "USD"
    adults = 2
    language = "en"

    # File path to save data
    json_file_path = "details_data.json"

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

    print("Parsing listing details...")
    parsed_data = parser.parse_listing_details(json_file_path)
    parser.write_output_to_file(parsed_data)

    print("Parsed data written to output file.\nDone!")

    print("Sending info to POE bot...")

    poeIntegration.run_ota_analysis(
        api_key=POE_API_KEY,
        file_paths=["details_data.json",
                   "Listing Description.pdf"], #"airbnb-ebook_newbranding_a2.pdf" "22 Quick and Easy Ways to Optimize Your Short-Term Rental Listing in 2024.pdf"
        output_file="ota_grades.txt"
    )

if __name__ == "__main__":
    main()