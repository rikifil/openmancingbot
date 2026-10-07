import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import RPCError

# Mengambil konfigurasi dari Config Vars Heroku
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# ID Grup Target Spesifik Anda
TARGET_CHAT_ID = -1004380577102 

# Inisialisasi Pyrogram Client
app = Client(
    "my_ubot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Menggunakan filter global (all chats), penyaringan dilakukan manual di dalam fungsi
@app.on_message(filters.text & ~filters.me)
async def deteksi_pancing(client, message):
    try:
        # 1. CEK ID GRUP: Jika bukan grup target, langsung abaikan secepatnya
        if message.chat.id != TARGET_CHAT_ID:
            return

        # 2. CEK TEKS: Jika di grup target dan ada teks pemicu
        if "Hasil tangkapan sudah dikirim ke pesan bot masing-masing" in message.text:
            print("Pesan pemicu terdeteksi di grup target! Mengirim perintah pancing...")
            
            # Jeda 1 detik agar terlihat natural
            await asyncio.sleep(1) 
            
            # Mengirimkan pesan perintah ke grup target
            await client.send_message(
                chat_id=TARGET_CHAT_ID,
                text="/open_mancing@fish_it_vip_bot"
            )
            
    except Exception as e:
        # Jika ada eror peer id invalid dari grup lain, biarkan saja (diabaikan) agar skrip tidak crash
        pass

print("Ubot Pancing Otomatis Berhasil Aktif & Proteksi Grup Lain Aktif...")
app.run()
