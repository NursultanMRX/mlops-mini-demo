from pydrive2.auth import ServiceAccountCredentials
from pydrive2.drive import GoogleDrive
import os
import json

# GitHub Secret orqali JSON
gdrive_json = os.environ["GDRIVE_KEY"]
with open("service_account.json", "w") as f:
    f.write(gdrive_json)

# Service Account Credentials
scopes = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scopes=scopes)
drive = GoogleDrive(creds)

# File yuklash
file_id = "1lLaxBSyKS-eZHclBWeY24ollDPXM1PdB"
downloaded = drive.CreateFile({'id': file_id})
os.makedirs("data", exist_ok=True)
downloaded.GetContentFile("data/adult11.csv")
print("CSV downloaded successfully!")
