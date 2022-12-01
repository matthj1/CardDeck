import argparse
import re
from urllib import parse


def has_scheme(url):
    return bool(re.search(r"^http", url))

def build_url(base_address, urls, token):
    if not has_scheme(base_address):
        print("urls must include a scheme")
        return

    for url in urls:
        if not has_scheme(url):
            print("urls must include a scheme")
            return
    
    return f"{base_address}?url={'&url='.join(urls)}&token={token}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("display_address", type=str, help="URL of the display")
    parser.add_argument("--urls", nargs="*", type=str, required=True, help="Endpoints from which to gather data, space seperated")
    parser.add_argument("--token", type=str, required=True, help="Auth token")

    args = parser.parse_args()

    encoded_urls = [parse.quote(url) for url in args.urls]
    print("\n")
    print(build_url(args.display_address, encoded_urls, args.token))