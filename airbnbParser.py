import json


def parse_listing_details(json_file_path):
    """
    Parses the JSON file to extract the title, description, photos, and reviews.
    """
    try:
        # Load the JSON file
        with open(json_file_path, 'r', encoding="utf8") as file:
            data = json.load(file)

        # Retrieve the listing title
        title = data.get("title", "No title found")

        # Retrieve the description
        description = data.get("description", "No description found")

        # Retrieve photos and captions
        photos = data.get("images", [])
        photo_details = []
        for photo in photos:
            photo_title = photo.get("title", "No caption available")
            photo_url = photo.get("url", "No URL available")
            photo_details.append({"caption": photo_title, "url": photo_url})

        # Retrieve reviews
        reviews = data.get("reviews", [])
        review_details = []
        for review in reviews:
            reviewer_name = review.get("reviewer", {}).get("firstName", "Anonymous")
            review_text = review.get("comments", "No review text available")
            review_date = review.get("createdAt", "No date available")
            review_details.append({
                "name": reviewer_name,
                "date": review_date,
                "text": review_text
            })

        # Return the extracted details
        return {
            "title": title,
            "description": description,
            "photos": photo_details,
            "reviews": review_details
        }

    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{json_file_path}' contains invalid JSON.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def write_output_to_file(output_data, output_file_path="output.txt"):
    """
    Writes the parsed listing details to a file in a readable format.
    """
    try:
        with open(output_file_path, 'w', encoding="utf8") as file:
            # Write the title
            file.write(f"Title: {output_data['title']}\n\n")

            # Write the description
            file.write(f"Description:\n{output_data['description']}\n\n")

            # Write the photos
            file.write("Photos:\n")
            for index, photo in enumerate(output_data["photos"], start=1):
                file.write(f"  {index}. Caption: {photo['caption']}\n")
                file.write(f"     URL: {photo['url']}\n")

            # Write the reviews
            file.write("\nReviews:\n")
            if output_data["reviews"]:
                for index, review in enumerate(output_data["reviews"], start=1):
                    file.write(f"  {index}. Reviewer: {review['name']}\n")
                    file.write(f"     Date: {review['date']}\n")
                    file.write(f"     Review: {review['text']}\n")
            else:
               file.write("  No reviews available.\n")

        print(f"Output successfully written to '{output_file_path}'")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


# Example usage
if __name__ == "__main__":
    # Path to your JSON file
    json_file_path = "details_data.json"

    # Parse the JSON file
    listing_details = parse_listing_details(json_file_path)

    # Write the output to a file if parsing was successful
    if listing_details:
        write_output_to_file(listing_details, "output.txt")