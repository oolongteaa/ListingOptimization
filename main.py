from airbnb_integration import airbnb_parser, airbnb_scraper
import poe_integration

POE_API_KEY = "wcK0nNN_liw1Q1YLfa7GnIjGY-h1mv_0ORnr3c7S6Ms"

def main():
    print("==Listing Optimization App==\n")

    room_url = input("Enter the Airbnb room URL: ").strip()

    # Fetch and save Airbnb data
    json_file_path = airbnb_scraper.fetch_airbnb_listing(room_url)

    # Parse and write output
    print("Parsing listing details...")
    parsed_data = airbnb_parser.parse_listing_details(json_file_path)
    airbnb_parser.write_output_to_file(parsed_data)
    print("Parsed data written to output file.\nDone!")

    #  POE bot analysis
    print("Sending info to POE bot...")
    poe_integration.run_ota_analysis(
        api_key=POE_API_KEY,
        file_paths=[
            "output.txt",
            "resources/Listing Description.pdf",
        ],
        output_file="ota_grades.txt"
    )

if __name__ == "__main__":
    main()
