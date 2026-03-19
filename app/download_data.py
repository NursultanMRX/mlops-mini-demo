from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

# JSON fayl GitHub Secret orqali
gdrive_json = os.environ["GDRIVE_KEY"]
with open("service_account.json", "w") as f:
    f.write(gdrive_json)

gauth = GoogleAuth()
# To‘g‘ridan-to‘g‘ri Service Account key bilan autentifikatsiya
gauth.LoadServiceAccountCredentials("service_account.json")
drive = GoogleDrive(gauth)

# Masalan, file yuklash
file_id = "1lLaxBSyKS-eZHclBWeY24ollDPXM1PdB"
downloaded = drive.CreateFile({'id': file_id})
os.makedirs("data", exist_ok=True)
downloaded.GetContentFile("data/adult11.csv")
print("CSV downloaded successfully!")
