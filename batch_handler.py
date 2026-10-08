"""
Backend untuk batch processing multi-file.
- Scan banyak file sekaligus dengan progress callback
- Bersihkan file sesuai pilihan per-file
- Bungkus hasil ke ZIP
"""
import io
import time
import zipfile
from pathlib import Path

from handler_router import (
    process_file,
    remove_metadata,
    get_file_info,
    UnsupportedFormatError,
    ProcessingError,
)


# ============================================================
# NAMING
# ============================================================
def generate_output_name(original_name, option="Akhir"):
    """Kembalikan nama file output sesuai pola pilihan user."""
    stem = Path(original_name).stem
    suffix = Path(original_name).suffix
    if option.startswith("Akhir"):
        return f"{stem}_clean{suffix}"
    elif option.startswith("Awal"):
        return f"clean_{stem}{suffix}"
    return original_name


def _unique_name(name, used: set):
    """Pastikan nama unik di dalam ZIP."""
    if name not in used:
        used.add(name)
        return name
    stem = Path(name).stem
    suffix = Path(name).suffix
    i = 2
    while f"{stem}_{i}{suffix}" in used:
        i += 1
    new = f"{stem}_{i}{suffix}"
    used.add(new)
    return new


# ============================================================
# SCAN BATCH
# ============================================================
def scan_batch(files, progress_callback=None):
    """
    Scan metadata untuk daftar file.
    Returns: list[dict] dengan struktur:
        {
            'file': UploadedFile,
            'file_name': str,
            'size_kb': float,
            'status': 'ok' | 'error' | 'unsupported',
            'info': dict | None,
            'error': str | None,
        }
    """
    total = len(files)
    results = []

    for i, f in enumerate(files):
        if progress_callback:
            progress_callback(i, total, f.name)

        name = f.name
        size_kb = f.size / 1024

        ext_info = get_file_info(name)
        if ext_info is None:
            results.append({
                "file": f,
                "file_name": name,
                "size_kb": size_kb,
                "status": "unsupported",
                "info": None,
                "error": f"Format `{Path(name).suffix}` belum didukung.",
            })
            continue

        try:
            info = process_file(f)
            results.append({
                "file": f,
                "file_name": name,
                "size_kb": size_kb,
                "status": "ok",
                "info": info,
                "error": None,
            })
        except UnsupportedFormatError as e:
            results.append({
                "file": f,
                "file_name": name,
                "size_kb": size_kb,
                "status": "unsupported",
                "info": None,
                "error": str(e),
            })
        except ProcessingError as e:
            results.append({
                "file": f,
                "file_name": name,
                "size_kb": size_kb,
                "status": "error",
                "info": None,
                "error": str(e),
            })
        except Exception as e:
            results.append({
                "file": f,
                "file_name": name,
                "size_kb": size_kb,
                "status": "error",
                "info": None,
                "error": str(e),
            })

    if progress_callback:
        progress_callback(total, total, "Selesai")

    return results


# ============================================================
# CLEAN BATCH (dengan progress tracker)
# ============================================================
def clean_batch(results, selected_keys_map, progress=None):
    """
    Bersihkan file sesuai pilihan.

    Args:
        results          : hasil scan_batch()
        selected_keys_map: {file_name: [keys]}
        progress         : BatchProgress instance (opsional, untuk tracking)

    Returns: list[dict] dengan tambahan:
        {
            'cleaned_bytes': bytes | None,
            'removed_count': int,
            'total_count'  : int,
            'status'       : 'ok' | 'error' | 'skipped',
        }
    """
    total = len(results)
    out = []

    if progress is not None:
        progress.start(total_files=total, phase="clean")

    for i, r in enumerate(results):
        if progress is not None:
            progress.set_current(i, r["file_name"])

        file_start = time.time()

        # Skip file gagal scan / tanpa metadata
        if r["status"] != "ok" or not r["info"] or not r["info"]["meta"]:
            duration = time.time() - file_start
            out.append({
                **r,
                "cleaned_bytes": None,
                "removed_count": 0,
                "total_count": 0,
                "status": "skipped",
            })
            if progress is not None:
                progress.add_result(r["file_name"], "skipped",
                                     removed_count=0, duration=duration)
            continue

        info = r["info"]
        keys = selected_keys_map.get(r["file_name"], [])
        total_meta = len(info["meta"])
        remove_all = (len(keys) == total_meta and total_meta > 0)

        try:
            cleaned = remove_metadata(
                info["ext"], info["file_bytes"], keys, remove_all,
            )
            duration = time.time() - file_start
            out.append({
                **r,
                "cleaned_bytes": cleaned,
                "removed_count": len(keys),
                "total_count": total_meta,
                "status": "ok",
            })
            if progress is not None:
                progress.add_result(r["file_name"], "ok",
                                     removed_count=len(keys), duration=duration)
        except Exception as e:
            duration = time.time() - file_start
            out.append({
                **r,
                "cleaned_bytes": None,
                "removed_count": 0,
                "total_count": total_meta,
                "status": "error",
                "error": str(e),
            })
            if progress is not None:
                progress.add_result(r["file_name"], "error",
                                     removed_count=0, duration=duration,
                                     error=str(e))

    if progress is not None:
        progress.finish()

    return out


