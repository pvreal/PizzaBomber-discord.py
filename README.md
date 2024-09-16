
```markdown
# Order pizza through discord!

This Discord bot allows users to order pizza from Pizza Hut using a simple command. It uses the TomTom API for geocoding and finding and the Playwright library for automating the ordering process on the Pizza Hut website.

## Features

- Geocode addresses using TomTom API
- Find nearby Pizza Hut locations
- Automate pizza ordering process on Pizza Hut website
- Discord bot integration for easy ordering

## Prerequisites

- Python 3.7+
- Discord Bot Token
- TomTom API Key

## Installation

1. Clone this repository
2. Install required packages:
   
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```
   playwright install
   ```

## Configuration

1. Open the script and set the following variables:
   - `TOKEN`: Your Discord bot token
   - `TOMTOMKEY`: Your TomTom API key

2. (Optional) To restrict the bot to a specific channel, uncomment and set the `CHANNELID` variable.

## Usage

1. Run the script:
   ```
   python main.py
   ```

2. In Discord, use the command:
   ```
   /orderpizza address:"Street Name" city:"City" state:"State" zip_code:"Postal/Zip code"
   ```

## Be very cautious using this as anybody can view your address from the command.

## Disclaimer

This bot is for educational purposes only. Please do not pizzabomb anyone as thats a waste of food and labour.

## License

[GPL-3.0 license](https://www.gnu.org/licenses/gpl-3.0.en.html)

For support or questions contact me on Discord @ 999.pv
