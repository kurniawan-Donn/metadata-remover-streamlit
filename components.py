"""
Semua komponen UI untuk Metadata Remover.
Setiap fungsi `render_*` dipanggil oleh app.py.

Catatan: File ini melakukan monkey-patch pada st.markdown agar otomatis
menghapus indentasi (dedent) pada HTML yang di-render dengan
unsafe_allow_html=True. Ini mencegah HTML muncul sebagai code block.
"""
from pathlib import Path
import textwrap

import streamlit as st

from icons import render_icon
from metadata_tiers import get_reason
from progress_tracker import humanize_duration
from file_config import (
    PATTERN_OPTIONS, validate_base_name, sanitize_base_name,
    generate_output_name, is_customized,
)

import re

# ============================================================
# MONKEY-PATCH: HTML block-safe markdown
# CommonMark memutus HTML block pada baris kosong, sehingga tag
# setelahnya dirender sebagai teks. Patch ini:
#   1. Dedent (hapus indentasi umum)
#   2. Deteksi HTML tag
#   3. Collapse multi-baris jadi satu baris
# ============================================================
_orig_markdown = st.markdown

_HTML_TAG_RE = re.compile(
    r"<\s*(div|span|h[1-6]|p|br|hr|ul|ol|li|table|tr|td|th|"
    r"svg|path|circle|line|polyline|polygon|rect|g|"
    r"strong|em|b|i|a|section|header|footer|main|aside|"
    r"figure|figcaption|article|nav)\b",
    re.IGNORECASE,
)


def _collapse_html(body):
    """Gabungkan HTML multi-baris jadi satu baris agar HTML block tidak terputus."""
    body = textwrap.dedent(body)
    lines = [ln.strip() for ln in body.split("\n") if ln.strip()]
    return " ".join(lines)


def _patched_markdown(body, *args, **kwargs):
    if kwargs.get("unsafe_allow_html") and isinstance(body, str):
        body = textwrap.dedent(body)
        if _HTML_TAG_RE.search(body):
            body = _collapse_html(body)
    return _orig_markdown(body, *args, **kwargs)


st.markdown = _patched_markdown
# ============================================================

# ============================================================
# HEADER
# ============================================================
def render_header():
    icon_shield = render_icon("shield-check", size=12, stroke_width=2.4)
    check = render_icon("check", size=15, stroke_width=2.4)

    st.markdown(f"""
<div class="hero">
    <div class="hero-badge">
        {icon_shield}
        PRIVACY TOOLKIT
    </div>

    <h1 class="hero-title">
        Bersihkan <span class="accent">Metadata</span>.<br>
        Lindungi Privasi Anda.
    </h1>

    <p class="hero-subtitle">
        Analisis dan hapus metadata sensitif —
        <strong>identitas</strong>, <strong>lokasi GPS</strong>,
        <strong>jejak waktu</strong>, dan
        <strong>informasi perangkat</strong> —
        dari file Anda sebelum dibagikan ke publik.
    </p>

    <div class="hero-meta">
        <div class="hero-meta-item">{check} 100% Offline</div>
        <div class="hero-meta-item">{check} File Tidak Diunggah</div>
        <div class="hero-meta-item">{check} Gratis & Open Source</div>
    </div>
</div>
    """, unsafe_allow_html=True)


# ============================================================
# UPLOAD ZONE
# ============================================================
def render_upload_zone(multi=False):
    """Area upload custom-styled dengan dukungan reset via version key."""
    # Version counter untuk reset uploader
    if "uploader_version" not in st.session_state:
        st.session_state.uploader_version = 0

    key = f"main_uploader_v{st.session_state.uploader_version}"

    uploaded = st.file_uploader(
        label="Upload file",
        type=None,
        accept_multiple_files=multi,
        label_visibility="collapsed",
        key=key,
    )

    is_empty = uploaded is None or (isinstance(uploaded, list) and len(uploaded) == 0)

    if is_empty:
        st.markdown("""
<div style="text-align:center;padding:18px 0 0 0;color:var(--text-tertiary);
            font-size:12.5px;font-weight:500;letter-spacing:0.2px;">
    Mendukung: PDF · JPG · PNG · WebP · DOCX · XLSX · PPTX · MP3
    <br><span style="font-size:11.5px;">Unggah 1 file untuk mode tunggal, atau beberapa file untuk mode batch.</span>
</div>
        """, unsafe_allow_html=True)

    return uploaded


