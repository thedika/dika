from rapidfuzz import process, fuzz
from datetime import datetime, timedelta
import pandas as pd
import os

# ==========================
# KONFIGURASI
# ==========================

MASTER = "db pkl.xlsx"
GOOGLE = "Presensi Lokasi PKL (Jawaban).xlsx"
ANDROID = "presensi(1).csv"
OUTPUT = "laporan"

os.makedirs(OUTPUT, exist_ok=True)


# ==========================
# FUNGSI
# ==========================

def bersihkan_nama(nama):
    """Membersihkan format nama."""
    if pd.isna(nama):
        return ""

    nama = str(nama).upper().strip()

    nama = (
        nama.replace(".", "")
            .replace(",", "")
            .replace("'", "")
            .replace('"', "")
    )

    while "  " in nama:
        nama = nama.replace("  ", " ")

    return nama


def gps_mati(lat, lon):
    """True jika koordinat kosong / 0."""
    try:
        lat = float(lat)
        lon = float(lon)
        return lat == 0 or lon == 0
    except:
        return False


def cocokkan_nama(nama, master_list):
    """
    Exact Match
    ↓
    Fuzzy Match
    """

    if nama in master_list:
        return nama, 100

    hasil = process.extractOne(
        nama,
        master_list,
        scorer=fuzz.token_set_ratio
    )

    if hasil:
        return hasil[0], hasil[1]

    return None, 0


# ==========================
# MULAI
# ==========================

print("=" * 60)
print("REKAP ABSENSI PKL")
print("=" * 60)

print("Membaca database...")

master = pd.read_excel(MASTER)
google = pd.read_excel(GOOGLE)
android = pd.read_csv(ANDROID)

master["nama"] = master["nama"].apply(bersihkan_nama)
google["Nama Lengkap"] = google["Nama Lengkap"].apply(bersihkan_nama)
android["nama"] = android["nama"].apply(bersihkan_nama)

print("OK")


print("Filter H-1...")

google["Tanggal"] = pd.to_datetime(
    google["Timestamp"],
    errors="coerce",
    dayfirst=True
).dt.date

android["Tanggal"] = pd.to_datetime(
    android["waktu"],
    format="%m/%d/%y %H:%M",
    errors="coerce"
).dt.date

kemarin = datetime.now().date() - timedelta(days=1)

google = google[
    google["Tanggal"] == kemarin
].copy()

android = android[
    android["Tanggal"] == kemarin
].copy()

print("Tanggal :", kemarin)
print("Google  :", len(google))
print("Android :", len(android))