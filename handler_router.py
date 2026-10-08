"""
Router untuk deteksi tipe file & pemanggilan handler yang sesuai.
Menormalisasi output handler menjadi struktur seragam.
"""
from pathlib import Path

from handlers import (
    pdf_handler, image_handler, audio_handler,
    Docx_handler, Xlsx_handler, Pptx_handler,
)


# ============================================================
# REGISTRY
# ============================================================
HANDLERS = {
    ".pdf":  (pdf_handler,   "PDF",  "application/pdf",                                                          "pdf"),
    ".jpg":  (image_handler, "JPEG", "image/jpeg",                                                               "image"),
    ".jpeg": (image_handler, "JPEG", "image/jpeg",                                                               "image"),
    ".png":  (image_handler, "PNG",  "image/png",                                                                "image"),
    ".webp": (image_handler, "WebP", "image/webp",                                                               "image"),
    ".docx": (Docx_handler,  "DOCX", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  "office"),
    ".xlsx": (Xlsx_handler,  "XLSX", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",         "office"),
    ".pptx": (Pptx_handler,  "PPTX", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "office"),
    ".mp3":  (audio_handler, "MP3",  "audio/mpeg",                                                               "audio"),
}

SUPPORTED_EXT = tuple(HANDLERS.keys())


# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================
class UnsupportedFormatError(Exception):
    """Ekstensi file tidak didukung."""


class ProcessingError(Exception):
    """Handler gagal memproses file (korup, terenkripsi, dll)."""


# ============================================================
# HELPERS
# ============================================================
def get_file_info(filename):
    """Kembalikan dict info tipe file, atau None jika tidak didukung."""
    ext = Path(filename).suffix.lower()
    if ext not in HANDLERS:
        return None
    handler, display_name, mime, kind = HANDLERS[ext]
    return {
        "ext": ext,
        "handler": handler,
        "display_name": display_name,
        "mime": mime,
        "kind": kind,
    }


def _is_tiers_dict(obj):
    return (
        isinstance(obj, dict)
        and set(obj.keys()) >= {"tier1", "tier2", "tier3"}
    )


# ============================================================
# PROCESS (SCAN)
# ============================================================
def process_file(uploaded_file):
    """
    Scan metadata dari file yang diupload.
    Returns dict dengan struktur:
        {
            'file_name': str,
            'ext': str,
            'file_bytes': bytes,
            'file_type': str,
            'kind': str,
            'mime': str,
            'meta': dict,
            'extra': dict,
        }
    Raises: UnsupportedFormatError, ProcessingError
    """
    file_name = uploaded_file.name
    info = get_file_info(file_name)

    if info is None:
        raise UnsupportedFormatError(
            f"Format file `{Path(file_name).suffix}` belum didukung."
        )

    try:
        file_bytes = uploaded_file.getvalue()
    except Exception as e:
        raise ProcessingError(f"Gagal membaca file dari upload: {e}") from e

    handler = info["handler"]
    kind = info["kind"]

    try:
        result = handler.read_metadata(file_bytes)
    except Exception as e:
        raise ProcessingError(
            f"Gagal membaca {info['display_name']}. "
            f"Pastikan file tidak rusak atau terenkripsi. ({e})"
        ) from e

    meta = {}
    extra = {}

    if kind == "pdf":
        meta, doc = result
        extra["doc"] = doc

    elif kind == "image":
        meta, img, tag_map, all_fields = result
        extra["img"] = img
        extra["tag_map"] = tag_map
        extra["all_fields"] = all_fields

    elif kind == "audio":
        meta, audio = result
        extra["audio"] = audio

    elif kind == "office":
        meta, second = result
        if _is_tiers_dict(second):
            extra["tiers"] = second
        else:
            extra["tree"] = second

    return {
        "file_name": file_name,
        "ext": info["ext"],
        "file_bytes": file_bytes,
        "file_type": info["display_name"],
        "kind": kind,
        "mime": info["mime"],
        "meta": meta or {},
        "extra": extra,
    }


# ============================================================
# REMOVE
# ============================================================
def remove_metadata(ext, file_bytes, selected_keys, remove_all):
    """
    Hapus metadata dari file.
    Returns: bytes
    Raises: UnsupportedFormatError, ProcessingError
    """
    ext = ext.lower()
    if ext not in HANDLERS:
        raise UnsupportedFormatError(f"Format `{ext}` belum didukung.")

    handler, display_name, _, kind = HANDLERS[ext]

    try:
        if kind == "image":
            return handler.remove_metadata(
                file_bytes,
                selected_categories=None,
                selected_labels=selected_keys,
                remove_all=remove_all,
            )
        return handler.remove_metadata(file_bytes, selected_keys, remove_all)
    except Exception as e:
        raise ProcessingError(
            f"Gagal menghapus metadata dari {display_name}: {e}"
        ) from e