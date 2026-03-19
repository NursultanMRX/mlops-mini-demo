import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# 1. GitHub Secret'dan JSON'ni o'qib faylga yozish
gdrive_json = os.environ["GDRIVE_KEY"]
with open("service_account.json", "w") as f:
    f.write(gdrive_json)

# 2. Service Account bilan to'g'ridan-to'g'ri autentifikatsiya
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
creds = service_account.Credentials.from_service_account_file(
    'service_account.json', scopes=SCOPES
)

# 3. Drive API'ni ulash
service = build('drive', 'v3', credentials=creds)

# 4. Faylni yuklab olish
file_id = "1lLaxBSyKS-eZHclBWeY24ollDPXM1PdB" # Faylingizning ID sini yozishni unutmang!
request = service.files().get_media(fileId=file_id)

os.makedirs("data", exist_ok=True)
with io.FileIO("data/adult11.csv", "wb") as fh:
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Yuklanmoqda... {int(status.progress() * 100)}%")

print("Adult Income CSV muvaffaqiyatli yuklandi!")