def reset_uploader():
    """Reset file uploader dengan bump version."""
    st.session_state.uploader_version = st.session_state.get("uploader_version", 0) + 1

# ============================================================
# SECTION HEADER
# ============================================================
def render_section_header(title, icon_name=None, count=None):
    icon_html = render_icon(icon_name, size=17, stroke_width=2.2) if icon_name else ""
    count_html = (
        f'<span style="margin-left:auto;font-size:11px;font-weight:700;'
        f'color:var(--text-secondary);background:#F1F5F9;padding:3px 10px;'
        f'border-radius:999px;">{count}</span>'
    ) if count is not None else ""

    st.markdown(f"""
<div class="section-header" style="justify-content:space-between;">
    <div style="display:flex;align-items:center;gap:10px;">
        {icon_html}
        <h2>{title}</h2>
    </div>
    {count_html}
</div>
    """, unsafe_allow_html=True)


def render_file_info_bar(file_name, size_kb, file_type, extra=None):
    """File info bar dengan layout grid 3 kolom sejajar."""
    extra_html = ""
    if extra:
        for k, v in extra.items():
            extra_html += f"""
<div class="file-info-item">
    <div class="label">{k}</div>
    <div class="value">{v}</div>
</div>"""

    st.markdown(f"""
<div class="file-info-bar">
    <div class="file-info-item">
        <div class="label">📄 FILE</div>
        <div class="value">{file_name}</div>
    </div>
    <div class="file-info-item">
        <div class="label">UKURAN</div>
        <div class="value">{size_kb:.1f} KB</div>
    </div>
    <div class="file-info-item">
        <div class="label">TIPE</div>
        <div class="value">{file_type}</div>
    </div>
    {extra_html}
</div>
    """, unsafe_allow_html=True)

# ============================================================
# METRICS
# ============================================================
def render_metrics(metadata_counts):
    total = metadata_counts.get("total", 0)
    tier1 = metadata_counts.get("tier1", 0)
    tier2 = metadata_counts.get("tier2", 0)
    tier3 = metadata_counts.get("tier3", 0)

    cards = [
        {"accent": "accent-brand", "icon": "layers",         "value": total, "label": "Total Metadata",     "sub": "Terdeteksi di file"},
        {"accent": "accent-tier1", "icon": "alert-triangle", "value": tier1, "label": "Tier 1 · Bahaya",     "sub": "Identitas & lokasi"},
        {"accent": "accent-tier2", "icon": "alert-circle",   "value": tier2, "label": "Tier 2 · Peringatan", "sub": "Software & struktur"},
        {"accent": "accent-tier3", "icon": "check-circle",   "value": tier3, "label": "Tier 3 · Aman",       "sub": "Informasi umum"},
    ]

    cols = st.columns(4, gap="medium")
    for col, card in zip(cols, cards):
        with col:
            svg = render_icon(card["icon"], size=17, stroke_width=2.4)
            st.markdown(f"""
<div class="metric-card {card['accent']}">
    <div class="metric-icon">{svg}</div>
    <div>
        <div class="metric-value">{card['value']}</div>
        <div class="metric-label">{card['label']}</div>
        <div class="metric-sub">{card['sub']}</div>
    </div>
</div>
            """, unsafe_allow_html=True)


# ============================================================
# TIER SELECTOR (segmented control)
# ============================================================
def render_tier_selector(tier_counts):
    options = {
        "tier1": f"Tier 1 · Bahaya ({tier_counts.get('tier1', 0)})",
        "tier2": f"Tier 2 · Peringatan ({tier_counts.get('tier2', 0)})",
        "tier3": f"Tier 3 · Aman ({tier_counts.get('tier3', 0)})",
    }
    labels = list(options.values())
    keys = list(options.keys())

    selected_label = st.radio(
        "Pilih tier metadata:",
        options=labels,
        horizontal=True,
        label_visibility="collapsed",
        key="tier_selector",
    )
    return keys[labels.index(selected_label)]


