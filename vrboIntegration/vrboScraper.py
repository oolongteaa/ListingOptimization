from playwright.sync_api import sync_playwright
import json


def fetch_vrbo_full_data_combined(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context(
            locale="en-US",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(url, timeout=60000)

        # Let the content load
        page.wait_for_timeout(5000)

        # Try clicking the Overview tab
        try:
            page.click('text=Overview', timeout=3000)
            page.wait_for_timeout(2000)
        except:
            print("No 'Overview' tab found or clickable.")

        # Scroll to bottom to trigger lazy loading
        page.evaluate("""
            () => {
                return new Promise((resolve) => {
                    let totalHeight = 0;
                    const distance = 100;
                    const timer = setInterval(() => {
                        window.scrollBy(0, distance);
                        totalHeight += distance;
                        if (totalHeight >= document.body.scrollHeight) {
                            clearInterval(timer);
                            resolve();
                        }
                    }, 100);
                });
            }
        """)
        page.wait_for_timeout(3000)

        # Extract structured visible text elements
        structured_data = page.evaluate("""
        () => {
            const elements = document.querySelectorAll('body *');
            const output = [];

            elements.forEach(el => {
                const rawText = el.innerText || '';
                const text = rawText.trim();
                if (text.length > 0 && el.offsetParent !== null) {
                    output.push({
                        tag: el.tagName.toLowerCase(),
                        class: el.className,
                        id: el.id,
                        text: text,
                        attrs: [...el.attributes].reduce((acc, attr) => {
                            acc[attr.name] = attr.value;
                            return acc;
                        }, {})
                    });
                }
            });

            return output;
        }
        """)

        # Extract all images on the page
        image_data = page.evaluate("""
        () => {
            return [...document.querySelectorAll('img')].map(img => ({
                url: img.src,
                alt: img.alt || null
            }));
        }
        """)

        browser.close()
        return {
            "structured_data": structured_data,
            "images": image_data
        }

def main():
    print("==Vrbo Full Listing Scraper with Images==\n")
    listing_url = input("Enter the Vrbo listing URL: ").strip()

    print("\nFetching structured text + images...")
    data = fetch_vrbo_full_data_combined(listing_url)

    output_path = "../vrbo_details_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nFull listing data saved to {output_path}")

if __name__ == "__main__":
    main()
