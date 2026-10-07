import os
import asyncio
from pyrogram import Client, filters

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

# Fungsi yang berjalan otomatis saat ubot baru menyala
async def load_database():
    async with app:
        print("Sedang menyinkronkan database grup... Mohon tunggu sebentar.")
        try:
            # Trik memaksa Pyrogram memuat semua chat ke memori agar tidak memicu 'Peer id invalid'
            async for dialog in app.get_dialogs(limit=100):
                pass
            print("Sinkronisasi database selesai! Semua grup berhasil dikenali.")
        except Exception as e:
            print(f"Gagal memuat dialog otomatis: {e}")

# Handler utama untuk mendeteksi pesan teks
@app.on_message(filters.text & ~filters.me)
async def deteksi_pancing(client, message):
    try:
        # Saring manual: jika bukan grup target, langsung abaikan
        if message.chat.id != TARGET_CHAT_ID:
            return

        # Cek kata kunci pemicu sesuai gambar pertama Anda
        if "Hasil tangkapan sudah dikirim ke pesan bot masing-masing" in message.text:
            print("Pesan pemicu terdeteksi di grup target! Mengirim perintah...")
            
            # Jeda 1 detik agar natural
            await asyncio.sleep(1) 
            
            # Kirim pesan otomatis ke grup target
            await client.send_message(
                chat_id=TARGET_CHAT_ID,
                text="/open_mancing@fish_it_vip_bot"
            )
    except Exception:
        pass

# Menjalankan sinkronisasi database terlebih dahulu baru menyalakan bot secara penuh
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_database())
    print("Ubot Pancing Otomatis Aktif & Siap Digunakan!")
    app.run()
