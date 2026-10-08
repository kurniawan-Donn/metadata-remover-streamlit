"""
MP3 handler menggunakan mutagen.
Approach: parsing ID3v2 header secara manual untuk pemotongan yang bersih.
"""
import io
from mutagen.mp3 import MP3
from mutagen.id3 import ID3


SENSITIVE_LABELS = {
    'TPE1': 'Artist / Performer',
    'TPE2': 'Band / Orchestra',
    'TPE3': 'Conductor',
    'TCOM': 'Composer / Lyricist',
    'TEXT': 'Lyricist',
    'TENC': 'Encoded By / Author',
    'TCOP': 'Copyright / License',
    'WOAR': 'Artist Webpage / URL',
    'TOWN': 'Owner / Purchaser',
    'TSSE': 'Software / Encoder Settings',
    'UFID': 'Unique File Identifier (UFID)',
    'TDRC': 'Creation Date / Time',
    'TDAT': 'Creation Date / Time',
    'TYER': 'Creation Date / Time',
    'TDTG': 'Encoding Time / Release Time',
    'COMM': 'Comments',
    'USLT': 'Lyrics / Unsynchronized Lyrics',
    'TRCK': 'Track Number / Disc Number',
    'TPOS': 'Track Number / Disc Number',
    'APIC': 'Thumbnail / Album Art',
    'TXXX': 'User-Defined Text (TXXX)',
}


# ---------- Parsing metadata ----------
def _parse_id3(file_bytes):
    audio = MP3(io.BytesIO(file_bytes), ID3=ID3)
    tags = audio.tags
    meta = {}
    label_to_keys = {}
    if tags:
        for key, frame in tags.items():
            base_key = key.split(':')[0]
            label = SENSITIVE_LABELS.get(base_key, key)
            value = str(frame).replace('\x00', '')
            if label in meta:
                meta[label] += "; " + value
            else:
                meta[label] = value
            label_to_keys.setdefault(label, []).append(key)
    return audio, meta, label_to_keys


def read_metadata(file_bytes):
    _, meta, _ = _parse_id3(file_bytes)
    return meta, _


# ---------- Manual ID3 strip ----------
def _strip_id3v2(data):
    """Hapus semua ID3v2 tag dari awal file (mendukung footer)."""
    while len(data) >= 10 and data[:3] == b'ID3':
        size_bytes = data[6:10]
        size = ((size_bytes[0] & 0x7F) << 21) | \
               ((size_bytes[1] & 0x7F) << 14) | \
               ((size_bytes[2] & 0x7F) << 7)  | \
               (size_bytes[3] & 0x7F)
        total = 10 + size
        if len(data) > 5 and (data[5] & 0x10):
            total += 10
        if total >= len(data) or total <= 0:
            break
        data = data[total:]
    return data


def _strip_id3v1(data):
    if len(data) >= 128 and data[-128:-125] == b'TAG':
        return data[:-128]
    return data


def _strip_ape(data):
    if len(data) >= 32 and data[-32:-24] == b'APETAGEX':
        size = int.from_bytes(data[-20:-16], 'little')
        if 0 < size <= len(data):
            return data[:-size]
    return data


def _get_audio_bytes(data):
    data = _strip_id3v1(data)
    data = _strip_ape(data)
    data = _strip_id3v2(data)
    return data


def remove_metadata(file_bytes, selected_labels, remove_all=False):
    """
    Hapus metadata MP3. Bangun tag baru + tempelkan ke audio murni.
    """
    data = _strip_id3v1(file_bytes)
    data = _strip_ape(data)
    audio_data = _get_audio_bytes(data)

    if remove_all:
        return audio_data

    try:
        mp3 = MP3(io.BytesIO(data), ID3=ID3)
    except Exception:
        return audio_data

    old_tags = mp3.tags
    if old_tags is None or len(old_tags) == 0:
        return audio_data

    labels_to_remove = set(selected_labels)
    new_tags = ID3()
    kept = 0
    for key in list(old_tags.keys()):
        base_key = key.split(':')[0]
        label = SENSITIVE_LABELS.get(base_key, key)
        if label not in labels_to_remove:
            try:
                new_tags[key] = old_tags[key]
                kept += 1
            except Exception:
                pass

    if kept == 0:
        return audio_data

    tmp = io.BytesIO()
    new_tags.save(tmp, v1=0, v2_version=3)
    tmp.seek(0)
    tag_bytes = tmp.getvalue()

    if not tag_bytes.startswith(b'ID3'):
        return audio_data

    return tag_bytes + audio_data