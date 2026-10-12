import os
import asyncio
import logging
from pyrogram import Client, filters

# Pembungkaman total semua logger bawaan Pyrogram
logging.basicConfig(level=logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.CRITICAL)

# Mengambil konfigurasi dasar dari Config Vars Heroku
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# DAFTAR ID GRUP TARGET AKTIF
GRUP_1 = -1004380577102
GRUP_3 = -1004216238522  
TARGET_CHATS = [GRUP_1, GRUP_3] 

# ====================================================================
# MENGAMBIL KATA KUNCI DARI HEROKU CONFIG VARS
# Menggunakan pemisah koma (,) dan otomatis diubah ke huruf kecil semua
# ====================================================================
def ambil_kata_kunci(var_name):
    raw_input = os.environ.get(var_name, "")
    if not raw_input:
        return []
    # Memisahkan berdasarkan koma dan menghapus spasi di awal/akhir kata
    return [kata.strip().lower() for kata in raw_input.split(",") if kata.strip()]

KATA_UNTUK_PIN = ambil_kata_kunci("KATA_PIN")
KATA_UNTUK_HAPUS = ambil_kata_kunci("KATA_HAPUS")
# ====================================================================

app = Client(
    "my_ubot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

# Handler Utama untuk mendeteksi semua pesan teks di grup target
@app.on_message(filters.chat(TARGET_CHATS) & filters.text)
async def ubot_multitask_handler(client, message):
    current_chat_id = message.chat.id
    pesan_teks_lower = message.text.lower()

    try:
        # ------------------------------------------------------------
        # MODUL 1: DETEKSI PANCING (Hanya merespons jika pengirim BUKAN ubot sendiri)
        # ------------------------------------------------------------
        if not message.from_user or not message.from_user.is_self:
            if "Hasil tangkapan sudah dikirim ke pesan bot masing-masing" in message.text:
                pesan_perintah = "/open_mancing@fish_it_vip_bot"
                print(f"[{current_chat_id}] Pemicu pancing terdeteksi! Mengirim perintah...")
                await asyncio.sleep(1) 
                await client.send_message(chat_id=current_chat_id, text=pesan_perintah)
                return

        # ------------------------------------------------------------
        # MODUL 2: AUTO PIN PESAN (Hanya jalan jika KATA_PIN diisi di Heroku)
        # ------------------------------------------------------------
        if KATA_UNTUK_PIN and any(kata in pesan_teks_lower for kata in KATA_UNTUK_PIN):
            print(f"[{current_chat_id}] Kata kunci PIN terdeteksi! Menyematkan pesan...")
            await client.pin_chat_message(chat_id=current_chat_id, message_id=message.id, both_for_all=True)
            return

        # ------------------------------------------------------------
        # MODUL 3: AUTO DELETE PESAN (Hanya jalan jika KATA_HAPUS diisi di Heroku)
        # ------------------------------------------------------------
        if KATA_UNTUK_HAPUS and any(kata in pesan_teks_lower for kata in KATA_UNTUK_HAPUS):
            print(f"[{current_chat_id}] Kata kunci HAPUS terdeteksi! Menghapus pesan...")
            await client.delete_messages(chat_id=current_chat_id, message_ids=message.id)
            return

    except Exception as e:
        print(f"Gagal mengeksekusi aksi di grup {current_chat_id}: {e}")

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
            
        print("Ubot Multitask Config Vars Berhasil Aktif!")
        
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
