import dropbox
import os

class Download:
    def __init__(self, download_path) -> None:
        self.download_path = download_path

    def download_files_from_dropbox(self):
        DROPBOX_ACCESS_TOKEN = 'sl.B56Q0k0JVFmRNPgHl91o3wjAQSSjS-v30wgkfYJHla0rDdUukS6GUvpIw-BspPhhZVhv9-zvK4EChGKiX3RA0_ShavmI4l_uj8wSmbcsdl_3LdUNp1yEUV1yAIDQobY8BIffJhz8BjRl'
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        final_directory = 'background'
        
        try:
            # List all files in the specified folder
            result = dbx.files_list_folder("", recursive = True)
        except dropbox.exceptions.ApiError as err:
            print(f"Failed to list folder contents: {err}")
            return
        for entry in result.entries:
            # Check if the entry is a file and if it is a video file
            print(f"Downloading {entry.name}...")
            try:
                # Download the file
                _, res = dbx.files_download(entry.path_lower)
                # Save the file to the specified download path
                with open(os.path.join(self.download_path, entry.name), 'wb') as f:
                    f.write(res.content)
                print(f"Downloaded {entry.name} successfully.")
            except dropbox.exceptions.ApiError as err:
                print(f"Failed to download {entry.name}: {err}")