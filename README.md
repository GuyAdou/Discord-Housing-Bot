# Discord-Housing-Bot

Hey there! 👋 Enter the Discord-Housing-Bot - a cool side project turned community lifesaver, designed to smooth out the housing hunt in Discord communities. This Discord bot, is to assist with housing and roommate searches within Discord communities, and automates messaging and data management with integration to Google Sheets.

## Core Features

- **Automated Messaging**: Sends timely messages based on user interactions with the housing list.
- **Google Sheets Integration**: Fetches and updates data in real-time, ensuring up-to-date housing information.
- **Response Management**: Tracks user responses and ensures timely follow-ups.
- **Member Caching**: Optimizes bot performance through efficient member caching strategies.


## Getting Started

To deploy the Discord Housing Bot within your community, follow these steps:

### 1. Clone the Repository

Clone this repository to your local machine or server environment.

### 2. Configure Environment Variables

Securely set up your Discord bot token:
- Set the `TOKEN` environment variable to your bot's token.

### 3. Install Dependencies

Ensure the bot functions correctly by installing the required Python packages.

4. **Google Sheets and SheetDB API**
   - Set up a Google Sheet for housing data and configure it with SheetDB for API access.
   - Update `GOOGLE_SHEET_URL` and `Gapi` in the script with your Google Sheet URL and SheetDB API endpoint.

5. **Running the Bot**
   - Run the bot using:
     ```bash
     BhouseBotMain.py
     ```

## Commands

- `$hello`: The bot responds with a greeting.
- Housing triggers: When specific housing-related phrases are detected in messages, the bot provides relevant information.

## Join the Party
Got an idea? Found a bug? Jump in and contribute! Fork it, branch it, push it, pull-request it. Let's make housing searches a breeze, one commit at a time.

## Author
**Guy-Georges Adou Bogolo**

Crafted with care (and a fair bit of coffee) by me, Guy-Georges Adou Bogolo, as I ventured into the "real world." Questions, kudos, existential queries? Reach out or contribute to the project!

## License

This project is licensed under the [MIT License](LICENSE.md).
