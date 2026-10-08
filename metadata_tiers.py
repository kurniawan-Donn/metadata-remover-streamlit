"""
Universal tier mapping + alasan sensitif untuk semua format metadata.
Digunakan sebagai fallback saat handler tidak menyediakan tiers.
"""
import re

# ============ Patterns per tier ============
TIER1_PATTERNS = [
    'author', 'creator', 'lastmodifiedby', 'lastsavedby', 'owner',
    'company', 'manager', 'artist', 'copyright', 'performer',
    'band', 'conductor', 'composer', 'lyricist', 'purchaser',
    'created', 'modified', 'lastprinted', 'creationdate',
    'modificationdate', 'datetimeoriginal', 'datetimedigitized',
    'datetime',
    'gps', 'gpsinfo', 'latitude', 'longitude', 'altitude',
    'make', 'model', 'serial', 'lensmake', 'lensmodel', 'lensinfo',
    'bodyserial', 'cameraserial', 'lensserial',
    'txxx', 'userdefinedtext', 'comment', 'comments',
    'lyrics', 'uslt', 'comm', 'ufid',
    'encodedby', 'encoder',
    'webpage', 'weburl', 'url',
    'subject', 'description', 'keywords', 'category',
    'contentstatus', 'revision',
    'tpe1', 'tpe2', 'tpe3', 'tpe4',
    'tcom', 'text', 'tenc', 'tsse', 'tcop', 'town', 'woar',
    'albumartist',
    'hostcomputer',
    'shutterspeed', 'aperture', 'iso', 'focallength',
    'exposuretime', 'exposureprogram', 'meteringmode', 'flash',
]

TIER2_PATTERNS = [
    'producer', 'application', 'appversion', 'template',
    'software', 'encodersettings', 'processingsoftware',
    'totaltime', 'slides', 'notes', 'hiddenslides', 'mmclips',
    'words', 'characters', 'lines', 'paragraphs',
    'headingpairs', 'titlesofparts', 'presentationformat',
    'shareddoc', 'hyperlinkschanged', 'linksuptodate', 'scalecrop',
    'docsecurity', 'pages', 'hyperlinkbase',
    'thumbnail', 'albumart', 'sldsz', 'notesz',
    'extlst', 'slide', 'name',
    'tags',
]

TIER3_PATTERNS = [
    'title', 'language', 'identifier', 'version', 'contenttype',
    'xresolution', 'yresolution', 'resolutionunit',
    'orientation', 'ycbcrpositioning', 'ycbcr',
    'imagewidth', 'imagelength', 'imageheight',
    'width', 'height',
    'exifoffset', 'interoperabilityoffset',
    'bitspersample', 'compression',
    'flashpixversion', 'exifversion',
    'colorspace', 'componentconfiguration',
]

