import dropbox
import os
import requests

class Download:
    def __init__(self, download_path):
        print("Initializing downloader...")
        self.download_path = download_path

    def refresh_access_token(self, refresh_token, client_id, client_secret):
        url = "https://api.dropboxapi.com/oauth2/token"
        data = {
            "refresh_token" : refresh_token,
            "grant_type" : "refresh_token",
            "client_id": client_id,
            "client_secret" : client_secret
        }
        response = requests.post(url, data = data)
        response_data = response.json()
        return response_data['access_token']

    def download_files_from_dropbox(self, access_token):
        #access_token = 'sl.B54hN4V54HsjmSqVT0yL0EBpmO2fo_dasCdrgyk6aJooK2-NTMVqV_FrRffIaHE5tTrq7qS6LlHqG-HKYGIzFiu4friBwcvfK22duv4iFfkQXPEQJjF3ngiHPM00GKMC-UD6fLWBOrxM'
        dbx = dropbox.Dropbox(access_token)

        try:
            # List all files in the specified folder
            result = dbx.files_list_folder("", recursive = True)
        except dropbox.exceptions.ApiError as err:
            print(f"Failed to list folder contents: {err}")
            return
        for index, entry in enumerate(result.entries):
            # Check if the entry is a file and if it is a video file
            print(f"Downloading {entry.name}...")
            try:
                # Download the file
                metadata, res = dbx.files_download(entry.path_lower)
                # Save the file to the specified download path
                file_name = f"{self.download_path}/{index}.mp4"
                with open(file_name, 'wb') as f:
                    f.write(res.content)
                print(f"Downloaded {entry.name} successfully.")
            except dropbox.exceptions.ApiError as err:
                print(f"Failed to download {entry.name}: {err}")