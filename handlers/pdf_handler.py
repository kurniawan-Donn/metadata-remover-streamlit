"""
PDF handler menggunakan pikepdf.
"""
import io
import pikepdf


def read_metadata(file_bytes):
    """
    Baca metadata dari PDF.
    Returns: (meta_dict, doc)
    """
    doc = pikepdf.open(io.BytesIO(file_bytes))
    meta = {}
    if doc.docinfo:
        for key in doc.docinfo.keys():
            meta[str(key)] = str(doc.docinfo[key])
    return meta, doc


def remove_metadata(file_bytes, selected_fields, remove_all=False):
    """
    Hapus metadata dari PDF.
    selected_fields: list key Info dictionary (contoh: '/Title')
    remove_all: hapus semua /Info dan /Metadata (XMP)
    Returns: bytes
    """
    doc = pikepdf.open(io.BytesIO(file_bytes))

    if remove_all:
        if '/Info' in doc.trailer:
            del doc.trailer['/Info']
        if '/Metadata' in doc.Root:
            del doc.Root['/Metadata']
    else:
        if '/Info' in doc.trailer:
            info = doc.trailer['/Info']
            for key in selected_fields:
                if key in info:
                    del info[key]
            if len(info) == 0:
                del doc.trailer['/Info']

    output = io.BytesIO()
    doc.save(output)
    return output.getvalue()