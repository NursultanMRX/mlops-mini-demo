import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 1. Autentifikatsiya
gdrive_json = os.environ["GDRIVE_KEY"]
with open("service_account.json", "w") as f:
    f.write(gdrive_json)

SCOPES = ['https://www.googleapis.com/auth/drive.file']
creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# 2. Yuklanishi kerak bo'lgan fayllar ro'yxati
files_to_upload = [
    "best_params.json",
    "app/final_model.keras",
    "metrics.png"
]

# 3. Google Drive'dagi papka ID si (O'zingizning papka ID'ingizni qo'ying)
# Maslahat: Drive'da yangi papka oching va uning URL'idan ID ni oling
FOLDER_ID = "1SxlXt4uulJpy7Eerx6YYb-_iIVe0uvQa" 

def upload_file(file_path, folder_id):
    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    
    # Eskisini o'chirib yangisini yuklash yoki shunchaki yuklash
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Fayl yuklandi: {file_name} (ID: {file.get('id')})")

# Yuklashni boshlash
for file_p in files_to_upload:
    if os.path.exists(file_p):
        upload_file(file_p, FOLDER_ID)
    else:
        print(f"Xato: {file_p} topilmadi!")
