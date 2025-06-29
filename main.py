from airbnbIntegration import airbnbParser, airbnbScraper
import poeIntegration

POE_API_KEY = "your poe api key here"

def main():
    print("==Listing Optimization App==\n")

    room_url = input("Enter the Airbnb room URL: ").strip()

    # Fetch and save Airbnb data
    json_file_path = airbnbScraper.fetch_airbnb_listing(room_url)

    # Parse and write output
    print("Parsing listing details...")
    parsed_data = airbnbParser.parse_listing_details(json_file_path)
    airbnbParser.write_output_to_file(parsed_data)
    print("Parsed data written to output file.\nDone!")

    #  POE bot analysis
    print("Sending info to POE bot...")
    poeIntegration.run_ota_analysis(
        api_key=POE_API_KEY,
        file_paths=[
            "output.txt",
            "resources/Listing Description.pdf",
        ],
        output_file="ota_grades.txt"
    )

if __name__ == "__main__":
    main()