# ============================================================
# METADATA CARD
# ============================================================
def render_metadata_card(field_key, field_value, tier, toggle_key, default_value):
    # Inisialisasi state — HANYA jika belum ada
    if toggle_key not in st.session_state:
        st.session_state[toggle_key] = default_value

    badge_text = {1: "TIER 1", 2: "TIER 2", 3: "TIER 3"}[tier]
    tier_class = f"tier{tier}"
    reason = get_reason(field_key, "")

    safe_reason = reason.replace('"', "&quot;").replace("'", "&#39;")
    safe_value = str(field_value).replace("<", "&lt;").replace(">", "&gt;")

    cols = st.columns([3, 1], vertical_alignment="center", gap="small")
    with cols[0]:
        st.markdown(f"""
<div class="metadata-card {tier_class}">
    <div class="meta-key">
        <span>{field_key}</span>
        <span class="meta-badge {tier_class}">{badge_text}</span>
        <span class="info-icon" data-tooltip="💡 {safe_reason}">i</span>
    </div>
    <div class="meta-value">{safe_value}</div>
</div>
        """, unsafe_allow_html=True)
    with cols[1]:
        # JANGAN pakai value=default_value — biar Streamlit ambil dari session_state
        st.toggle("Pilih", key=toggle_key, label_visibility="collapsed")


# ============================================================
# EMPTY STATE
# ============================================================
def render_empty_tier():
    icon = render_icon("check-circle-2", size=32, stroke_width=2, color="#10B981")
    st.markdown(f"""
<div class="empty-tier">
    <div style="margin-bottom:10px;opacity:0.85;">{icon}</div>
    Tidak ada metadata pada tier ini.
</div>
    """, unsafe_allow_html=True)


# ============================================================
# PRESET BUTTONS
# ============================================================
def render_preset_buttons():
    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        b_pii = st.button(
            "Hapus Semua PII", use_container_width=True,
            help="Hanya Tier 1: identitas, GPS, jejak waktu.",
            key="preset_pii",
        )
    with c2:
        b_meta = st.button(
            "Hapus Metadata Pribadi", use_container_width=True,
            help="Tier 1 + Tier 2: PII + software fingerprinting.",
            key="preset_meta",
        )
    with c3:
        b_all = st.button(
            "Hapus Semuanya", use_container_width=True,
            help="Semua metadata akan dihapus.",
            key="preset_all",
        )
    return b_pii, b_meta, b_all


