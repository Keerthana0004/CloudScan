import asyncio
from crawl4ai import AsyncWebCrawler

TARGET_URL = "https://github.com/hashicorp/terraform-provider-aws"
OUTPUT_FILE = "output.md"

async def main():
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        try:
            # Run the crawler on a URL
            result = await crawler.arun(url=TARGET_URL)
            if result and result.markdown:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    f.write(result.markdown)
            elif result.error_message:
                print(f"Crawler encountered an error: {result.error_message}")
            else:
                print("Crawl completed, but no markdown content was extracted.")

        except Exception as e:
            print(f"An unexpected error occurred during the crawl: {e}")


# Run the async main function
asyncio.run(main())