# ============================================================
# ZIP BUILDER
# ============================================================
def build_zip(cleaned_results, configs=None, naming_option="Akhir"):
    """
    Bungkus file yang berhasil dibersihkan ke dalam ZIP.

    Args:
        cleaned_results : hasil clean_batch()
        configs         : dict {original_name: config_dict} (opsional)
                          Jika None, fallback ke naming_option global.
        naming_option   : str — hanya dipakai jika configs None.

    Returns: (bytes, jumlah_file)
    """
    from file_config import resolve_all_names

    buf = io.BytesIO()
    used = set()
    count = 0

    original_names = [
        r["file_name"] for r in cleaned_results
        if r.get("cleaned_bytes") is not None
    ]

    if configs:
        name_map = resolve_all_names(original_names, configs, ensure_unique=True)
    else:
        name_map = {}
        for n in original_names:
            if naming_option.startswith("Akhir"):
                stem = Path(n).stem
                suffix = Path(n).suffix
                out = f"{stem}_clean{suffix}"
            elif naming_option.startswith("Awal"):
                stem = Path(n).stem
                suffix = Path(n).suffix
                out = f"clean_{stem}{suffix}"
            else:
                out = n
            name_map[n] = out

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for r in cleaned_results:
            if r.get("cleaned_bytes") is None:
                continue
            original = r["file_name"]
            out_name = name_map.get(original, original)
            final = _unique_name(out_name, used)
            zf.writestr(final, r["cleaned_bytes"])
            count += 1

    buf.seek(0)
    return buf.getvalue(), count


# ============================================================
# STATISTIK
# ============================================================
def compute_batch_stats(scan_results):
    """Hitung statistik batch dari hasil scan."""
    total_files = len(scan_results)
    ok_files = [r for r in scan_results if r["status"] == "ok"]
    error_files = [r for r in scan_results if r["status"] == "error"]
    unsupported = [r for r in scan_results if r["status"] == "unsupported"]

    total_meta = 0
    total_size_kb = 0.0
    files_with_meta = 0

    for r in ok_files:
        total_size_kb += r["size_kb"]
        info = r["info"]
        if info and info["meta"]:
            files_with_meta += 1
            total_meta += len(info["meta"])

    return {
        "total_files": total_files,
        "ok_files": len(ok_files),
        "error_files": len(error_files),
        "unsupported_files": len(unsupported),
        "files_with_meta": files_with_meta,
        "files_clean": len(ok_files) - files_with_meta,
        "total_meta": total_meta,
        "total_size_kb": total_size_kb,
    }


def compute_final_stats(cleaned_results, original_size_kb=0.0):
    """Hitung statistik akhir setelah pembersihan."""
    success = [r for r in cleaned_results if r["status"] == "ok"]
    failed = [r for r in cleaned_results if r["status"] == "error"]
    skipped = [r for r in cleaned_results if r["status"] == "skipped"]

    total_removed = sum(r["removed_count"] for r in success)
    total_before = sum(r["total_count"] for r in success)

    new_size_bytes = sum(len(r["cleaned_bytes"]) for r in success if r.get("cleaned_bytes"))
    new_size_kb = new_size_bytes / 1024

    return {
        "success_count": len(success),
        "failed_count": len(failed),
        "skipped_count": len(skipped),
        "total_removed": total_removed,
        "total_before": total_before,
        "new_size_kb": new_size_kb,
        "original_size_kb": original_size_kb,
    }