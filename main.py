from ChromiumBrowsers import ChromiumBrowserDataExtractor
import argparse
import sys

if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description="Chromium Browsers Data Extractor")
    arg_parser.add_argument(
        "--b",
        choices=["chrome", "brave", "edge"],
        dest="browser",
        help="Enter the browser name",
    )

    args = arg_parser.parse_args()
    if not args.browser:
        print("Error: Please provide the --b argument.")
        sys.exit(1)

    browser = ChromiumBrowserDataExtractor(args.browser)
    browser.extract_bookmarks()
    browser.extract_history()
    browser.extract_password()
