"""
Python wrapper untuk komponen drag-and-drop file list (SortableJS).
"""
from pathlib import Path
import streamlit.components.v1 as components


_component_path = Path(__file__).parent / "sortable_component"

_sortable_list = components.declare_component(
    "sortable_file_list",
    path=str(_component_path),
)


def render_sortable_file_list(files_data, theme="light", key=None):
    """
    Render daftar file yang bisa di-drag untuk mengubah urutan.

    Args:
        files_data : list[dict] dengan struktur:
                     [{'id': 'f0', 'name': 'a.pdf', 'size_kb': 12.4}, ...]
        theme      : 'light' | 'dark'
        key        : unique key Streamlit — ganti key untuk force re-mount.

    Returns:
        dict | None — {'order': ['f2', 'f0', 'f1']} setelah user drag, atau None.
    """
    result = _sortable_list(
        items=files_data,
        theme=theme,
        key=key,
        default=None,
    )
    return result