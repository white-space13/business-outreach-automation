import argparse

from app.pagination import build_page_urls


def main():
    parser = argparse.ArgumentParser(description="Generate paginated search URLs without fetching them.")
    parser.add_argument("search_url")
    parser.add_argument("--pages", type=int, default=10)
    parser.add_argument("--page-size", type=int, default=10)
    args = parser.parse_args()

    for index, url in enumerate(build_page_urls(args.search_url, args.pages, args.page_size), start=1):
        print(f"{index}: {url}")


if __name__ == "__main__":
    main()
