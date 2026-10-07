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

# Kedua ID grup target Anda
GRUP_LAMA = -1004380577102
GRUP_BARU = -1004389949822
TARGET_CHATS = [GRUP_LAMA, GRUP_BARU] 

app = Client(
    "my_ubot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

# Filter mendeteksi pesan dari kedua grup
@app.on_message(filters.chat(TARGET_CHATS) & filters.text & ~filters.me)
async def deteksi_pancing(client, message):
    if "Hasil tangkapan sudah dikirim ke pesan bot masing-masing" in message.text:
        current_chat_id = message.chat.id
        
        # Penyesuaian isi teks perintah berdasarkan masing-masing grup
        if current_chat_id == GRUP_BARU:
            pesan_perintah = "/open_mancing@fish_it_vip3_bot"
        else:
            pesan_perintah = "/open_mancing@fish_it_vip_bot"
            
        print(f"Pemicu terdeteksi di grup {current_chat_id}! Mengirim: {pesan_perintah}")
        
        # Jeda 1 detik agar natural
        await asyncio.sleep(1) 
        
        # Mengirimkan pesan perintah yang sesuai ke grup masing-masing
        await client.send_message(
            chat_id=current_chat_id,
            text=pesan_perintah
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
            
        print("Ubot Pancing Otomatis Aktif dengan Perintah Berbeda di Tiap Grup!")
        
        # Menjaga skrip tetap stand-by 24 jam
        while True:
            await asyncio.sleep(3600)

# Menjalankan fungsi utama
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
