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

# ID Grup Target Spesifik Anda
TARGET_CHAT_ID = -1004380577102 

app = Client(
    "my_ubot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

# Filter dikunci total untuk grup target saja
@app.on_message(filters.chat(TARGET_CHAT_ID) & filters.text & ~filters.me)
async def deteksi_pancing(client, message):
    if "Hasil tangkapan sudah dikirim ke pesan bot masing-masing" in message.text:
        print("Pesan pemicu terdeteksi di grup target! Mengirim perintah pancing...")
        await asyncio.sleep(1) 
        await client.send_message(
            chat_id=TARGET_CHAT_ID,
            text="/open_mancing@fish_it_vip_bot"
        )

# Fungsi utama untuk memancing pengenalan seluruh peer/grup akun Anda
async def main():
    async with app:
        print("Sedang menyinkronkan database grup... Mohon tunggu sebentar.")
        try:
            # Trik jitu: Mengambil semua chat aktif agar tersimpan di cache RAM Heroku
            async for dialog in app.get_dialogs():
                pass
            print("Sinkronisasi database selesai! Semua grup berhasil dikenali.")
        except Exception:
            print("Sinkronisasi database dilewati, ubot tetap berjalan.")
            
        print("Ubot Pancing Otomatis Aktif & Siap Digunakan!")
        
        # Menjaga skrip tetap stand-by 24 jam
        while True:
            await asyncio.sleep(3600)

# Menjalankan fungsi utama
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
