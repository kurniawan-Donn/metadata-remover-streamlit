"""
Metadata Remover — Main Application
Entry point untuk streamlit run app.py
"""
import io
import time
import traceback
from pathlib import Path

import streamlit as st

# ---------- Styling & Components ----------
from styles import inject_custom_css
from icons import render_icon
from theme import (
    init_theme, sync_theme_from_storage, apply_theme,
    render_theme_toggle, get_theme,
)
from components import (
    render_header,
    render_upload_zone,
    render_file_info_bar,
    render_metrics,
    render_section_header,
    render_tier_selector,
    render_metadata_card,
    render_empty_tier,
    render_preset_buttons,
    render_sticky_footer,
    build_confirm_dialog,
    render_success_screen,
    render_loader,
    render_processing_state,
    render_error_card,
    render_already_clean_card,
    render_batch_file_card,
    render_batch_summary,
    render_batch_progress,
    render_progress_panel,
    render_zip_summary,
    render_webhook_status,
    render_file_config_panel,
    render_apply_all_row,
)

# ---------- Backend ----------
from metadata_tiers import get_universal_tier
from handler_router import (
    process_file, remove_metadata,
    UnsupportedFormatError, ProcessingError,
    SUPPORTED_EXT,
)
from batch_handler import (
    scan_batch, clean_batch, build_zip,
    compute_batch_stats, compute_final_stats,
)
from progress_tracker import BatchProgress, humanize_duration
from webhook import send_webhook_notification, validate_webhook_url, test_webhook
from file_config import (
    init_file_configs, reset_all_configs, apply_pattern_to_all,
    resolve_all_names, is_customized, reset_config,
)
from sortable_list import render_sortable_file_list


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Metadata Remover",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_custom_css()


# ============================================================
# THEME
# ============================================================
init_theme()
if not st.session_state.get("theme_loaded"):
    sync_theme_from_storage()
    st.session_state.theme_loaded = True
apply_theme()


# ============================================================
# HELPERS
# ============================================================
def generate_output_name(original_name, option_or_config):
    """
    Wrapper: mendukung dua mode.
    - Single mode  : option_or_config = string (mis. "Akhir: [NamaFile]_clean.ext")
    - Batch mode   : option_or_config = dict config dari file_configs
    """
    if isinstance(option_or_config, dict):
        # Batch mode — delegate ke file_config (yang sudah handle dict config)
        from file_config import generate_output_name as _fc_gen
        return _fc_gen(original_name, option_or_config)

    # Single mode — string pattern
    option = str(option_or_config)
    stem = Path(original_name).stem
    suffix = Path(original_name).suffix
    if option.startswith("Akhir"):
        return f"{stem}_clean{suffix}"
    elif option.startswith("Awal"):
        return f"clean_{stem}{suffix}"
    return original_name



