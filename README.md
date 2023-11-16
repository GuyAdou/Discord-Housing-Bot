# Discord-Housing-Bot

This Discord bot, designed to assist with housing and roommate searches within Discord communities, automates messaging and data management with integration to Google Sheets.

## Features

- **Automated Messaging:** Sends scheduled messages to users based on their interaction with a Google Sheet containing housing information.
- **Data Integration:** Fetches and updates user information from a Google Sheet using SheetDB API.
- **Response Management:** Tracks and manages user responses within a specified time frame.
- **Member Caching:** Efficiently caches Discord guild members for optimized performance.

## Setup

1. **Clone Repository**
   - Clone this repository to your local machine or development environment.

2. **Environment Variables**
   - Set `TOKEN` in your environment variables to your Discord bot token.

3. **Dependencies**
   - Install the required dependencies:
     ```bash
     pip install discord.py requests asyncio pytz
     ```

4. **Google Sheets and SheetDB API**
   - Set up a Google Sheet for housing data and configure it with SheetDB for API access.
   - Update `GOOGLE_SHEET_URL` and `Gapi` in the script with your Google Sheet URL and SheetDB API endpoint.

5. **Running the Bot**
   - Run the bot using:
     ```bash
     python your_script_name.py
     ```

## Commands

- `$hello`: The bot responds with a greeting.
- Housing triggers: When specific housing-related phrases are detected in messages, the bot provides relevant information.

## Contribution

Contributions to this project are welcome. Please ensure to follow the project's coding standards and submit pull requests for any new features or bug fixes.

## Author

**Guy-Georges Adou Bogolo**

This project was developed and maintained by Your Name. For inquiries or collaboration requests, feel free to reach out or contribute to the project.

## License

This project is licensed under the [MIT License](LICENSE.md).