# ============ Alasan sensitif (reason text) ============
REASONS = {
    'author': 'Mengungkap nama asli pembuat file dan dapat melacak pemilik aslinya.',
    'creator': 'Nama pengguna/aplikasi yang membuat file — bisa mengungkap identitas.',
    'lastmodifiedby': 'Menunjukkan siapa terakhir mengedit file — melacak rekan kerja atau aktivitas.',
    'company': 'Nama organisasi tempat file dibuat — bisa mengungkap afiliasi.',
    'manager': 'Nama atasan pembuat file — informasi jabatan internal.',
    'artist': 'Nama pembuat/pemilik karya — bisa melacak identitas.',
    'copyright': 'Klaim hak cipta — mengungkap pemilik legal file.',
    'performer': 'Nama pemain/pencipta audio.',
    'composer': 'Nama pencipta lagu.',
    'lyricist': 'Nama penulis lirik.',
    'owner': 'Nama pemilik lisensi atau pembeli.',
    'purchaser': 'Nama atau email pembeli — sangat sensitif.',

    'created': 'Waktu pasti file dibuat — bisa mengungkap jadwal/kebiasaan kerja.',
    'modified': 'Waktu terakhir file diedit — jejak aktivitas.',
    'lastprinted': 'Waktu file terakhir dicetak — bisa melacak aktivitas fisik.',
    'creationdate': 'Tanggal pembuatan yang sangat presisi.',
    'modificationdate': 'Tanggal modifikasi sangat presisi.',
    'datetimeoriginal': 'Waktu tepat foto diambil — sangat sensitif jika digabung dengan GPS.',
    'datetimedigitized': 'Waktu file difoto/disimpan ke memori digital.',

    'gps': 'Koordinat GPS lokasi pengambilan — sangat sensitif! Bisa melacak alamat rumah.',
    'gpsinfo': 'Data koordinat GPS + ketinggian — mengungkap lokasi persis.',
    'latitude': 'Garis lintang lokasi pengambilan.',
    'longitude': 'Garis bujur lokasi pengambilan.',
    'altitude': 'Ketinggian perangkat saat memotret.',

    'make': 'Merek perangkat/kamera yang digunakan.',
    'model': 'Model spesifik perangkat — bisa mengidentifikasi Anda.',
    'serial': 'Nomor seri unik perangkat — sangat sensitif untuk pelacakan.',
    'lensmake': 'Merek lensa yang digunakan.',
    'lensmodel': 'Model lensa — bisa melacak perlengkapan Anda.',

    'software': 'Perangkat lunak yang digunakan — mengungkap versi dan kebiasaan.',
    'application': 'Aplikasi yang membuat file — software fingerprinting.',
    'appversion': 'Versi aplikasi — bisa mengungkap sistem operasi.',
    'producer': 'Aplikasi/library yang menghasilkan file.',
    'encodersettings': 'Info encoder — fingerprinting software dan versi.',
    'processingsoftware': 'Software pengolah yang digunakan.',

    'txxx': 'User-defined text — sering menyimpan metadata teknis + jejak encoder.',
    'userdefinedtext': 'Teks kustom — bisa berisi apa saja termasuk identitas.',
    'lyrics': 'Lirik atau pesan tersembunyi.',
    'uslt': 'Lirik tidak tersinkronisasi.',
    'comment': 'Komentar — sering berisi catatan pribadi.',
    'comments': 'Komentar internal — bisa berisi catatan pribadi.',
    'ufid': 'ID unik file untuk pelacakan digital.',
    'albumart': 'Gambar sampul — kadang menyimpan EXIF tersembunyi.',
    'encodedby': 'Nama/akun yang mengonversi file.',
    'webpage': 'Tautan situs web pribadi atau komersial.',

    'subject': 'Subjek dokumen — bisa mengungkap topik sensitif.',
    'description': 'Deskripsi — bisa mengungkap konteks.',
    'keywords': 'Kata kunci — bisa mengungkap isi/topik.',
    'category': 'Kategori dokumen.',
    'revision': 'Nomor revisi — mengungkap riwayat edit.',
    'contentstatus': 'Status konten (draft/final) — bisa mengungkap tahapan.',

    'totaltime': 'Total waktu editing — bisa mengungkap pola kerja.',
    'words': 'Jumlah kata — fingerprinting struktur.',
    'pages': 'Jumlah halaman.',
    'slides': 'Jumlah slide presentasi.',
    'notes': 'Jumlah catatan.',
    'thumbnail': 'Thumbnail preview — kadang menyimpan versi asli belum dipotong.',

    'title': 'Judul file — biasanya tidak sensitif.',
    'language': 'Bahasa dokumen — umumnya aman.',
    'identifier': 'Pengenal file.',
    'version': 'Versi dokumen.',
    'contenttype': 'Tipe konten.',
    'xresolution': 'Resolusi horizontal — info teknis dasar.',
    'yresolution': 'Resolusi vertikal — info teknis dasar.',
    'resolutionunit': 'Satuan resolusi (DPI/inch).',
    'orientation': 'Orientasi gambar.',
    'imagewidth': 'Lebar gambar dalam piksel.',
    'imagelength': 'Tinggi gambar dalam piksel.',
    'imageheight': 'Tinggi gambar dalam piksel.',
    'exifoffset': 'Pointer internal EXIF — jangan dihapus manual.',
}


# ============ Helper ============
def _normalize(s):
    return re.sub(r'[^a-z0-9]', '', str(s).lower())


def _matches(norm_key, pattern):
    np = _normalize(pattern)
    if not np:
        return False
    if len(np) < 5:
        return (norm_key == np or
                norm_key.startswith(np) or
                norm_key.endswith(np))
    return np in norm_key


def get_universal_tier(field_key, field_label=''):
    """Tentukan tier (1/2/3) berdasarkan nama field."""
    candidates = []
    if ':' in field_key:
        candidates.append(field_key.split(':', 1)[-1])
    candidates.append(field_key)
    if field_label:
        candidates.append(field_label)

    normalized = [_normalize(c) for c in candidates if c]

    for tier, patterns in [(1, TIER1_PATTERNS), (2, TIER2_PATTERNS), (3, TIER3_PATTERNS)]:
        for n in normalized:
            for p in patterns:
                if _matches(n, p):
                    return tier
    return 3


def get_reason(field_key, field_label=''):
    """Dapatkan alasan mengapa metadata ini sensitif."""
    candidates = []
    if ':' in field_key:
        candidates.append(field_key.split(':', 1)[-1])
    candidates.append(field_key)
    if field_label:
        candidates.append(field_label)

    normalized = [_normalize(c) for c in candidates if c]

    for n in normalized:
        for k, v in REASONS.items():
            if n == _normalize(k):
                return v
    for n in normalized:
        for k, v in REASONS.items():
            nk = _normalize(k)
            if len(nk) >= 4 and nk in n:
                return v

    return 'Metadata ini mungkin mengandung informasi teknis atau identitas yang tidak Anda sadari.'