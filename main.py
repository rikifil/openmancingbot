import os
import asyncio
import logging
from pyrogram import Client, filters

# Pembungkaman total semua logger bawaan Pyrogram
logging.basicConfig(level=logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.CRITICAL)

# Mengambil konfigurasi dari Config Vars Heroku
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# SEKARANG MENGGUNAKAN LIST UNTUK 2 GRUP TARGET
TARGET_CHATS = [-1004380577102, -1004389949822] 

app = Client(
    "my_ubot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

# Filter disetel untuk mendeteksi pesan dari List TARGET_CHATS
@app.on_message(filters.chat(TARGET_CHATS) & filters.text & ~filters.me)
async def deteksi_pancing(client, message):
    if "Hasil tangkapan sudah dikirim ke pesan bot masing-masing" in message.text:
        # Mengambil ID grup tempat pesan itu muncul
        current_chat_id = message.chat.id
        print(f"Pesan pemicu terdeteksi di grup {current_chat_id}! Mengirim perintah pancing...")
        
        # Jeda 1 detik agar natural
        await asyncio.sleep(1) 
        
        # Membalas otomatis ke grup yang bersangkutan
        await client.send_message(
            chat_id=current_chat_id,
            text="/open_mancing@fish_it_vip_bot"
        )

# Fungsi utama untuk sinkronisasi database peer/grup
async def main():
    async with app:
        print("Sedang menyinkronkan database grup... Mohon tunggu sebentar.")
        try:
            async for dialog in app.get_dialogs():
                pass
            print("Sinkronisasi database selesai! Semua grup berhasil dikenali.")
        except Exception:
            print("Sinkronisasi database dilewati, ubot tetap berjalan.")
            
        print("Ubot Pancing Otomatis Aktif & Mengunci Dua Grup Target!")
        
        # Menjaga skrip tetap stand-by 24 jam
        while True:
            await asyncio.sleep(3600)

# Menjalankan fungsi utama
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
