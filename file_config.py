"""
Manajemen konfigurasi output per-file untuk batch mode.
"""
import re
from datetime import datetime
from pathlib import Path

ILLEGAL_CHARS = r'[/\\:*?"<>|]'
ILLEGAL_CHAR_REGEX = re.compile(ILLEGAL_CHARS)

PATTERN_OPTIONS = {
    "suffix":    "[NamaAsli]_clean.ext",
    "prefix":    "clean_[NamaAsli].ext",
    "timestamp": "[NamaAsli]_[Timestamp].ext",
    "custom":    "Custom (nama manual)",
}


# ============================================================
# STATE
# ============================================================
def init_file_configs(file_names):
    """Inisialisasi default config untuk setiap file."""
    import streamlit as st
    if "file_configs" not in st.session_state:
        st.session_state.file_configs = {}

    configs = st.session_state.file_configs

    for name in file_names:
        if name not in configs:
            base = Path(name).stem
            ext = Path(name).suffix
            configs[name] = {
                "pattern": "suffix",
                "custom_base": base,
                "ext": ext,
                "is_default": True,
            }
    return configs


def reset_config(name):
    import streamlit as st
    base = Path(name).stem
    ext = Path(name).suffix
    st.session_state.file_configs[name] = {
        "pattern": "suffix",
        "custom_base": base,
        "ext": ext,
        "is_default": True,
    }


def reset_all_configs(file_names):
    for name in file_names:
        reset_config(name)


def apply_pattern_to_all(file_names, pattern):
    import streamlit as st
    for name in file_names:
        cfg = st.session_state.file_configs.get(name)
        if not cfg:
            continue
        cfg["pattern"] = pattern
        if pattern == "custom":
            cfg["custom_base"] = Path(name).stem
        cfg["is_default"] = (pattern == "suffix")


# ============================================================
# VALIDATION
# ============================================================
def sanitize_base_name(base):
    if not base:
        return "file"
    cleaned = ILLEGAL_CHAR_REGEX.sub("_", str(base))
    cleaned = cleaned.strip().strip(".")
    if not cleaned:
        return "file"
    return cleaned


def validate_base_name(base):
    if not base or not base.strip():
        return False, "Nama file tidak boleh kosong."
    if ILLEGAL_CHAR_REGEX.search(base):
        return False, "Nama mengandung karakter ilegal: / \\ : * ? \" < > |"
    if base.strip() in (".", ".."):
        return False, "Nama file tidak valid."
    return True, None


# ============================================================
# PREVIEW & RESOLVE
# ============================================================
def generate_output_name(original_name, config, timestamp=None):
    if not config:
        stem = Path(original_name).stem
        return f"{stem}_clean{Path(original_name).suffix}"

    pattern = config.get("pattern", "suffix")
    ext = config.get("ext") or Path(original_name).suffix
    base = Path(original_name).stem

    if pattern == "suffix":
        return f"{base}_clean{ext}"
    elif pattern == "prefix":
        return f"clean_{base}{ext}"
    elif pattern == "timestamp":
        ts = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base}_{ts}{ext}"
    elif pattern == "custom":
        custom = sanitize_base_name(config.get("custom_base", base))
        return f"{custom}{ext}"
    return f"{base}_clean{ext}"


def resolve_all_names(file_names, configs, ensure_unique=True):
    """Hasilkan mapping {original_name: output_name} untuk semua file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mapping = {}
    used = {}

    for name in file_names:
        cfg = configs.get(name, {})
        out = generate_output_name(name, cfg, timestamp=timestamp)

        if ensure_unique:
            if out.lower() in used:
                stem = Path(out).stem
                suffix = Path(out).suffix
                i = used[out.lower()] + 1
                while f"{stem}_{i}{suffix}".lower() in used:
                    i += 1
                out = f"{stem}_{i}{suffix}"
                used[out.lower()] = i
            else:
                used[out.lower()] = 0

        mapping[name] = out

    return mapping


def is_customized(name, configs):
    cfg = configs.get(name)
    if not cfg:
        return False
    if cfg.get("pattern") != "suffix":
        return True
    base = Path(name).stem
    if cfg.get("custom_base", base) != base:
        return True
    return False