def render_reorder_fallback(scan_results, key_prefix="reorder"):
    """
    UI reorder alternatif dengan tombol ⬆/⬇.
    Dipakai sebagai fallback jika komponen sortable gagal dimuat.
    """
    if "batch_file_ids" not in st.session_state:
        st.session_state.batch_file_ids = [f"f{i}" for i in range(len(scan_results))]
    if "file_order" not in st.session_state:
        st.session_state.file_order = list(st.session_state.batch_file_ids)

    ids = st.session_state.batch_file_ids
    order = list(st.session_state.file_order)

    # Sync kalau ada mismatch (file baru masuk / file berkurang)
    if set(order) != set(ids):
        order = list(ids)
        st.session_state.file_order = order

    id_to_result = {ids[i]: scan_results[i] for i in range(len(scan_results))}

    for pos, fid in enumerate(order):
        r = id_to_result.get(fid)
        if not r:
            continue

        c1, c2, c3 = st.columns([7, 1, 1], vertical_alignment="center", gap="small")

        with c1:
            st.markdown(
                f"<div style='padding:10px 14px;background:var(--bg-card);"
                f"border:1px solid var(--border-soft);border-radius:10px;"
                f"display:flex;align-items:center;gap:10px;'>"
                f"<span style='font-weight:800;color:var(--brand-primary);"
                f"font-size:12px;min-width:32px;'>#{pos+1}</span>"
                f"<span style='font-weight:600;color:var(--text-primary);'>"
                f"{r['file_name']}</span>"
                f"<span style='color:var(--text-tertiary);font-size:11.5px;'>"
                f"({r['size_kb']:.1f} KB)</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        with c2:
            if pos > 0:
                if st.button("⬆", key=f"{key_prefix}_up_{fid}",
                             use_container_width=True,
                             help="Naikkan"):
                    order[pos], order[pos - 1] = order[pos - 1], order[pos]
                    st.session_state.file_order = order
                    st.rerun()

        with c3:
            if pos < len(order) - 1:
                if st.button("⬇", key=f"{key_prefix}_down_{fid}",
                             use_container_width=True,
                             help="Turunkan"):
                    order[pos], order[pos + 1] = order[pos + 1], order[pos]
                    st.session_state.file_order = order
                    st.rerun()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan")
    nama_option = st.radio(
        "Pola nama file hasil:",
        options=[
            "Akhir: [NamaFile]_clean.ext",
            "Awal: clean_[NamaFile].ext",
            "Sama: [NamaFile].ext",
        ],
        index=0,
        key="naming_option_sidebar",
    )

    st.markdown("---")
    st.markdown("### 🔔 Notifikasi Webhook")

    webhook_url = st.text_input(
        "URL Webhook (opsional)",
        value=st.session_state.get("webhook_url", ""),
        type="password",
        placeholder="https://discord.com/api/webhooks/...",
        help="Kirim notifikasi progress batch ke Discord/Slack.",
        key="webhook_url_input",
    )
    st.session_state.webhook_url = webhook_url

    notify_per_file = st.toggle(
        "Notifikasi per file selesai",
        value=st.session_state.get("webhook_per_file", False),
        help="Kirim notifikasi setiap file selesai diproses.",
        key="webhook_per_file_toggle",
    )
    st.session_state.webhook_per_file = notify_per_file

    is_valid, err = validate_webhook_url(webhook_url)
    render_webhook_status(webhook_url, is_valid, err)

    if webhook_url and is_valid:
        if st.button("Test Kirim", use_container_width=True, key="test_webhook_btn"):
            ok, _ = test_webhook(webhook_url)
            if ok:
                st.success("Terkirim! Cek channel Anda.")
            else:
                st.error("Gagal mengirim. Periksa URL.")

    st.markdown("---")
    st.markdown("### 🎨 Legenda Tier")
    st.markdown("""
    <div style='font-size:13px;line-height:1.9;'>
        <span class='badge badge-danger'>TIER 1</span>&nbsp; Identitas, GPS, waktu<br>
        <span class='badge badge-warning'>TIER 2</span>&nbsp; Software, struktur<br>
        <span class='badge badge-safe'>TIER 3</span>&nbsp; Info umum
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# HEADER (STICKY) + THEME TOGGLE
# ============================================================
from components import reset_uploader

with st.container(key="sticky_header"):
    _tc1, _tc2 = st.columns([9, 1], vertical_alignment="center")
    with _tc2:
        render_theme_toggle()
    render_header()


# ============================================================
# UPLOAD
# ============================================================
uploaded = render_upload_zone(multi=True)

if uploaded is None or (isinstance(uploaded, list) and len(uploaded) == 0):
    st.stop()

# Normalisasi ke list
if not isinstance(uploaded, list):
    uploaded = [uploaded]

# Tombol "Hapus File" (reset uploader)
_cb1, _cb2, _cb3 = st.columns([5, 1.3, 5])
with _cb2:
    if st.button("✕  Hapus File", use_container_width=True,
                 key="clear_upload_btn",
                 help="Batalkan file yang diupload dan pilih ulang"):
        reset_uploader()
        # Reset juga state terkait file
        for k in list(st.session_state.keys()):
            if k.startswith("file_id") or k.startswith("batch_id"):
                del st.session_state[k]
        st.rerun()

# ============================================================
# ROUTE: SINGLE vs BATCH
# ============================================================
if len(uploaded) == 1:
    uploaded_file = uploaded[0]
    # ==========================================
    # SINGLE MODE
    # ==========================================
    file_id = f"{uploaded_file.name}__{uploaded_file.size}"

    RESET_KEYS = {
        "file_id", "file_name", "ext", "file_type", "kind", "mime",
        "file_bytes", "meta", "tier_map", "extra",
        "output_bytes", "new_size", "removed_count", "total_count",
        "output_name", "output_mime", "confirmed", "scan_error",
    }

    if st.session_state.get("file_id") != file_id:
        for k in list(st.session_state.keys()):
            if k.startswith("toggle_") or k in RESET_KEYS:
                del st.session_state[k]
        st.session_state.file_id = file_id

        loader_slot = st.empty()
        with loader_slot.container():
            render_loader(
                "Menganalisis metadata",
                f"Membaca struktur file {Path(uploaded_file.name).suffix.lstrip('.').upper() or 'file'}",
            )

        try:
            result = process_file(uploaded_file)
            st.session_state.file_name = result["file_name"]
            st.session_state.ext = result["ext"]
            st.session_state.file_type = result["file_type"]
            st.session_state.kind = result["kind"]
            st.session_state.mime = result["mime"]
            st.session_state.file_bytes = result["file_bytes"]
            st.session_state.meta = result["meta"]
            st.session_state.extra = result["extra"]
            st.session_state.tier_map = {
                k: get_universal_tier(k, k) for k in result["meta"].keys()
            }
            st.session_state.scan_error = None
        except UnsupportedFormatError as e:
            st.session_state.scan_error = ("unsupported", str(e))
        except ProcessingError as e:
            st.session_state.scan_error = ("processing", str(e))
        except Exception as e:
            st.session_state.scan_error = ("unknown", str(e))
        finally:
            loader_slot.empty()

    if st.session_state.get("scan_error"):
        err_kind, err_msg = st.session_state.scan_error
        render_error_card(err_kind, err_msg, file_name=uploaded_file.name)
        st.stop()

    # Ambil state
    file_bytes = st.session_state.file_bytes
    file_name = st.session_state.file_name
    ext = st.session_state.ext
    ftype = st.session_state.file_type
    kind = st.session_state.kind
    mime = st.session_state.mime
    meta = st.session_state.meta
    tier_map = st.session_state.tier_map
    size_kb = len(file_bytes) / 1024

    render_file_info_bar(file_name, size_kb, ftype)

    if not meta:
        render_already_clean_card(file_name)
        st.stop()

    # Group per tier
    tier1_items = [(k, v) for k, v in meta.items() if tier_map.get(k) == 1]
    tier2_items = [(k, v) for k, v in meta.items() if tier_map.get(k) == 2]
    tier3_items = [(k, v) for k, v in meta.items() if tier_map.get(k) == 3]

    render_section_header("Ringkasan Analisis", icon_name="layers")
    render_metrics({
        "total": len(meta),
        "tier1": len(tier1_items),
        "tier2": len(tier2_items),
        "tier3": len(tier3_items),
    })

    render_section_header("Aksi Cepat", icon_name="zap")

    def apply_preset_single(max_tier):
        for k in meta.keys():
            t = tier_map.get(k, 3)
            st.session_state[f"toggle_{k}"] = (t <= max_tier)

    b_pii, b_meta, b_all = render_preset_buttons()
    if b_pii:
        apply_preset_single(1); st.rerun()
    if b_meta:
        apply_preset_single(2); st.rerun()
    if b_all:
        apply_preset_single(3); st.rerun()

    render_section_header("Detail Metadata", icon_name="search", count=len(meta))

    selected_tier = render_tier_selector({
        "tier1": len(tier1_items),
        "tier2": len(tier2_items),
        "tier3": len(tier3_items),
    })

    default_toggle = {"tier1": True, "tier2": True, "tier3": False}[selected_tier]
    current_items = {
        "tier1": tier1_items,
        "tier2": tier2_items,
        "tier3": tier3_items,
    }[selected_tier]

    if not current_items:
        render_empty_tier()
    else:
        for k, v in current_items:
            render_metadata_card(
                field_key=k,
                field_value=v,
                tier=tier_map.get(k, 3),
                toggle_key=f"toggle_{k}",
                default_value=default_toggle,
            )

    selected_keys = [k for k in meta.keys() if st.session_state.get(f"toggle_{k}", False)]
    trigger = render_sticky_footer(len(selected_keys), len(meta))

    if trigger and selected_keys:
        dialog = build_confirm_dialog(file_name, selected_keys)
        dialog()

    # Eksekusi
    if st.session_state.get("confirmed"):
        st.session_state.confirmed = False
        selected_now = [k for k in meta.keys() if st.session_state.get(f"toggle_{k}", False)]
        remove_all = (len(selected_now) == len(meta))

        proc_slot = st.empty()
        with proc_slot.container():
            render_processing_state("Membersihkan file")

        try:
            out = remove_metadata(ext, file_bytes, selected_now, remove_all)
            st.session_state.output_bytes = out
            st.session_state.new_size = len(out) / 1024
            st.session_state.removed_count = len(selected_now)
            st.session_state.total_count = len(meta)
            st.session_state.output_mime = mime
            st.session_state.output_name = generate_output_name(file_name, nama_option)
            st.session_state.scan_error = None
        except (ProcessingError, UnsupportedFormatError) as e:
            proc_slot.empty()
            render_error_card("processing", str(e), file_name=file_name)
            st.stop()
        except Exception as e:
            proc_slot.empty()
            render_error_card("unknown", str(e), file_name=file_name)
            st.stop()
        finally:
            proc_slot.empty()

    if st.session_state.get("output_bytes"):
        selected_now = [k for k in meta.keys() if st.session_state.get(f"toggle_{k}", False)]
        after_meta = {k: v for k, v in meta.items() if k not in selected_now}

        render_success_screen(
            output_bytes=st.session_state.output_bytes,
            output_name=st.session_state.output_name,
            original_kb=size_kb,
            new_kb=st.session_state.new_size,
            removed_count=st.session_state.removed_count,
            total_count=st.session_state.total_count,
            mime=st.session_state.output_mime,
            before_meta=meta,
            after_meta=after_meta,
        )

    st.stop()  # Jangan jatuh ke batch mode


# ============================================================
# BATCH MODE (>= 2 file)
# ============================================================
MAX_BATCH = 50
if len(uploaded) > MAX_BATCH:
    st.warning(f"Maksimum {MAX_BATCH} file per batch. Anda mengunggah {len(uploaded)} file.")
    uploaded = uploaded[:MAX_BATCH]

batch_id = "__".join(f"{f.name}_{f.size}" for f in uploaded)

if st.session_state.get("batch_id") != batch_id:
    for k in list(st.session_state.keys()):
        if k.startswith("batch_") and k != "batch_id":
            del st.session_state[k]
        elif k.startswith("btoggle_"):
            del st.session_state[k]
        elif k.startswith("cfg_"):
            del st.session_state[k]
        elif k == "file_configs":
            del st.session_state[k]

    st.session_state.batch_id = batch_id
    st.session_state.batch_scan_done = False

# Scan batch
if not st.session_state.get("batch_scan_done"):
    progress_slot = st.empty()

    def _scan_cb(cur, total, name):
        with progress_slot.container():
            if cur < total:
                render_batch_progress(cur, total, name, label="Memindai")
            else:
                st.markdown("""
                    <div class="progress-wrap">
                        <div class="progress-label">
                            <span>Pemindaian selesai</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    scan_results = scan_batch(uploaded, progress_callback=_scan_cb)
    progress_slot.empty()

    # Tambah tier_map per file
    for r in scan_results:
        if r["status"] == "ok" and r["info"]:
            r["tier_map"] = {
                k: get_universal_tier(k, k)
                for k in r["info"]["meta"].keys()
            }
        else:
            r["tier_map"] = {}

    st.session_state.batch_scan_results = scan_results
    st.session_state.batch_scan_done = True

scan_results = st.session_state.batch_scan_results


# ============================================================
# RINGKASAN BATCH
# ============================================================
stats = compute_batch_stats(scan_results)

render_section_header("Ringkasan Batch", icon_name="layers")
render_batch_summary(stats)


# ============================================================
# DAFTAR FILE
# ============================================================
render_section_header("Daftar File", icon_name="file-text", count=len(scan_results))

for r in scan_results:
    meta_count = 0
    if r["status"] == "ok" and r["info"]:
        meta_count = len(r["info"]["meta"])

    if r["status"] == "ok" and meta_count == 0:
        status = "clean"
    else:
        status = r["status"]

    render_batch_file_card(r["file_name"], r["size_kb"], status, meta_count)


# ============================================================
# URUTKAN FILE
# ============================================================
# Init state order
if st.session_state.get("batch_id_for_order") != st.session_state.batch_id:
    st.session_state.batch_file_ids = [f"f{i}" for i in range(len(scan_results))]
    st.session_state.file_order = list(st.session_state.batch_file_ids)
    st.session_state.sortable_version = 0
    st.session_state.batch_id_for_order = st.session_state.batch_id

if "use_sortable" not in st.session_state:
    st.session_state.use_sortable = True

render_section_header("Urutkan File", icon_name="layers")

# Toggle mode: Drag & Drop vs Tombol ⬆⬇
_tc1, _tc2 = st.columns([5, 1.5], vertical_alignment="center")
with _tc2:
    new_toggle = st.toggle(
        "Drag & Drop",
        value=st.session_state.use_sortable,
        key="use_sortable_toggle",
        help="Matikan jika drag & drop tidak muncul → gunakan tombol ⬆⬇",
    )
    if new_toggle != st.session_state.use_sortable:
        st.session_state.use_sortable = new_toggle
        st.rerun()

if st.session_state.use_sortable:
    st.markdown("""
        <div style="font-size:12.5px;color:var(--text-secondary);
                    margin:-6px 0 12px 0;line-height:1.5;">
            Tarik handle <b>⋮⋮</b> di kiri untuk memindahkan file.
            Jika tidak muncul, matikan toggle <b>Drag & Drop</b> di atas untuk pakai tombol ⬆⬇.
        </div>
    """, unsafe_allow_html=True)

    files_for_sortable = [
        {
            "id": st.session_state.batch_file_ids[i],
            "name": scan_results[i]["file_name"],
            "size_kb": scan_results[i]["size_kb"],
        }
        for i in range(len(scan_results))
    ]

    sortable_key = (
        f"sortable_{st.session_state.batch_id}"
        f"_{st.session_state.get('sortable_version', 0)}"
    )

    sort_result = None
    sortable_error = None
    try:
        sort_result = render_sortable_file_list(
            files_for_sortable,
            theme=get_theme(),
            key=sortable_key,
        )
    except Exception as e:
        sortable_error = str(e)

    if sortable_error:
        st.warning(
            f"⚠️ Komponen drag & drop gagal dimuat. "
            f"Matikan toggle di atas untuk pakai tombol ⬆⬇. Error: {sortable_error}"
        )

    if sort_result and isinstance(sort_result, dict):
        new_order = sort_result.get("order")
        if new_order and new_order != st.session_state.file_order:
            st.session_state.file_order = new_order
            st.rerun()
else:
    st.markdown("""
        <div style="font-size:12.5px;color:var(--text-secondary);
                    margin:-6px 0 12px 0;line-height:1.5;">
            Gunakan tombol <b>⬆</b> dan <b>⬇</b> untuk memindahkan file.
        </div>
    """, unsafe_allow_html=True)
    render_reorder_fallback(scan_results)

# Tombol Reset Urutan
_c1, _c2, _c3 = st.columns([3, 1.2, 3])
with _c2:
    if st.button("Reset Urutan", use_container_width=True, key="reset_file_order"):
        st.session_state.file_order = list(st.session_state.batch_file_ids)
        st.session_state.sortable_version = st.session_state.get("sortable_version", 0) + 1
        st.rerun()

# Reorder scan_results sesuai urutan user
_id_to_idx = {fid: i for i, fid in enumerate(st.session_state.batch_file_ids)}
_ordered = []
_seen = set()
for fid in st.session_state.file_order:
    idx = _id_to_idx.get(fid)
    if idx is not None and idx not in _seen:
        _ordered.append(scan_results[idx])
        _seen.add(idx)
for i, r in enumerate(scan_results):
    if i not in _seen:
        _ordered.append(r)
scan_results = _ordered


# ============================================================
# KONFIGURASI OUTPUT PER-FILE
# ============================================================
file_names = [r["file_name"] for r in scan_results]
init_file_configs(file_names)
file_configs = st.session_state.file_configs

render_section_header("Konfigurasi Output", icon_name="settings")

bulk_pattern = render_apply_all_row(file_names)
if bulk_pattern:
    apply_pattern_to_all(file_names, bulk_pattern)
    st.rerun()

_customized_count = sum(1 for n in file_names if is_customized(n, file_configs))
_custom_msg = f" · {_customized_count} file dengan pola custom" if _customized_count > 0 else ""

st.markdown(f"""
    <div style="font-size:12.5px;color:var(--text-secondary);
                margin:-6px 0 12px 0;line-height:1.5;">
        Atur nama output setiap file. Klik untuk membuka panel konfigurasi.
        {_custom_msg}
    </div>
""", unsafe_allow_html=True)

for r in scan_results:
    fname = r["file_name"]

    tier_info = {
        "tier1_on": 0, "tier1_total": 0,
        "tier2_on": 0, "tier2_total": 0,
        "tier3_on": 0, "tier3_total": 0,
    }
    if r["status"] == "ok" and r["info"]:
        for k in r["info"]["meta"].keys():
            t = r["tier_map"].get(k, 3)
            is_on = st.session_state.get(f"btoggle_{fname}_{k}", False)
            tier_info[f"tier{t}_total"] += 1
            if is_on:
                tier_info[f"tier{t}_on"] += 1

    cfg = file_configs.get(fname, {})
    is_custom = is_customized(fname, file_configs)
    badge_html = ' <span class="custom-badge">CUSTOM</span>' if is_custom else ""
    current_preview = generate_output_name(fname, cfg)

    with st.expander(f"📄 {fname}   →   {current_preview}", expanded=False):
        st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-size:13.5px;font-weight:700;color:var(--text-primary);">
                    {fname}
                </span>
                {badge_html}
            </div>
        """, unsafe_allow_html=True)

        render_file_config_panel(
            file_name=fname,
            config=cfg,
            tier_info=tier_info,
            key_prefix=f"cfg_{st.session_state.batch_id[:8]}",
        )

        rc1, rc2 = st.columns([3, 1])
        with rc2:
            if st.button("Reset", key=f"reset_cfg_{fname}", use_container_width=True):
                reset_config(fname)
                st.rerun()

_rsc1, _rsc2, _rsc3 = st.columns([3, 1.5, 3])
with _rsc2:
    if st.button("Reset Semua Konfigurasi", use_container_width=True, key="reset_all_configs"):
        reset_all_configs(file_names)
        st.rerun()


# ============================================================
# AKSI MASSAL (Global Preset)
# ============================================================
render_section_header("Aksi Massal", icon_name="zap")

def apply_global_preset(max_tier):
    for r in scan_results:
        if r["status"] != "ok" or not r["info"]:
            continue
        fname = r["file_name"]
        for k in r["info"]["meta"].keys():
            t = r["tier_map"].get(k, 3)
            st.session_state[f"btoggle_{fname}_{k}"] = (t <= max_tier)

b_pii, b_meta, b_all = render_preset_buttons()
if b_pii:
    apply_global_preset(1); st.rerun()
if b_meta:
    apply_global_preset(2); st.rerun()
if b_all:
    apply_global_preset(3); st.rerun()


# ============================================================
# DETAIL PER FILE
# ============================================================
render_section_header("Detail Per File", icon_name="search")

for r in scan_results:
    if r["status"] != "ok" or not r["info"] or not r["info"]["meta"]:
        continue

    fname = r["file_name"]
    meta = r["info"]["meta"]
    tier_map = r["tier_map"]

    with st.expander(f"📄 {fname}  ·  {len(meta)} metadata", expanded=False):
        grouped = {1: [], 2: [], 3: []}
        for k, v in meta.items():
            grouped[tier_map.get(k, 3)].append((k, v))

        for tier in (1, 2, 3):
            items = grouped[tier]
            if not items:
                continue

            tier_names = {1: "Tier 1 · Bahaya", 2: "Tier 2 · Peringatan", 3: "Tier 3 · Aman"}
            tier_icons = {1: "alert-triangle", 2: "alert-circle", 3: "check-circle"}
            icon_svg = render_icon(tier_icons[tier], size=14, stroke_width=2.4)

            st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:14px 0 8px 0;">
                    {icon_svg}
                    <span style="font-size:12.5px;font-weight:700;color:var(--text-secondary);
                                 text-transform:uppercase;letter-spacing:0.6px;">
                        {tier_names[tier]} ({len(items)})
                    </span>
                </div>
            """, unsafe_allow_html=True)

            default = tier != 3
            for k, v in items:
                toggle_key = f"btoggle_{fname}_{k}"
                if toggle_key not in st.session_state:
                    st.session_state[toggle_key] = default

                cols = st.columns([5, 1], vertical_alignment="center", gap="small")
                with cols[0]:
                    safe_val = str(v).replace("<", "&lt;").replace(">", "&gt;")
                    st.markdown(f"""
                        <div class="metadata-card tier{tier}" style="margin:0;">
                            <div class="meta-key">
                                <span style="font-size:12.5px;">{k}</span>
                            </div>
                            <div class="meta-value" style="font-size:11.5px;">{safe_val}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with cols[1]:
                    st.toggle("Pilih", value=default, key=toggle_key,
                              label_visibility="collapsed")


# ============================================================
# HITUNG TERPILIH
# ============================================================
selected_keys_map = {}
total_selected = 0

for r in scan_results:
    if r["status"] != "ok" or not r["info"]:
        continue
    fname = r["file_name"]
    keys = [
        k for k in r["info"]["meta"].keys()
        if st.session_state.get(f"btoggle_{fname}_{k}", False)
    ]
    selected_keys_map[fname] = keys
    total_selected += len(keys)


# ============================================================
# STICKY FOOTER
# ============================================================
trigger = render_sticky_footer(total_selected, stats["total_meta"])


# ============================================================
# DIALOG KONFIRMASI BATCH
# ============================================================
if trigger and total_selected > 0:
    @st.dialog("Konfirmasi Batch")
    def _batch_confirm():
        st.markdown(f"""
            <div class="dialog-file-info">
                <div class="lbl">Batch Target</div>
                <div class="val">{len([1 for k in selected_keys_map.values() if k])} file</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="dialog-warning">
                <b>{total_selected}</b> metadata akan dihapus permanen dari
                <b>{len([1 for k in selected_keys_map.values() if k])}</b> file.
                Tindakan ini tidak dapat dibatalkan.
            </div>
        """, unsafe_allow_html=True)

        with st.expander("Lihat daftar file & metadata"):
            for fname, keys in selected_keys_map.items():
                if keys:
                    st.caption(f"• **{fname}** — {len(keys)} metadata")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="small")
        with c1:
            if st.button("Batal", use_container_width=True, key="batch_cancel"):
                st.session_state.batch_confirmed = False
                st.rerun()
        with c2:
            if st.button("Ya, Lanjutkan", use_container_width=True,
                         type="primary", key="batch_confirm"):
                st.session_state.batch_confirmed = True
                st.rerun()

    _batch_confirm()


# ============================================================
# EKSEKUSI BATCH
# ============================================================
if st.session_state.get("batch_confirmed"):
    st.session_state.batch_confirmed = False

    _wh_url = st.session_state.get("webhook_url", "").strip()
    _wh_per_file = st.session_state.get("webhook_per_file", False)

    progress = BatchProgress()
    progress.start_batch(total_files=len(scan_results), phase="clean")

    if _wh_url:
        send_webhook_notification(_wh_url, "start", {
            "total_files": len(scan_results),
            "mode": "Batch Clean",
        })

    progress_slot = st.empty()
    out = []

    for i, r in enumerate(scan_results):
        progress.set_current(i, r["file_name"])
        file_start = time.time()

        with progress_slot.container():
            render_progress_panel(progress, label="Memproses")

        if r["status"] != "ok" or not r["info"] or not r["info"]["meta"]:
            duration = time.time() - file_start
            out.append({
                **r,
                "cleaned_bytes": None,
                "removed_count": 0,
                "total_count": 0,
                "status": "skipped",
            })
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
            progress.add_result(r["file_name"], "ok",
                                removed_count=len(keys), duration=duration)

            if _wh_url and _wh_per_file:
                send_webhook_notification(_wh_url, "file", {
                    "file_name": r["file_name"],
                    "removed_count": len(keys),
                    "duration_str": humanize_duration(duration),
                })
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
            progress.add_result(r["file_name"], "error",
                                removed_count=0, duration=duration,
                                error=str(e))

    progress.finish()

    with progress_slot.container():
        render_progress_panel(progress, label="Selesai", show_log=True)

    zip_bytes, zip_count = build_zip(
        out, configs=st.session_state.file_configs,
    )

    original_size_kb = sum(r["size_kb"] for r in out if r["status"] == "ok")
    final_stats = compute_final_stats(out, original_size_kb=original_size_kb)

    if _wh_url:
        send_webhook_notification(_wh_url, "done", {
            "total_files": progress.total_files,
            "total_removed": progress.total_removed,
            "files_done": progress.files_done,
            "files_failed": progress.files_failed,
            "files_skipped": progress.files_skipped,
            "duration_str": humanize_duration(progress.elapsed),
        })

    st.session_state.batch_cleaned = out
    st.session_state.batch_zip_bytes = zip_bytes
    st.session_state.batch_zip_count = zip_count
    st.session_state.batch_final_stats = final_stats
    st.session_state.batch_progress_final = progress.to_dict()


# ============================================================
# SUKSES BATCH — ZIP DOWNLOAD
# ============================================================
if st.session_state.get("batch_zip_bytes"):
    final_stats = st.session_state.batch_final_stats

    check_svg = render_icon("check", size=46, stroke_width=3.2, color="#FFFFFF")
    st.markdown(f"""
        <div class="success-wrap">
            <div class="success-circle">{check_svg}</div>
            <div class="success-title">Batch Selesai!</div>
            <p class="success-sub">Semua file yang dipilih telah dibersihkan.</p>
        </div>
    """, unsafe_allow_html=True)

    render_zip_summary(final_stats)

    st.download_button(
        label="Download ZIP Berisi File Bersih",
        data=st.session_state.batch_zip_bytes,
        file_name=f"metadata_clean_{len(st.session_state.batch_zip_bytes)}b.zip",
        mime="application/zip",
        use_container_width=True,
        key="download_zip",
    )

    with st.expander("Lihat hasil per file"):
        cleaned = st.session_state.batch_cleaned
        for r in cleaned:
            icon_status = {
                "ok": "check-circle",
                "error": "alert-triangle",
                "skipped": "info",
            }.get(r["status"], "info")

            icon = render_icon(icon_status, size=16, stroke_width=2.4)
            status_text = {
                "ok": f"{r['removed_count']} / {r['total_count']} metadata dihapus",
                "error": f"Gagal: {r.get('error', '—')}",
                "skipped": "Dilewati (tanpa metadata atau gagal scan)",
            }.get(r["status"], "")

            st.markdown(f"""
                <div class="file-card">
                    <div class="file-icon">{icon}</div>
                    <div class="file-body">
                        <div class="file-name">{r['file_name']}</div>
                        <div class="file-meta">{status_text}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)