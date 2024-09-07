# Telegram Scraper

This repository contains a powerful and flexible Telegram scraper designed to collect message data and media files from Telegram channels or groups. Built with Python and the Telethon library, this scraper is ideal for data analysts, researchers, and developers looking to gather and analyze data from Telegram for various purposes, such as social network analysis, market research, or content monitoring.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
  - [1. Session Management and Login Authentication](#1-session-management-and-login-authentication)
  - [2. Main Scraper: Data and Media Collection](#2-main-scraper-data-and-media-collection)
  - [3. Data Merging](#3-data-merging)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Asynchronous Scraping**: Utilizes Python's `asyncio` and Telethon library for efficient and non-blocking data collection.
- **Data and Media Download**: Fetches messages, along with any attached media (images, videos, etc.), and saves them locally.
- **Error Management**: Includes mechanisms to handle rate limits (`FloodWaitError`) and other common exceptions gracefully.
- **Customizable**: Allows users to define scraping parameters such as group/channel name, message limits, and scraping intervals.
- **Data Consolidation**: Merges individual CSV files containing messages and metadata into a single, comprehensive dataset.

## Requirements

- Python 3.7 or later
- [Telethon](https://pypi.org/project/Telethon/)
- `nest_asyncio` for enabling nested event loops

## Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/Amirwpi/Telegram_Scraper.git
    cd telegram-scraper
    ```

2. **Install Dependencies**

    Install the required Python libraries using pip:

    ```sh
    pip install -r requirements.txt
    ```

    *Note: Ensure you have `Telethon` and `nest_asyncio` in your `requirements.txt`.*

## Usage

### 1. Set Up Your API Credentials

- Obtain your API ID and hash from the [Telegram API](https://my.telegram.org/auth).
- Update the placeholders in the script (`api_id`, `api_hash`, and `phone_number`) with your actual credentials.

### 2. Run the Session Management Script

Execute the following command to authenticate your Telegram session:

```sh
python session_management.py
```

Follow the on-screen instructions to complete authentication and retrieve your session string.

### 3. Run the Main Scraper

After obtaining the session string, run the main scraper to start collecting data:

```sh
python main_scraper.py
```

### 4. Merge the Data

Once the scraping is complete, use the merging script to consolidate all CSV files into a single file:

```sh
python merge_data.py
```

## Configuration

Before running the scraper, customize the following settings in `main_scraper.py`:

- **`api_id`** and **`api_hash`**: Your Telegram API credentials.
- **`group_title`**: The Telegram group or channel from which to scrape data.
- **`limit_msg`**: Maximum number of messages to fetch per request.
- **`Repeat_number`**: Number of iterations for repeated scraping.
- **`datetime_before`**: The initial timestamp to begin scraping messages from.

## How It Works

### 1. Session Management and Login Authentication

The first part of the scraper handles authentication with the Telegram API. It checks for authorization, manages two-factor authentication, and provides a session string for subsequent scraping tasks.

### 2. Main Scraper: Data and Media Collection

The main scraping script uses the `GetHistoryRequest` function to iteratively fetch messages and media from the specified group or channel. It handles Telegram's rate limits by catching `FloodWaitError` exceptions and waiting before retrying requests.

### 3. Data Merging

After data collection, the scraper saves the messages and media information in multiple CSV files. The merging script consolidates these files into a single dataset for easier analysis.

## Error Handling

- **FloodWaitError**: Automatically waits for the required time if Telegram's rate limit is hit.
- **SessionPasswordNeededError**: Handles two-factor authentication if enabled on the account.
- General exceptions are caught and logged to ensure the scraper continues running smoothly.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to suggest improvements or report bugs.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -am 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
