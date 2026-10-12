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

# DAFTAR ID GRUP TARGET AKTIF
GRUP_1 = -1004380577102
GRUP_3 = -1004216238522  
TARGET_CHATS = [GRUP_1, GRUP_3] 

# ====================================================================
# PENGATURAN KATA KUNCI (Silakan ubah kata di dalam tanda kutip sesuai keinginan)
# gunakan huruf kecil semua di dalam daftar ini agar deteksi lebih akurat
# ====================================================================
KATA_UNTUK_PIN = ["#pengumuman", "info penting", "wajib baca"]
KATA_UNTUK_HAPUS = ["judi online", "slot gacor", "link bokep", "open bo"]
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
    pesan_teks_lower = message.text.lower() # Mengubah teks ke huruf kecil semua untuk dicocokkan

    try:
        # ------------------------------------------------------------
        # MODUL 1: DETEKSI PANCING (Hanya merespons jika pengirim BUKAN akun ubot sendiri)
        # ------------------------------------------------------------
        if not message.from_user or not message.from_user.is_self:
            if "Hasil tangkapan sudah dikirim ke pesan bot masing-masing" in message.text:
                pesan_perintah = "/open_mancing@fish_it_vip_bot"
                print(f"[{current_chat_id}] Pemicu pancing terdeteksi! Mengirim perintah...")
                await asyncio.sleep(1) 
                await client.send_message(chat_id=current_chat_id, text=pesan_perintah)
                return # Selesai memproses modul pancing

        # ------------------------------------------------------------
        # MODUL 2: AUTO PIN PESAN (Mengecek apakah pesan mengandung kata kunci PIN)
        # ------------------------------------------------------------
        if any(kata in pesan_teks_lower for kata in KATA_UNTUK_PIN):
            print(f"[{current_chat_id}] Kata kunci PIN terdeteksi! Menyematkan pesan...")
            # Parameter both_for_all=True artinya pesan ter-pin untuk semua anggota grup
            await client.pin_chat_message(chat_id=current_chat_id, message_id=message.id, both_for_all=True)
            return # Selesai memproses modul pin

        # ------------------------------------------------------------
        # MODUL 3: AUTO DELETE PESAN (Mengecek apakah pesan mengandung kata kunci HAPUS)
        # ------------------------------------------------------------
        if any(kata in pesan_teks_lower for kata in KATA_UNTUK_HAPUS):
            print(f"[{current_chat_id}] Kata kunci HAPUS terdeteksi! Menghapus pesan...")
            await client.delete_messages(chat_id=current_chat_id, message_ids=message.id)
            return # Selesai memproses modul hapus

    except Exception as e:
        # Menangkap eror jika akun ubot Anda ternyata bukan admin saat mencoba PIN/HAPUS pesan
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
            
        print("Ubot Multitask (Pancing + Auto Pin + Auto Delete) Berhasil Aktif!")
        
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
