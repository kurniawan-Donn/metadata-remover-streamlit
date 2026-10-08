"""
Theme manager dengan persistensi localStorage.
Menggunakan komponen HTML+JS untuk menjembatani browser ↔ Python.
"""
import streamlit as st
import streamlit.components.v1 as components


THEME_KEY = "theme"
STORAGE_KEY = "metadata_remover_theme"
DEFAULT_THEME = "light"
VALID_THEMES = ("light", "dark")


# ============================================================
# STATE
# ============================================================
def init_theme():
    """Inisialisasi tema di session_state."""
    if THEME_KEY not in st.session_state:
        st.session_state[THEME_KEY] = DEFAULT_THEME
    if "theme_loaded" not in st.session_state:
        st.session_state.theme_loaded = False


def get_theme():
    return st.session_state.get(THEME_KEY, DEFAULT_THEME)


def set_theme(value):
    if value not in VALID_THEMES:
        value = DEFAULT_THEME
    st.session_state[THEME_KEY] = value


# ============================================================
# JS BRIDGE COMPONENT (BIDIRECTIONAL)
# ============================================================
_THEME_BRIDGE_HTML = """
<div id="theme-bridge" style="display:none;"></div>
<script>
(function() {
    const STORAGE_KEY = "%(storage_key)s";
    const VALID_THEMES = ["light", "dark"];

    function sendToPython(value) {
        if (window.Streamlit && typeof window.Streamlit.setComponentValue === 'function') {
            window.Streamlit.setComponentValue(value);
        } else {
            window.parent.postMessage({
                isStreamlitMessage: true,
                type: "streamlit:setComponentValue",
                value: value
            }, "*");
        }
    }

    let saved = null;
    try {
        saved = localStorage.getItem(STORAGE_KEY);
    } catch (e) {
        saved = null;
    }

    if (saved && !VALID_THEMES.includes(saved)) {
        saved = null;
    }

    if (saved) {
        sendToPython(saved);
    } else {
        sendToPython("__none__");
    }

    window.addEventListener("message", function(event) {
        if (!event.data || typeof event.data !== "object") return;
        if (event.data.type === "streamlit:render") {
            const args = event.data.args || {};
            const newTheme = args && args.theme ? args.theme : null;
            if (newTheme && VALID_THEMES.includes(newTheme)) {
                try { localStorage.setItem(STORAGE_KEY, newTheme); } catch (e) {}
            }
        }
    });

    if (window.Streamlit && typeof window.Streamlit.setFrameHeight === 'function') {
        window.Streamlit.setFrameHeight(0);
        window.Streamlit.setComponentReady && window.Streamlit.setComponentReady();
    }
})();
</script>
"""


def theme_persistence_manager():
    """Bidirectional: baca dari localStorage, tulis ke Python."""
    html = _THEME_BRIDGE_HTML % {"storage_key": STORAGE_KEY}
    value = components.html(html, height=0, width=0)

    if value == "__none__" or value is None:
        return None
    if value in VALID_THEMES:
        return value
    return None


def sync_theme_from_storage():
    """Panggil di awal app. Sinkronkan localStorage → session_state."""
    stored = theme_persistence_manager()
    if stored and stored != st.session_state.get(THEME_KEY):
        st.session_state[THEME_KEY] = stored
        st.session_state.theme_loaded = True


def push_theme_to_storage(theme):
    """Panggil saat user toggle. Simpan ke localStorage."""
    html = _THEME_BRIDGE_HTML.replace(
        "const STORAGE_KEY",
        f"const INJECTED_THEME = '{theme}';\n    const STORAGE_KEY"
    ).replace(
        "// ---- 2. DENGARKAN PERUBAHAN dari Python ----",
        "if (INJECTED_THEME) { try { localStorage.setItem(STORAGE_KEY, INJECTED_THEME); } catch(e){} }\n"
        "// ---- 2. DENGARKAN PERUBAHAN dari Python ----"
    ) % {"storage_key": STORAGE_KEY}
    components.html(html, height=0, width=0)


# ============================================================
# APPLY
# ============================================================
def apply_theme(theme=None):
    """Set atribut data-theme pada body parent document."""
    if theme is None:
        theme = get_theme()
    components.html(
        f"""
        <script>
            (function() {{
                const doc = window.parent.document;
                doc.body.setAttribute('data-theme', '{theme}');
                doc.documentElement.setAttribute('data-theme', '{theme}');
            }})();
        </script>
        """,
        height=0, width=0,
    )


# ============================================================
# TOGGLE UI
# ============================================================
def render_theme_toggle():
    current = get_theme()
    is_dark = (current == "dark")
    icon = "🌙" if not is_dark else "☀️"
    label = "Dark" if is_dark else "Light"

    value = st.toggle(
        f"{icon} {label}",
        value=is_dark,
        key="theme_toggle_widget",
        help="Ganti Light/Dark Mode (tersimpan otomatis)",
    )

    new_theme = "dark" if value else "light"
    if new_theme != current:
        set_theme(new_theme)
        push_theme_to_storage(new_theme)
        st.rerun()

    return new_theme