import fastapi_poe as fp
from pathlib import Path
from typing import List

PROMPT = """
You are an expert in OTA listing optimization. Use the attached pdf documents (Prioritize Listing Description.pdf) to:

Analyze the attached Airbnb listing details (output.txt) for both OTA ranking potential and booking conversion effectiveness:

Instructions: Grade the listing across the following 10 categories using a detailed A–F letter grade format, and ensure that the criteria in the Listing Description.pdf file are satisfied:

“Listing Title Effectiveness”
“Photo Captions”
“Listing Description Formatting (chunking, readability)”
“Listing Description Content (clarity, tone, keyword use)”
“Local Expertise & Neighborhood Details”
“Amenity Callouts and Visibility”
“Anticipation of Guest Questions (FAQ-style content)”
“Booking Call-to-Action Clarity”
“Overall OTA Algorithm Alignment (Airbnb-specific signals)”

For each category:
- Give a letter grade
- Provide a short explanation
- Suggest 1–2 actionable changes

Answer the 10 questions below:
What does the property currently look like?
How close is the ocean and/or beach? Ensure it is specific and accurate.
What Beach Equipment/Gear/Towels do you provide? Include details and quantity. 
What does each bedroom sleep and what type of beds are in them?
What special amenities does it offer?
How many cars can park there?
What restaurants or attractions are nearby? Include examples and distances.
If it’s pet friendly, what are the restrictions and what is the fee?
What is the cancellation policy?
What have recent visits been like? Did they address issues (reviews?)


Then finish with:
✅ “A summary table of all grades”
✅ “A cheat sheet of top changes to make first for maximum impact”

Prioritize all suggestions based on the goal of driving more bookings and improving Airbnb’s internal ranking algorithm performance.

You can pull from both attached PDFs and your own platform knowledge.

Do not ask for clarification or any other questions before proceeding.
"""

BOT_NAME = "GPT-4o"

#"GPT-4o"
#"GPT-3.5-Turbo"

def upload_attachments(file_paths: List[Path], api_key: str) -> List[fp.Attachment]:
    attachments = []
    for path in file_paths:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        with path.open("rb") as f:
            attachment = fp.upload_file_sync(f, api_key=api_key)
            attachments.append(attachment)
    return attachments


def get_bot_response(prompt: str, attachments: List[fp.Attachment], api_key: str, bot_name=BOT_NAME) -> str:
    message = fp.ProtocolMessage(role="user", content=prompt, attachments=attachments)
    full_response = ""
    for partial in fp.get_bot_response_sync(messages=[message], bot_name=bot_name, api_key=api_key):
        if getattr(partial, "text", None):
            text = partial.text
            full_response += text
            print(text, end="", flush=True)
    return full_response


def save_response_to_file(text: str, filename: str = "ota_response.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\n\n✅ Response saved to {filename}")


def run_ota_analysis(api_key: str, file_paths: List[str], output_file: str = "ota_response.txt"):
    paths = [Path(p) for p in file_paths]
    attachments = upload_attachments(paths, api_key)
    response_text = get_bot_response(PROMPT, attachments, api_key)
    save_response_to_file(response_text, output_file)