# ============================================================
# STICKY FOOTER
# ============================================================
def render_sticky_footer(selected_count, total_count):
    st.markdown('<div class="sticky-footer-wrap"><div class="sticky-footer-inner">',
                unsafe_allow_html=True)
    st.markdown(f"""
<div class="sticky-footer-info">
    <b>{selected_count}</b> dari <b>{total_count}</b> metadata akan dihapus
</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        triggered = st.button(
            "Bersihkan File Sekarang",
            type="primary",
            use_container_width=True,
            disabled=(selected_count == 0),
            key="clean_now_btn",
        )

    st.markdown('</div></div>', unsafe_allow_html=True)
    return triggered


# ============================================================
# CONFIRM DIALOG
# ============================================================
def build_confirm_dialog(file_name, keys):
    @st.dialog("Konfirmasi Penghapusan")
    def _dialog():
        safe_name = str(file_name).replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(f"""
<div class="dialog-file-info">
    <div class="lbl">File Target</div>
    <div class="val">📄 {safe_name}</div>
</div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
<div class="dialog-warning">
    <b>{len(keys)}</b> metadata akan dihapus secara permanen.
    Tindakan ini tidak dapat dibatalkan.
</div>
        """, unsafe_allow_html=True)

        with st.expander(f"Lihat {len(keys)} metadata yang akan dihapus"):
            for k in keys:
                st.caption(f"• {k}")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="small")
        with c1:
            if st.button("Batal", use_container_width=True, key="dialog_cancel"):
                st.session_state.confirmed = False
                st.rerun()
        with c2:
            if st.button("Ya, Lanjutkan", use_container_width=True,
                         type="primary", key="dialog_confirm"):
                st.session_state.confirmed = True
                st.rerun()

    return _dialog


# ============================================================
# SUCCESS SCREEN
# ============================================================
def render_success_screen(output_bytes, output_name, original_kb, new_kb,
                           removed_count, total_count, mime,
                           before_meta, after_meta):
    check_svg = render_icon("check", size=46, stroke_width=3.2, color="#FFFFFF")
    st.markdown(f"""
<div class="success-wrap">
    <div class="success-circle">{check_svg}</div>
    <div class="success-title">Metadata Berhasil Dihapus!</div>
    <p class="success-sub">File Anda siap diunduh dalam kondisi bersih.</p>
</div>
    """, unsafe_allow_html=True)

    diff = original_kb - new_kb
    pct = (diff / original_kb * 100) if original_kb > 0 else 0

    st.markdown(f"""
<div class="compare-row">
    <div class="compare-item">
        <div class="lbl">Sebelum</div>
        <div class="val">{original_kb:.1f} KB</div>
    </div>
    <div class="compare-arrow">→</div>
    <div class="compare-item after">
        <div class="lbl">Sesudah</div>
        <div class="val">{new_kb:.1f} KB</div>
        <div class="diff">−{diff:.1f} KB ({pct:.1f}%)</div>
    </div>
    <div class="compare-divider"></div>
    <div class="compare-item compare-count">
        <div class="lbl">Metadata Dihapus</div>
        <div class="val">{removed_count}<span class="slash"> / {total_count}</span></div>
    </div>
</div>
    """, unsafe_allow_html=True)

    with st.expander("Lihat perbandingan metadata (sebelum & sesudah)"):
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.markdown("##### Sebelum")
            for k in before_meta.keys():
                st.caption(f"• {k}")
        with c2:
            st.markdown("##### Sesudah")
            if after_meta:
                for k in after_meta.keys():
                    st.caption(f"• {k}")
            else:
                st.caption("_(Kosong — semua metadata berhasil dihapus)_")

    st.download_button(
        label="Download File Bersih",
        data=output_bytes,
        file_name=output_name,
        mime=mime,
        use_container_width=True,
        key="download_final",
    )


# ============================================================
# LOADER
# ============================================================
def render_loader(title="Menganalisis metadata", sub="Mohon tunggu sebentar"):
    st.markdown(f"""
<div class="loader-wrap fade-in">
    <div class="radar">
        <div class="radar-ping"></div>
    </div>
    <p class="loader-title">{title}<span class="loader-dots"></span></p>
    <p class="loader-sub">{sub}</p>
    <div class="skeleton-bar"></div>
</div>
    """, unsafe_allow_html=True)


def render_processing_state(step_label="Memproses file"):
    st.markdown(f"""
<div class="loader-wrap fade-in">
    <div class="radar">
        <div class="radar-ping"></div>
    </div>
    <p class="loader-title">{step_label}<span class="loader-dots"></span></p>
    <p class="loader-sub">Menghapus metadata dari file Anda</p>
    <div class="skeleton-bar"></div>
</div>
    """, unsafe_allow_html=True)


# ============================================================
# ERROR CARDS
# ============================================================
def render_error_card(error_kind, message, file_name=None, hint=None):
    titles = {
        "unsupported": "Format Tidak Didukung",
        "processing":  "Gagal Memproses File",
        "unknown":     "Terjadi Kesalahan",
    }
    hints = {
        "unsupported": "Coba periksa kembali ekstensi file, atau konversi ke format yang didukung "
                       "(PDF, JPG, PNG, WebP, DOCX, XLSX, PPTX, MP3).",
        "processing":  "Pastikan file tidak dalam kondisi rusak, terenkripsi, atau dipassword. "
                       "Beberapa file dari sumber tidak resmi juga bisa memiliki struktur yang tidak biasa.",
        "unknown":     "Jika masalah berlanjut, coba restart aplikasi atau laporkan file ke developer.",
    }
    title = titles.get(error_kind, "Terjadi Kesalahan")
    hint_text = hint or hints.get(error_kind, "")

    icon = render_icon("alert-triangle", size=24, stroke_width=2.2)
    file_html = f'<span class="state-file">📄 {file_name}</span>' if file_name else ""

    st.markdown(f"""
<div class="state-card error">
    <div class="state-icon">{icon}</div>
    <div class="state-body">
        <div class="state-title">{title}</div>
        <div class="state-message">{message}</div>
        {file_html}
        <div class="state-hint" style="margin-top:12px;">💡 {hint_text}</div>
    </div>
</div>
    """, unsafe_allow_html=True)


def render_already_clean_card(file_name):
    icon = render_icon("check-circle-2", size=24, stroke_width=2.2)
    st.markdown(f"""
<div class="state-card info">
    <div class="state-icon">{icon}</div>
    <div class="state-body">
        <div class="state-title">File Sudah Bersih</div>
        <div class="state-message">
            Tidak ada metadata yang terdeteksi di file ini.
            File Anda aman untuk dibagikan.
        </div>
        <span class="state-file">📄 {file_name}</span>
    </div>
</div>
    """, unsafe_allow_html=True)


# ============================================================
# BATCH — FILE CARD
# ============================================================
def render_batch_file_card(file_name, size_kb, status, meta_count=0):
    status_map = {
        "ok":          ("SIAP",          "check-circle"),
        "clean":       ("SUDAH BERSIH",  "check"),
        "error":       ("GAGAL",         "alert-triangle"),
        "unsupported": ("TIDAK DIDUKUNG","x"),
    }
    label, icon_name = status_map.get(status, ("—", "info"))
    icon_svg = render_icon(icon_name, size=18, stroke_width=2.4)

    meta_text = (
        f"{meta_count} metadata terdeteksi"
        if meta_count > 0
        else "Tidak ada metadata"
    )

    st.markdown(f"""
<div class="file-card">
    <div class="file-icon">{icon_svg}</div>
    <div class="file-body">
        <div class="file-name">{file_name}</div>
        <div class="file-meta">{size_kb:.1f} KB · {meta_text}</div>
    </div>
    <span class="file-status {status}">{label}</span>
</div>
    """, unsafe_allow_html=True)


# ============================================================
# BATCH — METRICS
# ============================================================
def render_batch_summary(stats):
    cards = [
        {"accent": "accent-brand",  "icon": "layers",
         "value": stats["total_files"], "label": "Total File",
         "sub": f"{stats['ok_files']} terbaca sukses"},
        {"accent": "accent-tier1",  "icon": "alert-triangle",
         "value": stats["files_with_meta"], "label": "File Ber-Metadata",
         "sub": f"{stats['total_meta']} metadata total"},
        {"accent": "accent-tier3",  "icon": "check-circle",
         "value": stats["files_clean"], "label": "Sudah Bersih",
         "sub": "Tanpa metadata"},
        {"accent": "accent-tier2",  "icon": "alert-circle",
         "value": stats["error_files"] + stats["unsupported_files"],
         "label": "Gagal / Skip",
         "sub": f"{stats['error_files']} error · {stats['unsupported_files']} unsupported"},
    ]

    cols = st.columns(4, gap="medium")
    for col, card in zip(cols, cards):
        with col:
            svg = render_icon(card["icon"], size=17, stroke_width=2.4)
            st.markdown(f"""
<div class="metric-card {card['accent']}">
    <div class="metric-icon">{svg}</div>
    <div>
        <div class="metric-value">{card['value']}</div>
        <div class="metric-label">{card['label']}</div>
        <div class="metric-sub">{card['sub']}</div>
    </div>
</div>
            """, unsafe_allow_html=True)


# ============================================================
# BATCH — PROGRESS (simple)
# ============================================================
def render_batch_progress(current, total, current_name, label="Memproses"):
    pct = int((current / total) * 100) if total > 0 else 0
    st.markdown(f"""
<div class="progress-wrap">
    <div class="progress-label">
        <span>{label} file {current} / {total} ({pct}%)</span>
        <span class="filename">{current_name}</span>
    </div>
</div>
    """, unsafe_allow_html=True)
    st.progress(current / total if total else 0)


# ============================================================
# BATCH — PROGRESS PANEL (dengan ETA + log)
# ============================================================
def render_progress_panel(progress, label="Memproses", show_log=True):
    """Panel progress lengkap dengan ETA, log real-time, dan pills."""
    pct = progress.pct
    current = progress.current_index + 1
    total = progress.total_files
    eta_str = humanize_duration(progress.eta) if progress.processed > 0 else "menghitung…"
    elapsed_str = humanize_duration(progress.elapsed)

    # Bagian 1: header + bar
    st.markdown(f"""
<div class="progress-panel">
    <div class="progress-header">
        <div class="progress-header-left">
            <div class="progress-current-file">
                <span class="spinner"></span>
                {label} <b>{progress.current_name or '…'}</b>
            </div>
            <div class="progress-counter">
                File {current} dari {total} · {pct}% · 
                Elapsed: {elapsed_str}
            </div>
        </div>
        <div class="progress-header-right">
            <div class="progress-eta-label">Estimasi Selesai</div>
            <div class="progress-eta">{eta_str}</div>
        </div>
    </div>
    <div class="progress-bar-wrap">
        <div class="progress-bar-fill" style="width:{pct}%;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Bagian 2: pills
    st.markdown(f"""
    <div class="progress-pills">
        <span class="progress-pill removed">
            {progress.total_removed} metadata dihapus
        </span>
        <span class="progress-pill ok">
            {progress.files_done} sukses
        </span>
        <span class="progress-pill error">
            {progress.files_failed} gagal
        </span>
        <span class="progress-pill skip">
            {progress.files_skipped} skip
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Bagian 3: log
    if show_log:
        st.markdown('<div class="progress-log">', unsafe_allow_html=True)
        if not progress.log:
            st.markdown('<div class="log-empty">Menunggu hasil file pertama…</div>',
                        unsafe_allow_html=True)
        else:
            for entry in reversed(progress.log[-20:]):
                if entry.status == "ok":
                    icon = render_icon("check-circle", size=15, stroke_width=2.4)
                    css_cls = "ok"
                elif entry.status == "error":
                    icon = render_icon("alert-triangle", size=15, stroke_width=2.4)
                    css_cls = "error"
                else:
                    icon = render_icon("info", size=15, stroke_width=2.4)
                    css_cls = "skip"

                meta_text = f"{entry.removed_count} md · {humanize_duration(entry.duration)}"

                st.markdown(f"""
<div class="log-entry {css_cls}">
    <span class="log-icon">{icon}</span>
    <span class="log-name">{entry.name}</span>
    <span class="log-meta">{meta_text}</span>
</div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# BATCH — ZIP SUMMARY
# ============================================================
def render_zip_summary(final_stats):
    icon = render_icon("download", size=26, stroke_width=2.2)

    diff = final_stats["original_size_kb"] - final_stats["new_size_kb"]
    pct = (diff / final_stats["original_size_kb"] * 100) if final_stats["original_size_kb"] > 0 else 0

    st.markdown(f"""
<div class="zip-summary">
    <div class="zip-icon">{icon}</div>
    <div class="zip-title">Semua File Siap Diunduh</div>
    <p class="zip-sub">File bersih dikemas dalam satu file ZIP.</p>
    <div class="zip-stats">
        <div class="zip-stat">
            <div class="lbl">Berhasil</div>
            <div class="val">{final_stats['success_count']}</div>
        </div>
        <div class="zip-stat">
            <div class="lbl">Metadata Dihapus</div>
            <div class="val">{final_stats['total_removed']}</div>
        </div>
        <div class="zip-stat">
            <div class="lbl">Ukuran Akhir</div>
            <div class="val">{final_stats['new_size_kb']:.1f} KB</div>
        </div>
        <div class="zip-stat">
            <div class="lbl">Hemat</div>
            <div class="val">−{pct:.1f}%</div>
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)


# ============================================================
# WEBHOOK STATUS
# ============================================================
def render_webhook_status(webhook_url, is_valid, error_msg=None):
    if not webhook_url:
        cls = "empty"
        text = "Webhook tidak diaktifkan"
    elif is_valid:
        cls = "valid"
        try:
            from webhook import mask_url
            text = f"Terhubung: {mask_url(webhook_url)}"
        except Exception:
            text = "Webhook aktif"
    else:
        cls = "invalid"
        text = error_msg or "URL tidak valid"

    st.markdown(f"""
<div class="webhook-status {cls}">
    <span class="dot"></span>
    <span>{text}</span>
</div>
    """, unsafe_allow_html=True)


# ============================================================
# PER-FILE CONFIG PANEL
# ============================================================
def render_file_config_panel(file_name, config, tier_info, key_prefix="cfg"):
    pattern_keys = list(PATTERN_OPTIONS.keys())
    pattern_labels = [PATTERN_OPTIONS[k] for k in pattern_keys]

    try:
        current_idx = pattern_keys.index(config.get("pattern", "suffix"))
    except ValueError:
        current_idx = 0

    selected_label = st.radio(
        "Pola penamaan",
        options=pattern_labels,
        index=current_idx,
        horizontal=True,
        key=f"{key_prefix}_pattern_{file_name}",
        label_visibility="collapsed",
    )
    selected_pattern = pattern_keys[pattern_labels.index(selected_label)]

    if selected_pattern != config.get("pattern"):
        config["pattern"] = selected_pattern
        if selected_pattern == "custom" and not config.get("custom_base"):
            config["custom_base"] = Path(file_name).stem

    custom_error = None
    if selected_pattern == "custom":
        default_base = config.get("custom_base") or Path(file_name).stem
        new_base = st.text_input(
            "Nama dasar (tanpa ekstensi)",
            value=default_base,
            key=f"{key_prefix}_base_{file_name}",
            placeholder="contoh: laporan_keuangan",
        )
        is_valid, err = validate_base_name(new_base)
        if is_valid:
            config["custom_base"] = new_base
        else:
            custom_error = err

    preview_name = generate_output_name(file_name, config)
    icon_svg = render_icon("file-text", size=14, stroke_width=2.2)

    st.markdown(f"""
<div class="output-preview">
    <span class="preview-icon">{icon_svg}</span>
    <span class="preview-label">Output</span>
    <span class="preview-value">{preview_name}</span>
</div>
    """, unsafe_allow_html=True)

    if custom_error:
        st.markdown(f"""
<div class="config-warning">
    <span>⚠</span>
    <span>{custom_error}</span>
</div>
        """, unsafe_allow_html=True)

    t1 = tier_info.get("tier1_on", 0)
    t2 = tier_info.get("tier2_on", 0)
    t3 = tier_info.get("tier3_on", 0)
    tt1 = tier_info.get("tier1_total", 0)
    tt2 = tier_info.get("tier2_total", 0)
    tt3 = tier_info.get("tier3_total", 0)

    def pill_class(on, total, tier):
        if total == 0:
            return "off"
        if on == 0:
            return "off"
        return {1: "on", 2: "on2", 3: "on3"}[tier]

    st.markdown(f"""
<div style="margin-top:14px;">
    <div class="config-panel-title">Metadata yang akan dihapus</div>
    <div class="tier-mini-summary">
        <span class="tier-mini-pill {pill_class(t1, tt1, 1)}">
            Tier 1 · {t1}/{tt1}
        </span>
        <span class="tier-mini-pill {pill_class(t2, tt2, 2)}">
            Tier 2 · {t2}/{tt2}
        </span>
        <span class="tier-mini-pill {pill_class(t3, tt3, 3)}">
            Tier 3 · {t3}/{tt3}
        </span>
    </div>
</div>
    """, unsafe_allow_html=True)

    config["is_default"] = (
        config.get("pattern") == "suffix"
        and (config.get("custom_base") or Path(file_name).stem) == Path(file_name).stem
    )

    return config


# ============================================================
# APPLY PATTERN TO ALL
# ============================================================
def render_apply_all_row(file_names):
    keys = list(PATTERN_OPTIONS.keys())
    labels = [PATTERN_OPTIONS[k] for k in keys]

    c1, c2 = st.columns([5, 2], vertical_alignment="bottom", gap="small")
    with c1:
        st.markdown(f"""
<div class="apply-all-row">
    <span class="apply-label">Ingin seragam? Terapkan satu pola ke semua {len(file_names)} file sekaligus.</span>
</div>
        """, unsafe_allow_html=True)
    with c2:
        selected_label = st.selectbox(
            "Pola massal",
            options=labels,
            index=0,
            key="bulk_pattern_select",
            label_visibility="collapsed",
        )
        apply_clicked = st.button(
            "Terapkan ke Semua",
            use_container_width=True,
            key="apply_all_pattern",
        )

    if apply_clicked:
        return keys[labels.index(selected_label)]
    return None

# ============================================================
# CLEAR FILE BUTTON — reset uploader
# ============================================================
def render_clear_file_button():
    """
    Tombol untuk menghapus file yang diupload (reset uploader).
    Bekerja dengan meng-increment uploader_version di session_state,
    yang mengubah key file_uploader → Streamlit remount komponen dengan state fresh.
    Mengembalikan True jika tombol diklik.
    """
    c1, c2, c3 = st.columns([1, 1, 4])
    with c1:
        if st.button("✕  Hapus File", use_container_width=True,
                     key="clear_uploaded_file_btn",
                     help="Batalkan file yang diupload dan pilih ulang"):
            return True
    return False