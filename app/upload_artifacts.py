import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 1. Autentifikatsiya
gdrive_json = os.environ["GDRIVE_KEY"]
with open("service_account.json", "w") as f:
    f.write(gdrive_json)

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

FOLDER_ID = "1SxlXt4uulJpy7Eerx6YYb-_ilVe0uvQa"
files_to_upload = ["best_params.json", "app/final_model.keras", "metrics.png"]

def upload_to_drive():
    try:
        # qaysi robot ishlayotganini aniq ekranga chiqaramiz
        user_info = service.about().get(fields="user").execute()
        bot_email = user_info['user']['emailAddress']
        print(f"🤖 Hozir GitHub'da ishlayotgan robot: {bot_email}")
        
        # supportsAllDrives=True parametrini qo'shdik!
        folder = service.files().get(
            fileId=FOLDER_ID, 
            fields='name', 
            supportsAllDrives=True
        ).execute()
        print(f"✅ Papka topildi: {folder.get('name')}")

        # Fayllarni yuklash
        for f_path in files_to_upload:
            if os.path.exists(f_path):
                file_name = os.path.basename(f_path)
                file_metadata = {'name': file_name, 'parents': [FOLDER_ID]}
                media = MediaFileUpload(f_path, resumable=True)
                
                # Bu yerga ham supportsAllDrives=True qo'shdik
                file = service.files().create(
                    body=file_metadata, 
                    media_body=media, 
                    fields='id, webViewLink',
                    supportsAllDrives=True
                ).execute()
                print(f"🚀 Yuklandi: {file_name}")
            else:
                print(f"❌ Xato: {f_path} topilmadi!")

    except Exception as e:
        print(f"DIQQAT XATO: {e}")
        print(f"\n🚨 ILTIMOS, Google Drive'da papkaga kirib, mana shu emailga ruxsat bering: {bot_email}")
        exit(1)

upload_to_drive()
