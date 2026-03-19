# download_data.py
import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# GitHub Actions secret
gdrive_json = os.environ["GDRIVE_KEY"]
with open("service_account.json", "w") as f:
    f.write(gdrive_json)

gauth = GoogleAuth()
gauth.ServiceAuthSettings = {"client_json_file": "service_account.json"}
gauth.ServiceAuth()
drive = GoogleDrive(gauth)

# Google Drive file ID
file_id = "1lLaxBSyKS-eZHclBWeY24ollDPXM1PdB"  # Adult Income CSV file ID
downloaded = drive.CreateFile({"id": file_id})
os.makedirs("data", exist_ok=True)
downloaded.GetContentFile("data/adult11.csv")
print("Adult Income CSV downloaded successfully!")
