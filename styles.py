"""
Semua CSS untuk Metadata Remover.
Dibagi per blok (1-31) sesuai tahap pengembangan.

Cara pakai:
    from styles import inject_custom_css, THEME_BOOT_SCRIPT
    inject_custom_css()
"""

CUSTOM_CSS = """
<style>
/* ============================================================
   1. IMPORT GOOGLE FONT — Plus Jakarta Sans
   ============================================================ */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');


/* ============================================================
   2. CSS VARIABLES (ROOT)
   ============================================================ */
:root {
    --bg-main: #F8FAFC;
    --bg-card: #FFFFFF;
    --bg-subtle: #F1F5F9;
    --bg-glass: rgba(255, 255, 255, 0.72);

    --text-primary: #0F172A;
    --text-secondary: #64748B;
    --text-tertiary: #94A3B8;

    --tier1: #EF4444;
    --tier1-soft: #FEF2F2;
    --tier2: #F59E0B;
    --tier2-soft: #FFFBEB;
    --tier3: #10B981;
    --tier3-soft: #ECFDF5;

    --brand-primary: #4F46E5;
    --brand-primary-dark: #4338CA;
    --brand-primary-soft: #EEF2FF;

    --border-soft: #E2E8F0;
    --border-medium: #CBD5E1;

    --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.04);
    --shadow-md: 0 4px 12px -2px rgba(15, 23, 42, 0.08);
    --shadow-lg: 0 10px 24px -4px rgba(15, 23, 42, 0.10);
    --shadow-xl: 0 20px 40px -8px rgba(15, 23, 42, 0.14);

    --radius-sm: 10px;
    --radius-md: 14px;
    --radius-lg: 18px;
    --radius-xl: 22px;

    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', Roboto, sans-serif;
    --font-mono: 'SF Mono', 'Consolas', 'Monaco', 'Courier New', monospace;
}


/* ============================================================
   3. SEMBUNYIKAN ELEMEN DEFAULT STREAMLIT
   ============================================================ */
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; display: none !important; }
header[data-testid="stHeader"] {
    background: transparent !important;
    visibility: hidden !important;
    height: 0 !important;
}
[data-testid="stToolbar"] { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }


/* ============================================================
   4. FONDASI BODY & APP
   ============================================================ */
html, body {
    font-family: var(--font-sans) !important;
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.stApp {
    background-color: var(--bg-main) !important;
    font-family: var(--font-sans) !important;
    color: var(--text-primary) !important;
}

.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 180px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1280px !important;
    margin: 0 auto !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stVerticalBlock"] > [style*="flex-direction: column"] {
    gap: 0.75rem;
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-sans) !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.3px;
}

p, span, div, label { font-family: var(--font-sans); }


/* ============================================================
   5. SCROLLBAR
   ============================================================ */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--border-medium);
    border-radius: 999px;
    border: 2px solid var(--bg-main);
}
::-webkit-scrollbar-thumb:hover { background: var(--text-tertiary); }


/* ============================================================
   6. TRANSISI GLOBAL
   ============================================================ */
* {
    transition-property: background-color, border-color, box-shadow, transform;
    transition-duration: 0.2s;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}


/* ============================================================
   7. HEADER / HERO
   ============================================================ */
.hero {
    padding: 8px 0 4px 0;
    margin-bottom: 8px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
    color: var(--brand-primary);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 6px 14px;
    border-radius: 999px;
    margin-bottom: 20px;
    border: 1px solid rgba(79, 70, 229, 0.15);
}
.hero-badge .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--brand-primary);
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15); }
    50%      { box-shadow: 0 0 0 6px rgba(79, 70, 229, 0.05); }
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -1.8px;
    color: var(--text-primary);
    margin: 0 0 14px 0;
}
.hero-title .accent {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 55%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 16px;
    line-height: 1.65;
    color: var(--text-secondary);
    max-width: 640px;
    margin: 0 0 8px 0;
    font-weight: 400;
}
.hero-subtitle strong { color: var(--text-primary); font-weight: 600; }

.hero-meta {
    display: flex;
    gap: 20px;
    margin-top: 18px;
    flex-wrap: wrap;
}
.hero-meta-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12.5px;
    color: var(--text-tertiary);
    font-weight: 500;
}
.hero-meta-item svg {
    width: 15px;
    height: 15px;
    color: var(--tier3);
}

/* ============================================================
   8. UPLOAD ZONE
   ============================================================ */
[data-testid="stFileUploader"] {
    background: transparent !important;
    width: 100%;
}

[data-testid="stFileUploader"] > section,
[data-testid="stFileUploadDropzone"] {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border-medium) !important;
    border-radius: var(--radius-xl) !important;
    padding: 44px 28px 40px 28px !important;
    transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: var(--shadow-sm) !important;
    position: relative;
    min-height: 220px;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 12px !important;
    cursor: pointer;
}

[data-testid="stFileUploader"] > section:hover,
[data-testid="stFileUploadDropzone"]:hover,
[data-testid="stFileUploadDropzone"]:focus-within {
    border-color: var(--brand-primary) !important;
    background: linear-gradient(135deg, #FAFBFF 0%, #F5F3FF 100%) !important;
    box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.08),
                0 14px 32px -10px rgba(79, 70, 229, 0.28) !important;
    transform: translateY(-2px);
}

/* Sembunyikan teks bawaan Streamlit */
[data-testid="stFileUploadDropzone"] svg,
[data-testid="stFileUploadDropzone"] > div > span,
[data-testid="stFileUploadDropzone"] > div > small,
[data-testid="stFileUploader"] section > span,
[data-testid="stFileUploader"] section small {
    display: none !important;
}

/* Ikon upload — pakai properti terpisah agar tidak reset */
[data-testid="stFileUploader"] > section::before,
[data-testid="stFileUploadDropzone"]::before {
    content: "";
    display: block;
    width: 68px;
    height: 68px;
    border-radius: 20px;
    background-color: #EEF2FF;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234F46E5' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242'/><path d='M12 12v9'/><path d='m16 16-4-4-4 4'/></svg>");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 34px 34px;
    box-shadow: 0 8px 20px -8px rgba(79, 70, 229, 0.4);
    margin-bottom: 4px;
    transition: transform 0.25s ease;
}
[data-testid="stFileUploader"] > section:hover::before,
[data-testid="stFileUploadDropzone"]:hover::before {
    transform: scale(1.06) translateY(-2px);
}

/* Teks utama */
[data-testid="stFileUploader"] > section::after,
[data-testid="stFileUploadDropzone"]::after {
    content: "Tarik & Lepas File di Sini";
    display: block;
    font-family: var(--font-sans);
    font-size: 17px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.3px;
    text-align: center;
}

/* Sub-label */
[data-testid="stFileUploader"] > section > div:last-child::before,
[data-testid="stFileUploadDropzone"] > div:last-child::before {
    content: "atau klik tombol di bawah untuk memilih file";
    display: block;
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 400;
    text-align: center;
    margin-top: 2px;
}

/* Tombol Browse */
[data-testid="stFileUploader"] button,
[data-testid="stFileUploadDropzone"] button {
    background: var(--brand-primary) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: -0.1px;
    box-shadow: 0 4px 12px -2px rgba(79, 70, 229, 0.4) !important;
    transition: all 0.2s ease !important;
    margin-top: 6px !important;
    font-family: var(--font-sans) !important;
}
[data-testid="stFileUploader"] button:hover,
[data-testid="stFileUploadDropzone"] button:hover {
    background: var(--brand-primary-dark) !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 20px -4px rgba(79, 70, 229, 0.55) !important;
}

/* File yang sudah diupload — tampilkan rapi */
[data-testid="stFileUploaderFile"] {
    background: var(--bg-subtle) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin-top: 10px !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}

/* Tombol X (delete) bawaan Streamlit — pastikan terlihat & kontras */
[data-testid="stFileUploaderDeleteBtn"],
[data-testid="stFileUploaderFileDeleteButton"] {
    background: transparent !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 8px !important;
    color: var(--tier1) !important;
    padding: 4px 8px !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    opacity: 1 !important;
    visibility: visible !important;
}
[data-testid="stFileUploaderDeleteBtn"]:hover,
[data-testid="stFileUploaderFileDeleteButton"]:hover {
    background: var(--tier1-soft) !important;
    border-color: var(--tier1) !important;
}
[data-testid="stFileUploaderDeleteBtn"] svg,
[data-testid="stFileUploaderFileDeleteButton"] svg {
    color: var(--tier1) !important;
    display: block !important;
    width: 14px !important;
    height: 14px !important;
}

[data-testid="stFileUploader"] small {
    color: var(--text-tertiary) !important;
    font-size: 11px !important;
}

/* Dark mode */
body[data-theme="dark"] [data-testid="stFileUploader"] > section,
body[data-theme="dark"] [data-testid="stFileUploadDropzone"] {
    background: #1E293B !important;
    border-color: #334155 !important;
}
body[data-theme="dark"] [data-testid="stFileUploader"] > section:hover,
body[data-theme="dark"] [data-testid="stFileUploadDropzone"]:hover {
    background: linear-gradient(135deg, #1E293B, #312E81) !important;
    border-color: #6366F1 !important;
}
body[data-theme="dark"] [data-testid="stFileUploader"] > section::before,
body[data-theme="dark"] [data-testid="stFileUploadDropzone"]::before {
    background-color: rgba(99, 102, 241, 0.2);
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23A5B4FC' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242'/><path d='M12 12v9'/><path d='m16 16-4-4-4 4'/></svg>");
    box-shadow: 0 8px 20px -8px rgba(99, 102, 241, 0.5);
}
body[data-theme="dark"] [data-testid="stFileUploader"] > section::after,
body[data-theme="dark"] [data-testid="stFileUploadDropzone"]::after { color: #F8FAFC !important; }
body[data-theme="dark"] [data-testid="stFileUploader"] > section > div:last-child::before,
body[data-theme="dark"] [data-testid="stFileUploadDropzone"] > div:last-child::before { color: #94A3B8; }
body[data-theme="dark"] [data-testid="stFileUploaderFile"] {
    background: #1E293B !important;
    border-color: #334155 !important;
}

/* ============================================================
   9. METRIC CARDS
   ============================================================ */
.metric-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 24px 22px 22px 22px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08),
                0 2px 4px -1px rgba(0, 0, 0, 0.04);
    position: relative;
    overflow: hidden;
    transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
    border-top: 4px solid var(--accent);
    min-height: 148px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    cursor: default;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px -6px rgba(0, 0, 0, 0.12),
                0 4px 8px -2px rgba(0, 0, 0, 0.06);
}
.metric-card.accent-brand  { --accent: var(--brand-primary); }
.metric-card.accent-tier1  { --accent: var(--tier1); }
.metric-card.accent-tier2  { --accent: var(--tier2); }
.metric-card.accent-tier3  { --accent: var(--tier3); }

/* Ikon di pojok kanan atas — diperbesar & diberi padding */
.metric-card .metric-icon {
    position: absolute;
    top: 20px;
    right: 20px;
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: color-mix(in srgb, var(--accent) 14%, transparent);
    color: var(--accent);
    transition: transform 0.25s ease;
    padding: 8px;
}
.metric-card:hover .metric-icon {
    transform: scale(1.08) rotate(-3deg);
}
.metric-card .metric-icon svg {
    width: 22px;
    height: 22px;
    stroke-width: 2.4;
}

.metric-card .metric-value {
    font-family: var(--font-sans);
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -1.5px;
    color: var(--text-primary);
    margin: 0 0 8px 0;
    display: flex;
    align-items: baseline;
    gap: 6px;
}
.metric-card .metric-value .unit {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-tertiary);
    letter-spacing: 0;
}
.metric-card .metric-label {
    font-size: 12.5px;
    color: var(--text-secondary);
    font-weight: 600;
    letter-spacing: -0.1px;
    margin: 0;
    line-height: 1.3;
}
.metric-card .metric-sub {
    font-size: 11px;
    color: var(--text-tertiary);
    font-weight: 500;
    margin-top: 3px;
    letter-spacing: 0;
}

/* ============================================================
   10. SEGMENTED CONTROL (Tab Tier)
   ============================================================ */
div[role="radiogroup"] {
    display: inline-flex !important;
    flex-direction: row !important;
    flex-wrap: wrap !important;
    gap: 6px !important;
    background: #F1F5F9 !important;
    padding: 6px !important;
    border-radius: 999px !important;
    border: 1px solid var(--border-soft) !important;
    margin: 4px 0 24px 0 !important;
    box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.03);
}

div[role="radiogroup"] > label {
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    background: transparent !important;
    border-radius: 999px !important;
    padding: 10px 18px !important;   /* tab lebih lega */
    margin: 0 !important;
    cursor: pointer !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid transparent !important;
    position: relative;
    min-height: 40px;
}

div[role="radiogroup"] > label > div:first-child { display: none !important; }

div[role="radiogroup"] > label p {
    font-family: var(--font-sans) !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    margin: 0 !important;
    letter-spacing: -0.1px;
    white-space: nowrap;
}

div[role="radiogroup"] > label:hover {
    background: rgba(255, 255, 255, 0.75) !important;
}
div[role="radiogroup"] > label:hover p {
    color: var(--text-primary) !important;
}

/* Tab aktif */
div[role="radiogroup"] > label:has(input:checked),
div[role="radiogroup"] > label[data-checked="true"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(79, 70, 229, 0.35) !important;
    box-shadow: 0 4px 12px -2px rgba(79, 70, 229, 0.2),
                0 1px 2px rgba(15, 23, 42, 0.06) !important;
}
div[role="radiogroup"] > label:has(input:checked) p,
div[role="radiogroup"] > label[data-checked="true"] p {
    color: var(--brand-primary) !important;
    font-weight: 700 !important;
}

/* Dark mode */
body[data-theme="dark"] div[role="radiogroup"] {
    background: #1E293B !important;
    border-color: #334155 !important;
}
body[data-theme="dark"] div[role="radiogroup"] > label p {
    color: #94A3B8 !important;
}
body[data-theme="dark"] div[role="radiogroup"] > label:hover {
    background: rgba(51, 65, 85, 0.6) !important;
}
body[data-theme="dark"] div[role="radiogroup"] > label:hover p {
    color: #F8FAFC !important;
}
body[data-theme="dark"] div[role="radiogroup"] > label:has(input:checked),
body[data-theme="dark"] div[role="radiogroup"] > label[data-checked="true"] {
    background: #334155 !important;
    border-color: #6366F1 !important;
    box-shadow: 0 4px 12px -2px rgba(99, 102, 241, 0.35),
                0 1px 2px rgba(0, 0, 0, 0.4) !important;
}
body[data-theme="dark"] div[role="radiogroup"] > label:has(input:checked) p {
    color: #A5B4FC !important;
}

/* ============================================================
   11. METADATA CARD
   ============================================================ */
.metadata-card {
    background: #F1F5F9;
    border-radius: 12px;
    border-left: 4px solid var(--accent);
    padding: 16px 20px;
    transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    min-height: 88px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 8px;
}
.metadata-card:hover {
    background: #FFFFFF;
    box-shadow: 0 6px 16px -4px rgba(15, 23, 42, 0.10),
                0 2px 4px rgba(15, 23, 42, 0.04);
    transform: translateX(3px);
}
.metadata-card.tier1 { --accent: var(--tier1); }
.metadata-card.tier2 { --accent: var(--tier2); }
.metadata-card.tier3 { --accent: var(--tier3); }

.metadata-card .meta-key {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.2px;
    line-height: 1.3;
}
.metadata-card .meta-value {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 12.5px;
    color: #334155;
    background: rgba(255, 255, 255, 0.85);
    padding: 5px 10px;
    border-radius: 6px;
    word-break: break-word;
    max-width: 100%;
    line-height: 1.5;
    border: 1px solid rgba(226, 232, 240, 0.7);
}
.metadata-card:hover .meta-value { background: var(--bg-subtle); }

.metadata-card .meta-badge {
    display: inline-flex;
    align-items: center;
    font-size: 9.5px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 999px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.metadata-card .meta-badge.tier1 { background: #FEE2E2; color: #B91C1C; }
.metadata-card .meta-badge.tier2 { background: #FEF3C7; color: #B45309; }
.metadata-card .meta-badge.tier3 { background: #D1FAE5; color: #047857; }

.metadata-card .info-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #CBD5E1;
    color: #FFFFFF;
    font-size: 10px;
    font-weight: 800;
    font-family: var(--font-sans);
    cursor: help;
    position: relative;
    margin-left: auto;
    transition: background 0.15s ease;
    flex-shrink: 0;
}
.metadata-card .info-icon:hover { background: var(--accent); }

.metadata-card .info-icon::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: calc(100% + 10px);
    right: 0;
    background: #0F172A;
    color: #F8FAFC;
    padding: 10px 13px;
    border-radius: 10px;
    font-size: 11.5px;
    font-weight: 500;
    font-family: var(--font-sans);
    line-height: 1.5;
    white-space: normal;
    width: 250px;
    text-align: left;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: opacity 0.18s ease, transform 0.18s ease;
    transform: translateY(4px);
    box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.45);
    z-index: 9999;
}
.metadata-card .info-icon::before {
    content: "";
    position: absolute;
    bottom: calc(100% + 4px);
    right: 5px;
    width: 8px;
    height: 8px;
    background: #0F172A;
    transform: rotate(45deg);
    opacity: 0;
    transition: opacity 0.18s ease;
    z-index: 9999;
}
.metadata-card .info-icon:hover::after,
.metadata-card .info-icon:hover::before {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

/* Toggle di kolom kanan metadata card — di tengah vertikal */
div[class*="st-key-toggle_"] [data-testid="stToggle"],
div[class*="st-key-btoggle_"] [data-testid="stToggle"] {
    display: flex;
    align-items: center;
    justify-content: center;
    padding-top: 0;
    min-height: 88px;
}
div[class*="st-key-toggle_"] [data-testid="stToggle"] label p,
div[class*="st-key-btoggle_"] [data-testid="stToggle"] label p {
    display: none !important;
}
div[class*="st-key-toggle_"] [data-testid="stToggle"] label > div:first-child,
div[class*="st-key-btoggle_"] [data-testid="stToggle"] label > div:first-child {
    margin: 0 !important;
}

/* Dark mode */
body[data-theme="dark"] .metadata-card { background: #1E293B; }
body[data-theme="dark"] .metadata-card:hover {
    background: #334155;
    box-shadow: 0 8px 20px -6px rgba(0, 0, 0, 0.5),
                0 3px 6px -2px rgba(0, 0, 0, 0.3);
}
body[data-theme="dark"] .metadata-card .meta-key { color: #F8FAFC; }
body[data-theme="dark"] .metadata-card .meta-value {
    background: #0F172A;
    color: #CBD5E1;
    border-color: #334155;
}
body[data-theme="dark"] .metadata-card .info-icon { background: #475569; color: #E2E8F0; }

/* ============================================================
   12. PRESET BUTTONS
   ============================================================ */
.preset-row {
    display: flex;
    gap: 10px;
    margin: 4px 0 8px 0;
    flex-wrap: wrap;
}

div.stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 999px !important;
    padding: 11px 22px !important;
    font-family: var(--font-sans) !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    letter-spacing: -0.1px;
    transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
    width: 100% !important;
}
div.stButton > button[kind="secondary"]:hover {
    transform: translateY(-1px);
    border-color: var(--brand-primary) !important;
    color: var(--brand-primary) !important;
    background: var(--brand-primary-soft) !important;
    box-shadow: 0 6px 16px -4px rgba(79, 70, 229, 0.28) !important;
}

/* Dark mode — fix kontras warna teks */
body[data-theme="dark"] div.stButton > button[kind="secondary"] {
    background: #1E293B !important;
    color: #F8FAFC !important;      /* putih terang */
    border-color: #334155 !important;
}
body[data-theme="dark"] div.stButton > button[kind="secondary"] p {
    color: #F8FAFC !important;      /* pastikan teks di dalam <p> juga putih */
}
body[data-theme="dark"] div.stButton > button[kind="secondary"]:hover {
    background: rgba(79, 70, 229, 0.22) !important;
    border-color: #6366F1 !important;
    color: #A5B4FC !important;
}
body[data-theme="dark"] div.stButton > button[kind="secondary"]:hover p {
    color: #A5B4FC !important;
}

/* Dark mode untuk tombol di dalam expander (Reset / Reset Semua) */
body[data-theme="dark"] div[data-testid="stExpander"] div.stButton > button[kind="secondary"] {
    background: #334155 !important;
    color: #F8FAFC !important;
    border-color: #475569 !important;
}
body[data-theme="dark"] div[data-testid="stExpander"] div.stButton > button[kind="secondary"] p {
    color: #F8FAFC !important;
}

/* ============================================================
   13. STICKY FOOTER
   ============================================================ */
.sticky-footer-wrap {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 998;
    background: linear-gradient(
        180deg,
        rgba(248, 250, 252, 0) 0%,
        rgba(248, 250, 252, 0.85) 30%,
        rgba(248, 250, 252, 0.98) 60%,
        #F8FAFC 100%
    );
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    padding: 30px 0 22px 0;
    pointer-events: none;
}
.sticky-footer-inner {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 32px;
    pointer-events: auto;
}
.sticky-footer-info {
    text-align: center;
    margin-bottom: 10px;
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 500;
}
.sticky-footer-info b {
    color: var(--text-primary);
    font-weight: 700;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #EF4444 0%, #DC2626 50%, #B91C1C 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 24px !important;
    font-family: var(--font-sans) !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    letter-spacing: -0.2px;
    box-shadow:
        0 8px 24px -6px rgba(239, 68, 68, 0.55),
        0 0 0 1px rgba(239, 68, 68, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transition: all 0.24s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100% !important;
    position: relative;
    overflow: hidden;
}
div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow:
        0 14px 34px -8px rgba(239, 68, 68, 0.7),
        0 0 0 1px rgba(239, 68, 68, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    background: linear-gradient(135deg, #F05252 0%, #E11D48 50%, #BE123C 100%) !important;
}
div.stButton > button[kind="primary"]:active { transform: translateY(0); }
div.stButton > button[kind="primary"]:disabled {
    background: #E2E8F0 !important;
    color: #94A3B8 !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
}


/* ============================================================
   14. DIALOG / MODAL — Command Palette Style
   ============================================================ */
div[role="dialog"] {
    background: #0F172A !important;
    border: 1px solid #1E293B !important;
    border-radius: 18px !important;
    box-shadow: 0 30px 80px -12px rgba(0, 0, 0, 0.7) !important;
    padding: 4px !important;
}
div[role="dialog"] * { font-family: var(--font-sans) !important; }
div[role="dialog"] h2,
div[role="dialog"] h3 {
    color: #F8FAFC !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
    margin-bottom: 4px !important;
}
div[role="dialog"] p,
div[role="dialog"] .stCaption p,
div[role="dialog"] [data-testid="stCaptionContainer"] p {
    color: #94A3B8 !important;
}
div[role="dialog"] hr {
    border-color: #1E293B !important;
    margin: 14px 0 !important;
}
div[role="dialog"] [data-testid="stExpander"] {
    background: #111C33 !important;
    border: 1px solid #1E293B !important;
    border-radius: 12px !important;
}
div[role="dialog"] [data-testid="stExpander"] summary p {
    color: #CBD5E1 !important;
    font-weight: 600 !important;
}
div[role="dialog"] div.stButton > button[kind="secondary"] {
    background: #1E293B !important;
    color: #E2E8F0 !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}
div[role="dialog"] div.stButton > button[kind="secondary"]:hover {
    background: #334155 !important;
    color: #FFFFFF !important;
    border-color: #475569 !important;
}
div[role="dialog"] div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #EF4444, #B91C1C) !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
    font-size: 14px !important;
}

.dialog-file-info {
    background: #111C33;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 14px 16px;
    margin: 12px 0;
}
.dialog-file-info .lbl {
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #64748B;
    font-weight: 700;
    margin-bottom: 6px;
}
.dialog-file-info .val {
    font-size: 15px;
    color: #F8FAFC;
    font-weight: 600;
    word-break: break-all;
}
.dialog-warning {
    background: rgba(239, 68, 68, 0.08);
    border-left: 3px solid #EF4444;
    border-radius: 8px;
    padding: 12px 14px;
    margin: 14px 0 6px 0;
    color: #FCA5A5 !important;
    font-size: 13px;
    font-weight: 500;
    line-height: 1.5;
}


/* ============================================================
   15. LAYAR SUKSES
   ============================================================ */
.success-wrap {
    text-align: center;
    padding: 20px 0 8px 0;
    animation: success-pop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.success-circle {
    width: 88px;
    height: 88px;
    margin: 0 auto 18px auto;
    border-radius: 50%;
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow:
        0 0 0 8px rgba(16, 185, 129, 0.12),
        0 0 0 20px rgba(16, 185, 129, 0.05),
        0 16px 32px -8px rgba(16, 185, 129, 0.45);
    animation: pulse-ring 2.4s ease-in-out infinite;
    position: relative;
}
.success-circle svg {
    width: 46px;
    height: 46px;
    color: #FFFFFF;
    stroke-width: 3.2;
}
.success-title {
    font-family: var(--font-sans);
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.6px;
    margin: 0 0 6px 0;
}
.success-sub {
    font-size: 13.5px;
    color: var(--text-secondary);
    margin: 0;
    font-weight: 500;
}
@keyframes success-pop {
    0%   { transform: scale(0.85); opacity: 0; }
    60%  { transform: scale(1.05); opacity: 1; }
    100% { transform: scale(1);    opacity: 1; }
}
@keyframes pulse-ring {
    0%, 100% {
        box-shadow:
            0 0 0 8px rgba(16, 185, 129, 0.12),
            0 0 0 20px rgba(16, 185, 129, 0.05),
            0 16px 32px -8px rgba(16, 185, 129, 0.45);
    }
    50% {
        box-shadow:
            0 0 0 12px rgba(16, 185, 129, 0.08),
            0 0 0 26px rgba(16, 185, 129, 0.03),
            0 16px 32px -8px rgba(16, 185, 129, 0.55);
    }
}


/* ============================================================
   16. PERBANDINGAN UKURAN
   ============================================================ */
.compare-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 26px;
    padding: 24px 20px;
    background: #FFFFFF;
    border: 1px solid var(--border-soft);
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.06);
    margin: 8px 0 16px 0;
    flex-wrap: wrap;
}
.compare-item {
    text-align: center;
    min-width: 110px;
}
.compare-item .lbl {
    font-size: 11px;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 700;
    margin-bottom: 6px;
}
.compare-item .val {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.6px;
    line-height: 1.1;
}
.compare-item.after .val { color: var(--tier3); }
.compare-item .diff {
    font-size: 11.5px;
    color: var(--tier3);
    font-weight: 700;
    margin-top: 4px;
    background: var(--tier3-soft);
    padding: 2px 8px;
    border-radius: 999px;
    display: inline-block;
}
.compare-arrow {
    font-size: 22px;
    color: var(--text-tertiary);
    font-weight: 300;
}
.compare-divider {
    width: 1px;
    height: 52px;
    background: var(--border-soft);
}
.compare-count .val {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
}
.compare-count .val .slash {
    color: var(--text-tertiary);
    font-weight: 600;
    font-size: 16px;
}


/* ============================================================
   17. DOWNLOAD BUTTON
   ============================================================ */
div.stDownloadButton > button {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 50%, #3730A3 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 24px !important;
    font-family: var(--font-sans) !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    letter-spacing: -0.2px;
    box-shadow:
        0 8px 24px -6px rgba(79, 70, 229, 0.55),
        0 0 0 1px rgba(79, 70, 229, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.18) !important;
    transition: all 0.24s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100% !important;
    margin-top: 4px;
}
div.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 14px 34px -8px rgba(79, 70, 229, 0.7),
        0 0 0 1px rgba(79, 70, 229, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.22) !important;
}


/* ============================================================
   18. ICON ALIGNMENT
   ============================================================ */
.icon-inline {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    vertical-align: middle;
}
.icon-inline svg { flex-shrink: 0; }

.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 12px 0;
}
.section-header svg {
    color: var(--text-secondary);
    opacity: 0.85;
}
.section-header h2 {
    font-family: var(--font-sans);
    font-size: 17px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.3px;
    margin: 0;
}
.hero-badge svg { width: 13px; height: 13px; stroke-width: 2.4; }
.hero-meta-item svg {
    width: 15px;
    height: 15px;
    color: var(--tier3);
    flex-shrink: 0;
}


/* ============================================================
   19. BUTTON ICON INJECTION
   ============================================================ */
div.st-key-clean_now_btn button p::before {
    content: '';
    display: inline-block;
    width: 18px;
    height: 18px;
    margin-right: 8px;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='m7 21-4.3-4.3c-1-1-1-2.5 0-3.4l9.6-9.6c1-1 2.5-1 3.4 0l5.6 5.6c1 1 1 2.5 0 3.4L13 21'/><path d='M22 21H7'/><path d='m5 11 9 9'/></svg>");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    vertical-align: -3px;
}
div.st-key-download_final button p::before,
div.st-key-download_zip button p::before {
    content: '';
    display: inline-block;
    width: 18px;
    height: 18px;
    margin-right: 8px;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/><polyline points='7 10 12 15 17 10'/><line x1='12' x2='12' y1='15' y2='3'/></svg>");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    vertical-align: -3px;
}
div.st-key-preset_pii button p::before {
    content: '';
    display: inline-block;
    width: 15px;
    height: 15px;
    margin-right: 7px;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23EF4444' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z'/><path d='m9 12 2 2 4-4'/></svg>");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    vertical-align: -2px;
}
div.st-key-preset_meta button p::before {
    content: '';
    display: inline-block;
    width: 15px;
    height: 15px;
    margin-right: 7px;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23F59E0B' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4'/><path d='M14 13.12c0 2.38 0 6.38-1 8.88'/><path d='M17.29 21.02c.12-.6.43-2.3.5-3.02'/><path d='M2 12a10 10 0 0 1 18-6'/><path d='M2 16h.01'/><path d='M21.8 16c.2-2 .131-5.354 0-6'/><path d='M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2'/><path d='M8.65 22c.21-.66.45-1.32.57-2'/><path d='M9 6.8a6 6 0 0 1 9 5.2v2'/></svg>");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    vertical-align: -2px;
}
div.st-key-preset_all button p::before {
    content: '';
    display: inline-block;
    width: 15px;
    height: 15px;
    margin-right: 7px;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2310B981' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z'/></svg>");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    vertical-align: -2px;
}


/* ============================================================
   20. TIER SELECTOR — Icon per-opsi radio
   ============================================================ */
div[role="radiogroup"] > label:nth-of-type(1) p::before {
    content: '';
    display: inline-block;
    width: 13px; height: 13px;
    margin-right: 6px;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23EF4444' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><path d='m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3'/><path d='M12 9v4'/><path d='M12 17h.01'/></svg>");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    vertical-align: -2px;
}
div[role="radiogroup"] > label:nth-of-type(2) p::before {
    content: '';
    display: inline-block;
    width: 13px; height: 13px;
    margin-right: 6px;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23F59E0B' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><line x1='12' x2='12' y1='8' y2='12'/><line x1='12' x2='12.01' y1='16' y2='16'/></svg>");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    vertical-align: -2px;
}
div[role="radiogroup"] > label:nth-of-type(3) p::before {
    content: '';
    display: inline-block;
    width: 13px; height: 13px;
    margin-right: 6px;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2310B981' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><path d='M22 11.08V12a10 10 0 1 1-5.93-9.14'/><polyline points='22 4 12 14.01 9 11.01'/></svg>");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    vertical-align: -2px;
}


/* ============================================================
   21. MICRO-INTERACTIONS
   ============================================================ */
.metric-card,
.metadata-card,
.compare-row,
.file-info-bar,
button,
.stDownloadButton button,
[role="dialog"] {
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                background-color 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                border-color 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                color 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 32px -8px rgba(15, 23, 42, 0.14),
                0 6px 12px -4px rgba(15, 23, 42, 0.08) !important;
}
.metadata-card:hover {
    transform: translateX(3px) translateY(-1px);
    box-shadow: 0 8px 20px -6px rgba(15, 23, 42, 0.12),
                0 3px 6px -2px rgba(15, 23, 42, 0.06) !important;
}

div.stButton > button:active,
div.stDownloadButton > button:active {
    transform: translateY(0) scale(0.98) !important;
    transition-duration: 0.08s !important;
}


/* ============================================================
   22. TOGGLE ANIMATION
   ============================================================ */
[data-testid="stToggle"] label > div:first-child {
    transition: background-color 0.25s cubic-bezier(0.4, 0, 0.2, 1),
                box-shadow 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
[data-testid="stToggle"] label > div:first-child > div {
    transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1),
                background-color 0.25s ease !important;
}
[data-testid="stToggle"] label > div:first-child[data-checked="true"],
[data-testid="stToggle"] input:checked ~ div:first-child {
    background-color: var(--brand-primary) !important;
}
[data-testid="stToggle"] input:focus-visible ~ div:first-child {
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.25) !important;
}


/* ============================================================
   23. CUSTOM LOADING (Radar Scan)
   ============================================================ */
.loader-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 56px 24px 44px 24px;
    background: var(--bg-card);
    border-radius: 20px;
    border: 1px solid var(--border-soft);
    box-shadow: 0 8px 24px -10px rgba(15, 23, 42, 0.10);
    margin: 12px 0 20px 0;
    animation: fade-slide-in 0.4s ease;
}
.radar {
    width: 92px;
    height: 92px;
    border-radius: 50%;
    position: relative;
    background: radial-gradient(circle at center,
                rgba(79, 70, 229, 0.06) 0%,
                rgba(79, 70, 229, 0.02) 55%,
                transparent 70%);
    margin-bottom: 22px;
}
.radar::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 2px solid rgba(79, 70, 229, 0.15);
}
.radar::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: conic-gradient(
        from 0deg,
        transparent 0deg,
        rgba(79, 70, 229, 0.0) 240deg,
        rgba(79, 70, 229, 0.35) 330deg,
        rgba(79, 70, 229, 0.6) 360deg
    );
    animation: radar-sweep 1.4s linear infinite;
    -webkit-mask: radial-gradient(circle, transparent 12%, black 14%);
    mask: radial-gradient(circle, transparent 12%, black 14%);
}
.radar .radar-ping {
    position: absolute;
    top: 50%; left: 50%;
    width: 8px; height: 8px;
    background: var(--brand-primary);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.25);
    animation: radar-ping 1.4s ease-out infinite;
}
@keyframes radar-sweep {
    0%   { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
@keyframes radar-ping {
    0%   { transform: translate(-50%, -50%) scale(1);   opacity: 1; }
    100% { transform: translate(-50%, -50%) scale(2.8); opacity: 0; }
}
.loader-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.3px;
    margin: 0 0 4px 0;
}
.loader-sub {
    font-size: 12.5px;
    color: var(--text-secondary);
    font-weight: 500;
    margin: 0;
}
.loader-dots::after {
    content: "";
    animation: dots 1.4s steps(4, end) infinite;
}
@keyframes dots {
    0%   { content: ""; }
    25%  { content: "."; }
    50%  { content: ".."; }
    75%  { content: "..."; }
    100% { content: ""; }
}
.skeleton-bar {
    width: 200px;
    height: 4px;
    border-radius: 999px;
    background: #E2E8F0;
    overflow: hidden;
    margin-top: 18px;
    position: relative;
}
.skeleton-bar::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(79, 70, 229, 0.55) 50%,
        transparent 100%
    );
    animation: skeleton-move 1.5s ease-in-out infinite;
}
@keyframes skeleton-move {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
@keyframes fade-slide-in {
    0%   { opacity: 0; transform: translateY(8px); }
    100% { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fade-slide-in 0.4s cubic-bezier(0.4, 0, 0.2, 1); }


/* ============================================================
   24. TOOLTIP ELEGAN
   ============================================================ */
[data-baseweb="tooltip"] {
    background: #0F172A !important;
    color: #F8FAFC !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    font-family: var(--font-sans) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.4),
                0 4px 8px -2px rgba(0, 0, 0, 0.2) !important;
    border: 1px solid #1E293B !important;
    max-width: 260px;
    line-height: 1.5;
    animation: tooltip-in 0.18s ease;
}
[data-baseweb="tooltip"] * {
    color: #F8FAFC !important;
    background: transparent !important;
}
@keyframes tooltip-in {
    0%   { opacity: 0; transform: translateY(4px); }
    100% { opacity: 1; transform: translateY(0); }
}


/* ============================================================
   25. RESPONSIVE — MEDIA QUERIES
   ============================================================ */
@media (max-width: 1024px) {
    .block-container {
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }
    .hero-title { font-size: 38px; letter-spacing: -1.2px; }
    .metric-card .metric-value { font-size: 2rem; }
}

@media (max-width: 768px) {
    .block-container {
        padding-top: 1.25rem !important;
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
        padding-bottom: 200px !important;
    }
    .hero-title { font-size: 30px !important; letter-spacing: -0.8px; }
    .hero-subtitle { font-size: 14px; }
    .hero-meta { gap: 12px; margin-top: 14px; }
    .hero-meta-item { font-size: 11.5px; }
    .hero-badge { font-size: 10px; padding: 5px 11px; }

    .metric-card {
        min-height: auto;
        padding: 16px 18px;
        margin-bottom: 10px;
    }
    .metric-card .metric-value { font-size: 1.85rem; letter-spacing: -0.8px; }
    .metric-card .metric-icon { width: 26px; height: 26px; top: 14px; right: 14px; }
    .metric-card .metric-icon svg { width: 14px; height: 14px; }

    .metadata-card { padding: 12px 14px; min-height: auto; }
    .metadata-card .meta-key { font-size: 13px; }
    .metadata-card .meta-value { font-size: 11.5px; padding: 3px 8px; }

    div[role="radiogroup"] {
        display: flex !important;
        width: 100% !important;
        flex-wrap: wrap !important;
        justify-content: center;
    }
    div[role="radiogroup"] > label {
        padding: 8px 14px !important;
        font-size: 12.5px !important;
        flex: 1 1 auto;
        justify-content: center;
    }
    div[role="radiogroup"] > label p { font-size: 12px !important; }

    .sticky-footer-inner { padding: 0 14px; }
    .sticky-footer-info { font-size: 12px; }
    div.stButton > button[kind="primary"] {
        font-size: 14.5px !important;
        padding: 13px 18px !important;
    }

    .compare-row { gap: 14px; padding: 18px 14px; }
    .compare-item .val { font-size: 18px; }
    .compare-divider { display: none; }
    .compare-arrow { font-size: 18px; }

    div[role="dialog"] { margin: 12px !important; }
    div[role="dialog"] h2 { font-size: 16px !important; }

    .radar { width: 70px; height: 70px; }
    .loader-title { font-size: 14px; }
}

@media (max-width: 480px) {
    .hero-title { font-size: 26px !important; }
    .hero-subtitle { font-size: 13px; }
    .metric-card .metric-value { font-size: 1.65rem; }
    div[role="radiogroup"] > label { padding: 7px 10px !important; }
    div[role="radiogroup"] > label p { font-size: 11px !important; }
    .metadata-card .meta-key { font-size: 12px; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* ============================================================
   26. FILE INFO BAR
   ============================================================ */
.file-info-bar {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-lg);
    padding: 18px 24px;
    margin-bottom: 24px;
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 24px;
    align-items: center;
    box-shadow: var(--shadow-sm);
}

.file-info-item {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    gap: 4px;
    min-width: 0;
}

.file-info-item .label {
    font-size: 10px;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 700;
    margin: 0;
    line-height: 1;
}
.file-info-item .value {
    font-size: 14px;
    color: var(--text-primary);
    font-weight: 600;
    margin: 0;
    line-height: 1.3;
    word-break: break-word;
}

/* Responsif: di mobile jadi kolom tunggal */
@media (max-width: 768px) {
    .file-info-bar {
        grid-template-columns: 1fr;
        gap: 14px;
        padding: 16px 18px;
    }
}

/* ============================================================
   27. STATE CARDS (Error / Warning / Info)
   ============================================================ */
.state-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 26px 26px 22px 26px;
    box-shadow: 0 8px 24px -10px rgba(15, 23, 42, 0.10);
    border: 1px solid var(--border-soft);
    display: flex;
    gap: 18px;
    align-items: flex-start;
    margin: 12px 0 20px 0;
    animation: fade-slide-in 0.35s ease;
}
.state-card.error  { border-left: 4px solid var(--tier1); background: linear-gradient(90deg, #FEF2F2 0%, #FFFFFF 40%); }
.state-card.warning { border-left: 4px solid var(--tier2); background: linear-gradient(90deg, #FFFBEB 0%, #FFFFFF 40%); }
.state-card.info   { border-left: 4px solid var(--tier3); background: linear-gradient(90deg, #ECFDF5 0%, #FFFFFF 40%); }

.state-card .state-icon {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.state-card.error .state-icon   { background: #FEE2E2; color: #B91C1C; }
.state-card.warning .state-icon { background: #FEF3C7; color: #B45309; }
.state-card.info .state-icon    { background: #D1FAE5; color: #047857; }

.state-card .state-body { flex: 1; min-width: 0; }
.state-card .state-title {
    font-size: 15.5px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 6px 0;
    letter-spacing: -0.3px;
}
.state-card .state-message {
    font-size: 13.5px;
    color: var(--text-secondary);
    margin: 0 0 10px 0;
    line-height: 1.55;
}
.state-card .state-hint {
    font-size: 12.5px;
    color: var(--text-tertiary);
    background: rgba(15, 23, 42, 0.03);
    padding: 8px 12px;
    border-radius: 8px;
    line-height: 1.5;
    border-left: 2px solid var(--border-medium);
}
.state-card .state-file {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--text-secondary);
    background: rgba(255, 255, 255, 0.7);
    padding: 3px 9px;
    border-radius: 6px;
    margin-top: 4px;
    border: 1px solid var(--border-soft);
}


/* ============================================================
   28. DARK MODE
   ============================================================ */
body[data-theme="dark"] {
    --bg-main: #0F172A;
    --bg-card: #1E293B;
    --bg-subtle: #334155;
    --bg-glass: rgba(30, 41, 59, 0.72);
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-tertiary: #64748B;
    --border-soft: #334155;
    --border-medium: #475569;
    --brand-primary-soft: rgba(79, 70, 229, 0.15);
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 12px -2px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 10px 24px -4px rgba(0, 0, 0, 0.5);
    --shadow-xl: 0 20px 40px -8px rgba(0, 0, 0, 0.6);
}

body[data-theme="dark"],
body[data-theme="dark"] html,
body[data-theme="dark"] .stApp,
body[data-theme="dark"] [data-testid="stAppViewContainer"] {
    background-color: #0F172A !important;
    color: #F8FAFC !important;
}
body[data-theme="dark"] h1,
body[data-theme="dark"] h2,
body[data-theme="dark"] h3,
body[data-theme="dark"] h4,
body[data-theme="dark"] h5,
body[data-theme="dark"] h6 { color: #F8FAFC !important; }

body[data-theme="dark"] .hero-badge {
    background: linear-gradient(135deg, rgba(79,70,229,0.18), rgba(124,58,237,0.15));
    color: #A5B4FC;
    border-color: rgba(79, 70, 229, 0.3);
}
body[data-theme="dark"] .hero-badge .dot { background: #A5B4FC; }
body[data-theme="dark"] .hero-subtitle { color: #94A3B8; }
body[data-theme="dark"] .hero-subtitle strong { color: #F8FAFC; }
body[data-theme="dark"] .hero-meta-item { color: #64748B; }

body[data-theme="dark"] [data-testid="stFileUploader"] > section,
body[data-theme="dark"] [data-testid="stFileUploadDropzone"] {
    background: #1E293B !important;
    border-color: #334155 !important;
}
body[data-theme="dark"] [data-testid="stFileUploader"] > section:hover,
body[data-theme="dark"] [data-testid="stFileUploadDropzone"]:hover {
    background: linear-gradient(135deg, #1E293B, #312E81) !important;
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15),
                0 14px 32px -10px rgba(79, 70, 229, 0.5) !important;
}
body[data-theme="dark"] [data-testid="stFileUploader"] > section::after,
body[data-theme="dark"] [data-testid="stFileUploadDropzone"]::after { color: #F8FAFC !important; }
body[data-theme="dark"] [data-testid="stFileUploader"] > section > div:last-child::before,
body[data-theme="dark"] [data-testid="stFileUploadDropzone"] > div:last-child::before { color: #94A3B8; }

body[data-theme="dark"] .file-info-bar { background: #1E293B; border-color: #334155; }
body[data-theme="dark"] .file-info-item .label { color: #64748B; }
body[data-theme="dark"] .file-info-item .value { color: #F8FAFC; }

body[data-theme="dark"] .metric-card {
    background: #1E293B;
    border-color: #334155;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4),
                0 2px 4px -1px rgba(0, 0, 0, 0.3);
}
body[data-theme="dark"] .metric-card:hover {
    box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.6),
                0 6px 12px -4px rgba(0, 0, 0, 0.4);
}
body[data-theme="dark"] .metric-card .metric-value { color: #F8FAFC; }
body[data-theme="dark"] .metric-card .metric-label { color: #94A3B8; }
body[data-theme="dark"] .metric-card .metric-sub   { color: #64748B; }

body[data-theme="dark"] .section-header h2 { color: #F8FAFC; }
body[data-theme="dark"] .section-header svg { color: #94A3B8; }

body[data-theme="dark"] div.stButton > button[kind="secondary"] {
    background: #1E293B !important;
    color: #F8FAFC !important;
    border-color: #334155 !important;
}
body[data-theme="dark"] div.stButton > button[kind="secondary"]:hover {
    background: rgba(79, 70, 229, 0.18) !important;
    border-color: #6366F1 !important;
    color: #A5B4FC !important;
}

body[data-theme="dark"] div[role="radiogroup"] {
    background: #1E293B !important;
    border-color: #334155 !important;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.3);
}
body[data-theme="dark"] div[role="radiogroup"] > label p { color: #94A3B8 !important; }
body[data-theme="dark"] div[role="radiogroup"] > label:hover {
    background: rgba(51, 65, 85, 0.5) !important;
}
body[data-theme="dark"] div[role="radiogroup"] > label:hover p { color: #F8FAFC !important; }
body[data-theme="dark"] div[role="radiogroup"] > label:has(input:checked),
body[data-theme="dark"] div[role="radiogroup"] > label[data-checked="true"] {
    background: #334155 !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35) !important;
}
body[data-theme="dark"] div[role="radiogroup"] > label:has(input:checked) p { color: #F8FAFC !important; }

body[data-theme="dark"] .metadata-card { background: #1E293B; }
body[data-theme="dark"] .metadata-card:hover {
    background: #334155;
    box-shadow: 0 8px 20px -6px rgba(0, 0, 0, 0.5),
                0 3px 6px -2px rgba(0, 0, 0, 0.3);
}
body[data-theme="dark"] .metadata-card .meta-key { color: #F8FAFC; }
body[data-theme="dark"] .metadata-card .meta-value {
    background: #0F172A;
    color: #CBD5E1;
    border-color: #334155;
}
body[data-theme="dark"] .metadata-card:hover .meta-value { background: #0F172A; }
body[data-theme="dark"] .metadata-card .info-icon { background: #475569; color: #E2E8F0; }

body[data-theme="dark"] .badge-danger,
body[data-theme="dark"] .meta-badge.tier1 { background: rgba(239, 68, 68, 0.2); color: #FCA5A5; }
body[data-theme="dark"] .badge-warning,
body[data-theme="dark"] .meta-badge.tier2 { background: rgba(245, 158, 11, 0.2); color: #FCD34D; }
body[data-theme="dark"] .badge-safe,
body[data-theme="dark"] .meta-badge.tier3 { background: rgba(16, 185, 129, 0.2); color: #6EE7B7; }

body[data-theme="dark"] .empty-tier {
    background: #1E293B;
    color: #64748B;
    border-color: #334155;
}

body[data-theme="dark"] .sticky-footer-wrap {
    background: linear-gradient(
        180deg,
        rgba(15, 23, 42, 0) 0%,
        rgba(15, 23, 42, 0.85) 30%,
        rgba(15, 23, 42, 0.98) 60%,
        #0F172A 100%
    );
    border-top-color: rgba(51, 65, 85, 0.6);
}
body[data-theme="dark"] .sticky-footer-info { color: #94A3B8; }
body[data-theme="dark"] .sticky-footer-info b { color: #F8FAFC; }

body[data-theme="dark"] .compare-row {
    background: #1E293B;
    border-color: #334155;
}
body[data-theme="dark"] .compare-item .lbl { color: #64748B; }
body[data-theme="dark"] .compare-item .val { color: #F8FAFC; }
body[data-theme="dark"] .compare-divider { background: #334155; }
body[data-theme="dark"] .compare-arrow { color: #64748B; }
body[data-theme="dark"] .success-title { color: #F8FAFC; }
body[data-theme="dark"] .success-sub { color: #94A3B8; }

body[data-theme="dark"] .state-card { background: #1E293B; border-color: #334155; }
body[data-theme="dark"] .state-card.error { background: linear-gradient(90deg, rgba(239, 68, 68, 0.10) 0%, #1E293B 40%); }
body[data-theme="dark"] .state-card.warning { background: linear-gradient(90deg, rgba(245, 158, 11, 0.10) 0%, #1E293B 40%); }
body[data-theme="dark"] .state-card.info { background: linear-gradient(90deg, rgba(16, 185, 129, 0.10) 0%, #1E293B 40%); }
body[data-theme="dark"] .state-card .state-title { color: #F8FAFC; }
body[data-theme="dark"] .state-card .state-message { color: #94A3B8; }
body[data-theme="dark"] .state-card .state-hint {
    background: rgba(15, 23, 42, 0.5);
    border-left-color: #475569;
    color: #94A3B8;
}
body[data-theme="dark"] .state-card .state-file {
    background: rgba(15, 23, 42, 0.6);
    border-color: #334155;
    color: #CBD5E1;
}

body[data-theme="dark"] .loader-wrap { background: #1E293B; border-color: #334155; }
body[data-theme="dark"] .loader-title { color: #F8FAFC; }
body[data-theme="dark"] .loader-sub { color: #94A3B8; }
body[data-theme="dark"] .skeleton-bar { background: #334155; }

body[data-theme="dark"] ::-webkit-scrollbar-thumb {
    background: #475569;
    border-color: #0F172A;
}
body[data-theme="dark"] ::-webkit-scrollbar-thumb:hover { background: #64748B; }

body[data-theme="dark"] [data-testid="stFileUploader"] small { color: #64748B !important; }
body[data-theme="dark"] [data-testid="stFileUploaderFile"] {
    background: #1E293B !important;
    border-color: #334155 !important;
}

body[data-theme="dark"] [data-testid="stToggle"] label > div:first-child {
    background-color: #475569 !important;
}
body[data-theme="dark"] [data-testid="stToggle"] label > div:first-child[data-checked="true"],
body[data-theme="dark"] [data-testid="stToggle"] input:checked ~ div:first-child {
    background-color: #6366F1 !important;
}

body[data-theme="dark"] div.stDownloadButton > button {
    box-shadow: 0 8px 24px -6px rgba(79, 70, 229, 0.7),
                0 0 0 1px rgba(79, 70, 229, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
}
body[data-theme="dark"] div.stButton > button[kind="primary"] {
    box-shadow: 0 8px 24px -6px rgba(239, 68, 68, 0.65),
                0 0 0 1px rgba(239, 68, 68, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
}
body[data-theme="dark"] div[role="dialog"] {
    background: #0B1220 !important;
    border-color: #1E293B !important;
}


/* ============================================================
   29. BATCH MODE — File List, Progress
   ============================================================ */
.file-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}
.file-card:hover {
    background: var(--bg-subtle);
    transform: translateX(2px);
    box-shadow: var(--shadow-md);
}
.file-card .file-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--brand-primary-soft);
    color: var(--brand-primary);
    flex-shrink: 0;
}
.file-card .file-body { flex: 1; min-width: 0; }
.file-card .file-name {
    font-size: 13.5px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 2px 0;
    letter-spacing: -0.2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.file-card .file-meta {
    font-size: 11.5px;
    color: var(--text-tertiary);
    font-weight: 500;
}
.file-card .file-status {
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.file-status.ok          { background: #D1FAE5; color: #047857; }
.file-status.clean       { background: #DBEAFE; color: #1E40AF; }
.file-status.error       { background: #FEE2E2; color: #B91C1C; }
.file-status.unsupported { background: #F3E8FF; color: #6B21A8; }

.progress-wrap {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 14px;
    padding: 18px 20px;
    margin: 12px 0 18px 0;
    box-shadow: var(--shadow-sm);
}
.progress-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 10px;
}
.progress-label .filename {
    font-family: var(--font-mono);
    font-size: 11.5px;
    color: var(--text-tertiary);
    max-width: 55%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.batch-file-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 10px;
    background: var(--bg-subtle);
    margin-bottom: 6px;
    border-left: 4px solid var(--border-soft);
}
.batch-file-row.selected { border-left-color: var(--brand-primary); }

.zip-summary {
    background: linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%);
    border: 1px solid rgba(79, 70, 229, 0.2);
    border-radius: 16px;
    padding: 22px 26px;
    margin: 14px 0 20px 0;
    text-align: center;
}
.zip-summary .zip-icon {
    width: 56px; height: 56px;
    margin: 0 auto 14px;
    border-radius: 14px;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--brand-primary);
    box-shadow: 0 6px 16px -4px rgba(79, 70, 229, 0.3);
}
.zip-summary .zip-title {
    font-size: 17px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.4px;
    margin: 0 0 6px 0;
}
.zip-summary .zip-sub {
    font-size: 13px;
    color: var(--text-secondary);
    margin: 0;
}
.zip-summary .zip-stats {
    display: flex;
    justify-content: center;
    gap: 26px;
    margin-top: 16px;
    flex-wrap: wrap;
}
.zip-summary .zip-stat .lbl {
    font-size: 10.5px;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 700;
    margin-bottom: 3px;
}
.zip-summary .zip-stat .val {
    font-size: 20px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}

body[data-theme="dark"] .file-card { background: #1E293B; border-color: #334155; }
body[data-theme="dark"] .file-card:hover { background: #334155; }
body[data-theme="dark"] .file-card .file-icon {
    background: rgba(79, 70, 229, 0.18);
    color: #A5B4FC;
}
body[data-theme="dark"] .file-card .file-name { color: #F8FAFC; }
body[data-theme="dark"] .file-card .file-meta { color: #64748B; }
body[data-theme="dark"] .progress-wrap { background: #1E293B; border-color: #334155; }
body[data-theme="dark"] .progress-label { color: #94A3B8; }
body[data-theme="dark"] .batch-file-row { background: #334155; }
body[data-theme="dark"] .zip-summary {
    background: linear-gradient(135deg, rgba(79,70,229,0.15) 0%, rgba(124,58,237,0.10) 100%);
    border-color: rgba(99, 102, 241, 0.3);
}
body[data-theme="dark"] .zip-summary .zip-icon { background: #1E293B; color: #A5B4FC; }
body[data-theme="dark"] .zip-summary .zip-title { color: #F8FAFC; }
body[data-theme="dark"] .zip-summary .zip-sub { color: #94A3B8; }
body[data-theme="dark"] .zip-summary .zip-stat .val { color: #F8FAFC; }


/* ============================================================
   30. PER-FILE CONFIG PANEL
   ============================================================ */
.config-panel {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 14px;
    padding: 18px 20px;
    margin: 10px 0 14px 0;
    box-shadow: var(--shadow-sm);
}
.config-panel-title {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--text-tertiary);
    margin: 0 0 10px 0;
}

.custom-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 9.5px;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 999px;
    background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
    color: var(--brand-primary);
    margin-left: 8px;
    border: 1px solid rgba(79, 70, 229, 0.18);
}
body[data-theme="dark"] .custom-badge {
    background: linear-gradient(135deg, rgba(79,70,229,0.22), rgba(124,58,237,0.18));
    color: #A5B4FC;
    border-color: rgba(99, 102, 241, 0.3);
}

.output-preview {
    display: flex;
    align-items: center;
    gap: 10px;
    background: var(--bg-subtle);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    padding: 11px 14px;
    margin-top: 4px;
    font-family: var(--font-mono);
    font-size: 12.5px;
    color: var(--text-primary);
    overflow: hidden;
}
.output-preview .preview-label {
    font-family: var(--font-sans);
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: var(--text-tertiary);
    flex-shrink: 0;
}
.output-preview .preview-value {
    font-family: var(--font-mono);
    font-weight: 600;
    color: var(--text-primary);
    word-break: break-all;
    flex: 1;
    min-width: 0;
}
.output-preview .preview-icon {
    color: var(--brand-primary);
    flex-shrink: 0;
    display: flex;
    align-items: center;
}
body[data-theme="dark"] .output-preview { background: #0F172A; border-color: #334155; }
body[data-theme="dark"] .output-preview .preview-value { color: #F8FAFC; }

.config-warning {
    display: flex;
    gap: 8px;
    align-items: flex-start;
    background: #FEF3C7;
    border-left: 3px solid #F59E0B;
    padding: 9px 12px;
    border-radius: 8px;
    font-size: 12px;
    color: #92400E;
    margin-top: 8px;
    line-height: 1.5;
}
body[data-theme="dark"] .config-warning {
    background: rgba(245, 158, 11, 0.12);
    color: #FCD34D;
}

.tier-mini-summary {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 4px;
}
.tier-mini-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
    letter-spacing: 0.2px;
}
.tier-mini-pill.on  { background: #FEE2E2; color: #B91C1C; }
.tier-mini-pill.on2 { background: #FEF3C7; color: #B45309; }
.tier-mini-pill.on3 { background: #D1FAE5; color: #047857; }
.tier-mini-pill.off { background: #F1F5F9; color: #94A3B8; text-decoration: line-through; }

body[data-theme="dark"] .tier-mini-pill.on  { background: rgba(239,68,68,0.2);  color: #FCA5A5; }
body[data-theme="dark"] .tier-mini-pill.on2 { background: rgba(245,158,11,0.2); color: #FCD34D; }
body[data-theme="dark"] .tier-mini-pill.on3 { background: rgba(16,185,129,0.2); color: #6EE7B7; }
body[data-theme="dark"] .tier-mini-pill.off { background: #334155; color: #64748B; }

.apply-all-row {
    display: flex;
    align-items: center;
    gap: 10px;
    background: var(--brand-primary-soft);
    border-radius: 12px;
    padding: 12px 16px;
    margin: 6px 0 14px 0;
    border: 1px dashed rgba(79, 70, 229, 0.3);
    flex-wrap: wrap;
}
body[data-theme="dark"] .apply-all-row {
    background: rgba(79, 70, 229, 0.12);
    border-color: rgba(99, 102, 241, 0.4);
}
.apply-all-row .apply-label {
    font-size: 12.5px;
    font-weight: 700;
    color: var(--brand-primary);
    flex: 1;
    min-width: 200px;
}
body[data-theme="dark"] .apply-all-row .apply-label { color: #A5B4FC; }


/* ============================================================
   31. PROGRESS PANEL — ETA + Real-time Log
   ============================================================ */
.progress-panel {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 16px;
    padding: 20px 22px;
    margin: 14px 0 18px 0;
    box-shadow: var(--shadow-md);
    animation: fade-slide-in 0.35s ease;
}
.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 14px;
    flex-wrap: wrap;
}
.progress-header-left { flex: 1; min-width: 200px; }
.progress-header-right { text-align: right; min-width: 120px; }

.progress-current-file {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13.5px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.2px;
}
.progress-current-file .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid var(--border-medium);
    border-top-color: var(--brand-primary);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

.progress-counter {
    font-size: 12.5px;
    color: var(--text-secondary);
    font-weight: 600;
    margin-top: 4px;
}
.progress-eta {
    font-size: 22px;
    font-weight: 800;
    color: var(--brand-primary);
    letter-spacing: -0.6px;
    line-height: 1.1;
}
.progress-eta-label {
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--text-tertiary);
    font-weight: 700;
    margin-bottom: 4px;
}

.progress-bar-wrap {
    height: 10px;
    background: var(--bg-subtle);
    border-radius: 999px;
    overflow: hidden;
    position: relative;
    margin: 8px 0 14px 0;
}
.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #4F46E5, #7C3AED 60%, #EC4899);
    border-radius: 999px;
    transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.progress-bar-fill::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(255,255,255,0.4) 50%,
        transparent 100%
    );
    animation: shimmer-progress 1.6s infinite;
}
@keyframes shimmer-progress {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.progress-log {
    background: var(--bg-subtle);
    border-radius: 12px;
    padding: 10px 6px 6px 10px;
    max-height: 220px;
    overflow-y: auto;
    margin-top: 6px;
    border: 1px solid var(--border-soft);
}
.log-entry {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 10px;
    border-radius: 8px;
    font-size: 12.5px;
    transition: background 0.15s ease;
}
.log-entry:hover { background: rgba(255,255,255,0.6); }
body[data-theme="dark"] .log-entry:hover { background: rgba(255,255,255,0.04); }
.log-entry .log-icon {
    width: 18px;
    height: 18px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.log-entry.ok    .log-icon { color: var(--tier3); }
.log-entry.error .log-icon { color: var(--tier1); }
.log-entry.skip  .log-icon { color: var(--text-tertiary); }
.log-entry .log-name {
    flex: 1;
    font-weight: 600;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.log-entry .log-meta {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-tertiary);
    flex-shrink: 0;
}
.log-empty {
    text-align: center;
    color: var(--text-tertiary);
    font-size: 12px;
    padding: 12px 0;
    font-weight: 500;
}

.progress-pills {
    display: flex;
    gap: 8px;
    margin-top: 12px;
    flex-wrap: wrap;
}
.progress-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    font-weight: 700;
    padding: 6px 12px;
    border-radius: 999px;
    background: var(--bg-subtle);
    color: var(--text-secondary);
}
.progress-pill.ok      { background: #D1FAE5; color: #047857; }
.progress-pill.error   { background: #FEE2E2; color: #B91C1C; }
.progress-pill.skip    { background: #E2E8F0; color: #475569; }
.progress-pill.removed { background: var(--brand-primary-soft); color: var(--brand-primary); }

body[data-theme="dark"] .progress-pill.ok      { background: rgba(16,185,129,0.2); color: #6EE7B7; }
body[data-theme="dark"] .progress-pill.error   { background: rgba(239,68,68,0.2);  color: #FCA5A5; }
body[data-theme="dark"] .progress-pill.skip    { background: #334155; color: #94A3B8; }
body[data-theme="dark"] .progress-pill.removed { background: rgba(79,70,229,0.2); color: #A5B4FC; }

.webhook-status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11.5px;
    padding: 8px 10px;
    border-radius: 8px;
    background: var(--bg-subtle);
    margin-top: 8px;
    color: var(--text-secondary);
}
.webhook-status .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}
.webhook-status.valid .dot   { background: #10B981; box-shadow: 0 0 0 3px rgba(16,185,129,0.2); }
.webhook-status.invalid .dot { background: #EF4444; box-shadow: 0 0 0 3px rgba(239,68,68,0.2); }
.webhook-status.empty .dot   { background: #94A3B8; }


/* ============================================================
   32. SECTION SPACING — konsistensi antar section
   ============================================================ */
.section-header {
    margin: 32px 0 16px 0 !important;
}
.section-header h2 {
    line-height: 1.2;
}

/* Jarak antar grup komponen */
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}

/* Expander di batch — beri jarak */
div[data-testid="stExpander"] {
    margin-bottom: 8px !important;
    border-radius: 12px !important;
}

/* Kartu metrics row — beri jarak dengan section berikutnya */
div[data-testid="stHorizontalBlock"] {
    gap: 14px !important;
}

/* ============================================================
   33. STICKY HEADER WRAPPER
   ============================================================ */
div[class*="st-key-sticky_header"] {
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
    background: var(--bg-main) !important;
    padding: 12px 0 10px 0 !important;
    margin-top: -12px !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
div[class*="st-key-sticky_header"]:has(+ div) {
    border-bottom-color: var(--border-soft);
}

/* Pastikan theme toggle terlihat di light mode */
div[class*="st-key-theme_toggle_widget"] {
    display: flex !important;
    justify-content: flex-end !important;
    align-items: center !important;
}
div[class*="st-key-theme_toggle_widget"] [data-testid="stToggle"] label {
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 6px 14px !important;
    border-radius: 999px !important;
    background: #FFFFFF !important;
    border: 1px solid var(--border-soft) !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
div[class*="st-key-theme_toggle_widget"] [data-testid="stToggle"] label:hover {
    border-color: var(--brand-primary) !important;
    box-shadow: 0 4px 12px -2px rgba(79, 70, 229, 0.2) !important;
}
div[class*="st-key-theme_toggle_widget"] [data-testid="stToggle"] label p {
    display: inline !important;
    font-size: 12.5px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    white-space: nowrap;
}

body[data-theme="dark"] div[class*="st-key-theme_toggle_widget"] [data-testid="stToggle"] label {
    background: #1E293B !important;
    border-color: #334155 !important;
}
body[data-theme="dark"] div[class*="st-key-theme_toggle_widget"] [data-testid="stToggle"] label:hover {
    border-color: #6366F1 !important;
    box-shadow: 0 4px 12px -2px rgba(99, 102, 241, 0.3) !important;
}
body[data-theme="dark"] div[class*="st-key-theme_toggle_widget"] [data-testid="stToggle"] label p {
    color: #F8FAFC !important;
}

</style>
"""


THEME_BOOT_SCRIPT = """
<script>
(function() {
    try {
        const t = localStorage.getItem("metadata_remover_theme");
        if (t === "dark" || t === "light") {
            document.documentElement.setAttribute("data-theme", t);
            document.body && document.body.setAttribute("data-theme", t);
        }
    } catch(e) {}
})();
</script>
"""


def inject_custom_css():
    """Suntikkan CSS kustom ke aplikasi Streamlit."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)