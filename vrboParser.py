import re
import json

def extract_vrbo_listing_info(data):
    # Title from first <h1>
    title = next(
        (item["text"].strip()
         for item in data
         if item.get("tag") == "h1" and item.get("text")), None)

    # About section: look for section with "About this property"
    about_section = next(
        (item["text"].strip()
         for item in data
         if isinstance(item.get("text"), str)
         and "About this property" in item["text"]), None)

    # Overview block: gather amenities, rooms, and layout text
    overview_candidates = [
        item["text"].strip()
        for item in data
        if isinstance(item.get("text"), str)
        and re.search(r"(?i)(sleeps|bedroom|bathroom|deck|kitchen|washer|dryer|air conditioning|wifi|fireplace|overview|parking)", item["text"])
    ]
    overview_text = "\n".join(dict.fromkeys(overview_candidates)) if overview_candidates else None

    # Image captions from <figure> elements
    image_captions = []
    seen = set()
    for item in data:
        if item.get("tag") == "figure":
            caption = item.get("text", "").strip()
            if caption and caption not in seen:
                image_captions.append(caption)
                seen.add(caption)

    return {
        "title": title,
        "about_this_property": about_section,
        "overview_excerpt": overview_text,
        "image_captions": image_captions
    }

def main():
    # Example usage:
    with open("vrbo_details_data.json", encoding="utf-8") as f:
        data = json.load(f)

    parsed = extract_vrbo_listing_info(data)
    print(json.dumps(parsed, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
