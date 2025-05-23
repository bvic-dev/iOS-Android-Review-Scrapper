import argparse
from misc.config import config
import ios_review
import android_review
from misc.utils import build_json_result
from discord_sender import send_review_to_discord

"""
Generates a JSON file containing ratings and store reviews for Android and iOS apps.

Required environment variables:

iOS:
    KEY_ID             - API Key ID from App Store Connect
    ISSUER_ID          - Issuer ID from App Store Connect
    PRIVATE_KEY_FILE   - Path to your .p8 key file
    APPLE_APP_ID       - Numeric App ID (https://appstoreconnect.apple.com/apps/XXXXXXXX)

Android:
    JSON_KEY_FILE      - Path to Google service account JSON file
    REPO_PACKAGE_NAME  - App package name (e.g., com.example.app)

Discord:
    DISCORD_WEBHOOK_URL  - Your Discord webhook URL
"""

def main():
    parser = argparse.ArgumentParser(
        description=(
            "App Store & Google Play reviews fetcher.\n\n"
            "Examples:\n"
            "  python main.py --ios -d -w ios_reviews.json -t 48 -q 100\n"
            "  python main.py --android --write-file android_reviews.json --quantity 20\n"
            "\n"
            "You must specify one of --ios or --android, and at least one action (--send-discord and/or --write-file)."
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--ios', action='store_true', help='Fetch iOS app reviews')
    group.add_argument('-a', '--android', action='store_true', help='Fetch Android app reviews')

    parser.add_argument('-d', '--send-discord', action='store_true', help='Send reviews to Discord')
    parser.add_argument('-w', '--write-file', metavar='FILE', help='Output JSON file path')
    parser.add_argument('-t', '--timedelta', type=int, metavar='HOURS', help='Time window in hours to fetch reviews (default: 72)')
    parser.add_argument('-q', '--quantity', type=int, metavar='N', help='Maximum number of reviews to fetch (default: 50)')

    args = parser.parse_args()
    reviews = []

    # At least one action: send to Discord OR write to file
    if not args.send_discord and not args.write_file:
        parser.error("You must specify at least one action: --send-discord and/or --write-file FILE.")

    # Set time window for reviews if specified
    if args.timedelta:
        config.TIMEDELTA_HOURS = args.timedelta
        print(f"⏳ Time window set to {args.timedelta}h")

    # Set output file if specified
    if args.write_file:
        config.OUTPUT_FILE = args.write_file
        print(f"💾 Output file: {config.OUTPUT_FILE}")

    # Set review fetch quantity if specified
    if args.quantity:
        config.REVIEWS_FETCH_QUANTITY = args.quantity
        print(f"🔢 Will fetch up to {args.quantity} reviews per platform")

    # Fetch reviews (choice is already required)
    if args.ios:
        print("📱 Fetching iOS reviews...")
        reviews = ios_review.get_reviews()
    elif args.android:
        print("🤖 Fetching Android reviews...")
        reviews = android_review.get_reviews()

    # Send reviews to Discord
    if args.send_discord:
        print(f"📤 Sending {len(reviews)} review(s) to Discord...")
        for review in reviews:
            send_review_to_discord(review)

    # Write reviews to file if specified
    if args.write_file:
        print(f"💾 Writing {len(reviews)} review(s) to {config.OUTPUT_FILE}...")
        with open(config.OUTPUT_FILE, 'w') as file:
            file.write(build_json_result(reviews=reviews))

if __name__ == "__main__":
    main()
