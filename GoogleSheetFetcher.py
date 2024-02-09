import requests
import json

class GoogleSheetFetcher:
    def __init__(self, Gapi):
        self.Gapi = Gapi
        self.fetched_data = None

    def dataFetcher(self):
        try:
            response = requests.get(self.Gapi)
            response.raise_for_status()
            self.fetched_data = json.loads(response.text)
        except requests.RequestException as e:
            print(f"Failed to get data: {e}")
            self.fetched_data = None

    def dataProcessing(self):
        try:
            if self.fetched_data is not None:
                valid_discord_usernames_and_record_creation_date = [(entry["Discord username"], entry["Created date"]) for entry in self.fetched_data if entry["update"].lower() == "true"]
                return valid_discord_usernames_and_record_creation_date
            else:
                print("No data available for processing.")
                return None
        except Exception as e:
            print(f"Error during data processing: {e}")
            return None
        
    async def remove_user_entry(self, username):
        pass

# Example of using the class
Gapi_url = "your_sheet_api_url_here"
fetcher = GoogleSheetFetcher(Gapi_url)
fetcher.dataFetcher()
processed_data = fetcher.dataProcessing()
print(processed_data)
