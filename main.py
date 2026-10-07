import os
import asyncio
from pyrogram import Client, filters

# Mengambil konfigurasi dari Config Vars Heroku untuk keamanan
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# Sesuai request Anda, target ID grup dimasukkan ke kode atau bisa via Heroku
TARGET_CHAT_ID = -1004380577102 

# Inisialisasi Pyrogram Client
app = Client(
    "my_ubot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Filter untuk mendeteksi pesan di grup spesifik
@app.on_message(filters.chat(TARGET_CHAT_ID) & filters.text)
async def deteksi_pancing(client, message):
    # Mencari teks spesifik yang ada di bagian bawah gambar Anda
    if "Hasil tangkapan sudah dikirim ke pesan bot masing-masing" in message.text:
        print(f"[{message.chat.title}] Pesan pemicu terdeteksi! Mengirim perintah pancing...")
        
        # Jeda 1 detik agar terlihat natural dan menghindari spam block
        await asyncio.sleep(1) 
        
        # Mengirimkan pesan perintah sesuai request Anda
        await client.send_message(
            chat_id=TARGET_CHAT_ID,
            text="/open_mancing@fish_it_vip_bot"
        )

print("Ubot Pancing Otomatis Aktif...")
app.run()
