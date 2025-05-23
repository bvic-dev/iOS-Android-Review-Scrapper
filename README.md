# App Store & Google Play Reviews Fetcher

Python scripts to automatically fetch reviews from the App Store (iOS) and Google Play (Android), save them as JSON, and optionally send them to a Discord channel via webhook.

## ℹ️ About this fork

This project is a **fork** of [review\_scrapper](https://github.com/GTrebaol/review_scrapper).
It was extended to add Discord integration, cross-platform improvements, and easier configuration.

Many thanks to the original author for the foundation of this tool!

---

## 🚀 Features

* Fetch reviews for both iOS and Android apps
* Filter reviews by recent hours (default: last 72h)
* Output as JSON file (optional)
* Send reviews to a Discord channel with rich embeds (optional)
* Easy configuration with `.env` file

---

## ⚙️ Setup

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourname/review-fetcher.git
   cd review-fetcher
   ```

2. **Create and activate a Python virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Copy and configure `.env`**

   ```bash
   cp .env.example .env
   # Edit .env and fill in your credentials and variables
   ```

5. **Ensure your keys are in the correct files/locations**

   * Place your iOS `.p8` file in the path specified by `PRIVATE_KEY_FILE`
   * Place your Google Cloud service account JSON in the path specified by `JSON_KEY_FILE`

---

## 📝 Usage

```bash
python main.py --help
```

Examples:

* **Fetch iOS reviews and send to Discord:**

  ```bash
  python main.py --ios --send-discord
  ```

* **Fetch Android reviews and save to a file (last 24h):**

  ```bash
  python main.py --android --write-file android_reviews.json --timedelta 24
  ```

* **Fetch iOS reviews, save to file and send to Discord:**

  ```bash
  python main.py --ios --send-discord --write-file ios_reviews.json
  ```

* **Fetch iOS reviews (limit 100), save to file and send to Discord:**

  ```bash
  python main.py --ios --send-discord --write-file ios_reviews.json --quantity 100
  ```

---

## 📦 Environment Variables (`.env`)

Copy `.env.example` and fill in the values.

* **iOS (App Store Connect API):**

  * `KEY_ID`, `ISSUER_ID`, `PRIVATE_KEY_FILE`, `APPLE_APP_ID`

* **Android (Google Play Developer API):**

  * `JSON_KEY_FILE`, `REPO_PACKAGE_NAME`

* **Discord:**

  * `DISCORD_WEBHOOK_URL`

---

## 🤝 Contributions

PRs welcome!

---

## 🤖 Automate with GitHub Actions

You can run this fetcher automatically using GitHub Actions.

### Example: Android reviews every 6h

Create a file `.github/workflows/fetch-android-reviews.yml`:

```yaml
name: Fetch Android Reviews
on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:
    inputs:
      timedelta:
        description: 'Time window in hours to fetch reviews'
        required: false
        default: '6'
      quantity:
        description: 'Max number of reviews to fetch'
        required: false
        default: '50'
jobs:
  fetch-android-reviews:
    runs-on: ubuntu-latest
    env:
      JSON_KEY_FILE: ${{ secrets.JSON_KEY_FILE }}
      REPO_PACKAGE_NAME: ${{ secrets.REPO_PACKAGE_NAME }}
      DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
      TIMEDELTA_HOURS: ${{ github.event.inputs.timedelta || '6' }}
      REVIEWS_FETCH_QUANTITY: ${{ github.event.inputs.quantity || '50' }}
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Save Google service account to file
        run: |
          echo "${JSON_KEY_FILE}" > service-account.json
      - name: Run Android Review Fetcher
        run: |
          python main.py --android --send-discord --timedelta ${{ env.TIMEDELTA_HOURS }} --quantity ${{ env.REVIEWS_FETCH_QUANTITY }}
        env:
          JSON_KEY_FILE: service-account.json
```

### Example: iOS reviews every 24h

Create a file `.github/workflows/fetch-ios-reviews.yml`:

```yaml
name: Fetch iOS Reviews
on:
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch:
    inputs:
      timedelta:
        description: 'Time window in hours to fetch reviews'
        required: false
        default: '24'
      quantity:
        description: 'Max number of reviews to fetch'
        required: false
        default: '50'
jobs:
  fetch-ios-reviews:
    runs-on: ubuntu-latest
    env:
      KEY_ID: ${{ secrets.KEY_ID }}
      ISSUER_ID: ${{ secrets.ISSUER_ID }}
      APPLE_APP_ID: ${{ secrets.APPLE_APP_ID }}
      DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
      TIMEDELTA_HOURS: ${{ github.event.inputs.timedelta || '24' }}
      REVIEWS_FETCH_QUANTITY: ${{ github.event.inputs.quantity || '50' }}
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Save Apple .p8 key to file
        run: |
          echo "${{ secrets.PRIVATE_KEY }}" > AuthKey.p8
      - name: Run iOS Review Fetcher
        run: |
          python main.py --ios --send-discord --timedelta ${{ env.TIMEDELTA_HOURS }} --quantity ${{ env.REVIEWS_FETCH_QUANTITY }}
        env:
          PRIVATE_KEY_FILE: AuthKey.p8
```

> **Don’t forget to configure your repository secrets for API keys and Discord webhook!**

---