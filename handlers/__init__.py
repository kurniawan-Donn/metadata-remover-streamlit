"""
Package handlers untuk Metadata Remover.
Semua modul handler punya interface standar:
    read_metadata(file_bytes) -> tuple
    remove_metadata(file_bytes, selected, remove_all) -> bytes
"""