"""
Image handler untuk JPEG/JPG, PNG, WebP.
Menggunakan Pillow + EXIF parsing.
"""
import io
from PIL import Image, ExifTags


SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


TAG_LABELS = {
    0x0100: 'Image Width (Lebar Gambar)',
    0x0101: 'Image Height (Tinggi Gambar)',
    0x010E: 'Image Description (Deskripsi Gambar)',
    0x010F: 'Make (Merek Perangkat)',
    0x0110: 'Model (Model Perangkat)',
    0x0112: 'Orientation (Orientasi)',
    0x011A: 'X Resolution (Resolusi Horizontal)',
    0x011B: 'Y Resolution (Resolusi Vertikal)',
    0x0128: 'Resolution Unit (Satuan Resolusi)',
    0x0131: 'Software (Perangkat Lunak)',
    0x0132: 'Modify Date (Tanggal Modifikasi)',
    0x013B: 'Artist (Pembuat)',
    0x0213: 'YCbCr Positioning (Posisi Warna)',
    0x8298: 'Copyright (Hak Cipta)',
    0x8769: 'Exif Offset (Internal)',
    0x8825: 'GPS Info (Data GPS)',
    0x9003: 'DateTime Original (Tanggal Pengambilan)',
    0x9004: 'DateTime Digitized (Tanggal Digitalisasi)',
    0x9201: 'Shutter Speed Value (Kecepatan Rana)',
    0x9202: 'Aperture Value (Bukaan Lensa)',
    0x9204: 'Exposure Bias (Kompensasi Pencahayaan)',
    0x9207: 'Metering Mode (Mode Pengukuran Cahaya)',
    0x9209: 'Flash (Status Flash)',
    0x920A: 'Focal Length (Jarak Fokus)',
    0xA431: 'Serial Number (Nomor Seri)',
    0xA432: 'Lens Info (Info Lensa)',
    0xA433: 'Lens Make (Merek Lensa)',
    0xA434: 'Lens Model (Model Lensa)',
}


def _get_tag_name(tag_id):
    if tag_id in TAG_LABELS:
        return TAG_LABELS[tag_id]
    if tag_id in ExifTags.TAGS:
        return ExifTags.TAGS[tag_id]
    return f"Tag 0x{tag_id:04X}"


def _clean_value(value):
    if isinstance(value, bytes):
        value = value.decode('utf-8', errors='ignore')
    elif not isinstance(value, str):
        value = str(value)
    return value.replace('\x00', '').strip()


def get_category(tag_name):
    tag_name = str(tag_name)
    if 'GPS' in tag_name or 'Altitude' in tag_name or 'Latitude' in tag_name or 'Longitude' in tag_name:
        return 'Lokasi Fisik (Geolokasi)'
    elif tag_name in ['Make', 'Model', 'Serial Number', 'Lens Make', 'Lens Model',
                       'Body Serial Number', 'Lens Serial Number'] or 'Serial' in tag_name:
        return 'Perangkat & Identitas Hardware'
    elif tag_name in ['Aperture Value', 'Shutter Speed Value', 'ISO Speed Ratings',
                       'Focal Length', 'Flash', 'Exposure Time', 'Exposure Program',
                       'Metering Mode']:
        return 'Pengaturan Teknis Kamera'
    elif tag_name in ['DateTime Original', 'DateTime Digitized', 'Offset Time Original',
                       'Offset Time Digitized', 'Modify Date', 'Create Date']:
        return 'Waktu & Kronologi'
    elif tag_name in ['Software', 'Processing Software', 'Host Computer']:
        return 'Riwayat Pengeditan & Software'
    elif tag_name in ['Artist', 'Copyright', 'Image Description', 'XPTitle',
                       'XPComment', 'XPAuthor', 'XPKeywords']:
        return 'Hak Cipta & Identitas Pembuat'
    elif 'Thumbnail' in tag_name or 'JPEGThumbnail' in tag_name:
        return 'Thumbnail'
    return 'Lainnya'


def read_metadata(file_bytes):
    """
    Baca metadata EXIF.
    Returns: (meta, img, tag_map, all_fields)
    """
    img = Image.open(io.BytesIO(file_bytes))
    exif = img.getexif()
    meta = {}
    tag_map = {}
    all_fields = []

    if exif:
        for tag_id, value in exif.items():
            tag_name = _get_tag_name(tag_id)
            clean_val = _clean_value(value)
            label = tag_name
            meta[label] = clean_val
            tag_map.setdefault(label, []).append(tag_id)
            category = get_category(tag_name)
            all_fields.append({
                'tag_id': tag_id,
                'label': label,
                'value': clean_val,
                'category': category,
            })

    return meta, img, tag_map, all_fields


def remove_metadata(file_bytes, selected_categories=None, selected_labels=None,
                     remove_all=False):
    """
    Hapus metadata EXIF.
    Bisa hapus berdasarkan kategori, berdasarkan label, atau semua.
    Returns: bytes
    """
    img = Image.open(io.BytesIO(file_bytes))
    exif = img.getexif()

    if not exif:
        return file_bytes

    if remove_all:
        data = list(img.getdata())
        new_img = Image.new(img.mode, img.size)
        new_img.putdata(data)
        output = io.BytesIO()
        new_img.save(output, format=img.format)
        return output.getvalue()

    tags_to_delete = set()

    if selected_categories:
        for tag_id in exif.keys():
            tag_name = _get_tag_name(tag_id)
            if get_category(tag_name) in selected_categories:
                tags_to_delete.add(tag_id)

    if selected_labels:
        for label in selected_labels:
            for tag_id in exif.keys():
                current_label = _get_tag_name(tag_id)
                if current_label == label:
                    tags_to_delete.add(tag_id)

    for tag_id in tags_to_delete:
        if tag_id in exif:
            del exif[tag_id]

    output = io.BytesIO()
    img.save(output, format=img.format, exif=exif.tobytes() if exif else b'')
    return output.getvalue()