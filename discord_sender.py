import os
import requests
from misc.config import config

def send_review_to_discord(review):
    webhook_url = config.DISCORD_WEBHOOK_URL
    if not webhook_url:
        print("No DISCORD_WEBHOOK_URL provided.")
        return
    
    # Choose the appropriate icon for the OS
    if review.os == "Android":
        icon_url = "https://cdn-icons-png.flaticon.com/512/888/888889.png"
    else:
        icon_url = "https://cdn-icons-png.flaticon.com/512/740/740922.png"

    # Generate star emojis
    stars = '⭐️' * review.rating

    # Main description with stars and content
    description = f"\n{stars}\n"
    description += f"{review.content}\n\n"

    # Optional: add title if present (iOS only)
    if review.title:
        title = f"{review.os} — {review.title}"
    else:
        title = f"{review.os}"

    # Footer with author and date
    footer_text = f"{review.author_name} • {review.datetime.strftime('%d/%m/%Y %H:%M')}"

    # Add fields for version, device, and language if present
    fields = []
    if review.version:
        fields.append({
            "name": "📦 Version",
            "value": f"{review.version} - {review.build_version}\n\n",
        })
    if review.phone:
        fields.append({
            "name": "📱 Device",
            "value": f"{review.phone}\n\n",
        })
    if review.reviewerLanguage:
        fields.append({
            "name": "🌐  Language",
            "value": review.reviewerLanguage,
        })

    embed = {
        "author": {
            "icon_url": icon_url,
            "name": title
        },
        "description": description.strip(),
        "color": 3447003 if review.os == "iOS" else 5763719,
        "footer": {
            "text": footer_text
        },
        "fields": fields
    }

    payload = {
        "embeds": [embed]
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code != 204:
            print(f"Failed to send to Discord: {response.status_code} {response.text}")
        else:
            print("Review sent to Discord.")
    except requests.RequestException as e:
        print(f"Network error when sending to Discord: {e}")
