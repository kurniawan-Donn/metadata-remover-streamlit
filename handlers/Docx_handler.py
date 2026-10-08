"""
DOCX handler — manipulasi ZIP + XML core properties.
"""
import io
import zipfile
import xml.etree.ElementTree as ET


NS_CP = 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'
NS_DC = 'http://purl.org/dc/elements/1.1/'
NS_DCTERMS = 'http://purl.org/dc/terms/'
NS_EP = 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'
NS_VT = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'

ET.register_namespace('cp', NS_CP)
ET.register_namespace('dc', NS_DC)
ET.register_namespace('dcterms', NS_DCTERMS)
ET.register_namespace('vt', NS_VT)
ET.register_namespace('', NS_EP)


CORE_TIERS = {
    'creator': 1, 'lastModifiedBy': 1, 'created': 1, 'modified': 1,
    'lastPrinted': 1, 'revision': 1, 'subject': 1, 'description': 1,
    'keywords': 1, 'category': 1, 'contentStatus': 1,
    'title': 3, 'language': 3, 'identifier': 3, 'version': 3,
}

APP_TIERS = {
    'Company': 1, 'Manager': 1, 'Application': 1, 'AppVersion': 1,
    'Template': 1, 'TotalTime': 1, 'HyperlinkBase': 1,
    'Pages': 2, 'Words': 2, 'Characters': 2, 'Lines': 2, 'Paragraphs': 2,
    'HeadingPairs': 2, 'TitlesOfParts': 2, 'SharedDoc': 2,
    'HyperlinksChanged': 2, 'LinksUpToDate': 2, 'ScaleCrop': 2,
    'DocSecurity': 2,
}

LOCALNAME_TO_LABEL = {
    'title': 'Title', 'creator': 'Author', 'subject': 'Subject',
    'description': 'Description', 'keywords': 'Keywords',
    'lastModifiedBy': 'Last Modified By', 'created': 'Created',
    'modified': 'Modified', 'category': 'Category',
    'contentStatus': 'Content Status', 'identifier': 'Identifier',
    'language': 'Language', 'version': 'Version',
}


EMPTY_CUSTOM_XML = (
    b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
    b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"/>'
)


def _localname(tag):
    return tag.split('}')[-1] if '}' in tag else tag


def _xml_bytes(root):
    body = ET.tostring(root, encoding='utf-8')
    return b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n' + body


def _part_matches(part, prefix):
    return part.lstrip('/').startswith(prefix.lstrip('/'))


def _get_core_xml_tree(file_bytes):
    with zipfile.ZipFile(io.BytesIO(file_bytes)) as zf:
        if 'docProps/core.xml' not in zf.namelist():
            return None
        with zf.open('docProps/core.xml') as f:
            return ET.parse(f)


def read_metadata(file_bytes):
    """
    Baca metadata dari DOCX.
    Returns: (meta, tiers)
    """
    meta = {}
    tiers = {'tier1': [], 'tier2': [], 'tier3': []}

    with zipfile.ZipFile(io.BytesIO(file_bytes)) as zf:
        names = set(zf.namelist())

        # core.xml
        if 'docProps/core.xml' in names:
            try:
                root = ET.fromstring(zf.read('docProps/core.xml'))
                for elem in root:
                    ln = _localname(elem.tag)
                    if ln in CORE_TIERS:
                        val = (elem.text or '').strip()
                        if val:
                            key = f'core:{ln}'
                            meta[key] = val
                            tiers[f'tier{CORE_TIERS[ln]}'].append(key)
            except Exception:
                pass

        # app.xml
        if 'docProps/app.xml' in names:
            try:
                root = ET.fromstring(zf.read('docProps/app.xml'))
                for elem in root:
                    ln = _localname(elem.tag)
                    if ln in APP_TIERS:
                        if ln in ('HeadingPairs', 'TitlesOfParts'):
                            val = '(struktur kompleks)'
                        else:
                            val = (elem.text or '').strip()
                        if val:
                            key = f'app:{ln}'
                            meta[key] = val
                            tiers[f'tier{APP_TIERS[ln]}'].append(key)
            except Exception:
                pass

        # custom.xml
        if 'docProps/custom.xml' in names:
            try:
                root = ET.fromstring(zf.read('docProps/custom.xml'))
                for prop in root:
                    name = prop.get('name', 'unknown')
                    text = ''
                    for child in prop.iter():
                        if child.text and child.text.strip():
                            text = child.text.strip()
                            break
                    key = f'custom:{name}'
                    meta[key] = text or '(kosong)'
                    tiers['tier1'].append(key)
            except Exception:
                pass

        # customXml folder
        custom_xml = [n for n in names if n.startswith('customXml/')]
        if custom_xml:
            key = 'customXml:__folder__'
            meta[key] = f'({len(custom_xml)} file)'
            tiers['tier1'].append(key)

    return meta, tiers


def _clean_simple(data, remove_names):
    try:
        root = ET.fromstring(data)
        for elem in list(root):
            if _localname(elem.tag) in remove_names:
                root.remove(elem)
        return _xml_bytes(root)
    except Exception:
        return data


def _clean_custom(data, custom_names):
    try:
        root = ET.fromstring(data)
        for prop in list(root):
            if prop.get('name') in custom_names:
                root.remove(prop)
        return _xml_bytes(root)
    except Exception:
        return data


def _clean_content_types(data, removed_paths, removed_prefixes):
    try:
        root = ET.fromstring(data)
        for child in list(root):
            if _localname(child.tag) == 'Override':
                part = (child.get('PartName', '') or '').lstrip('/')
                remove = part in removed_paths
                if not remove:
                    for prefix in removed_prefixes:
                        if part.startswith(prefix.rstrip('/')):
                            remove = True
                            break
                if remove:
                    root.remove(child)
        return _xml_bytes(root)
    except Exception:
        return data


def _clean_rels(data, removed_paths, removed_prefixes):
    try:
        root = ET.fromstring(data)
        for child in list(root):
            if _localname(child.tag) == 'Relationship':
                target = (child.get('Target', '') or '').lstrip('/')
                remove = target in removed_paths
                if not remove:
                    for prefix in removed_prefixes:
                        if target.startswith(prefix.rstrip('/')):
                            remove = True
                            break
                if remove:
                    root.remove(child)
        return _xml_bytes(root)
    except Exception:
        return data


def remove_metadata(file_bytes, selected_keys=None, remove_all=False):
    """
    Hapus metadata dari DOCX.
    """
    if selected_keys is None:
        selected_keys = []
    selected = set(selected_keys)

    if remove_all:
        for k, t in CORE_TIERS.items():
            if t in (1, 2):
                selected.add(f'core:{k}')
        for k, t in APP_TIERS.items():
            if t in (1, 2):
                selected.add(f'app:{k}')
        selected.add('custom:__all__')
        selected.add('customXml:__folder__')

    core_remove = set()
    app_remove = set()
    custom_all = False
    custom_names = set()
    customxml_all = False

    for key in selected:
        if key.startswith('core:'):
            core_remove.add(key.split(':', 1)[1])
        elif key.startswith('app:'):
            app_remove.add(key.split(':', 1)[1])
        elif key == 'custom:__all__':
            custom_all = True
        elif key.startswith('custom:'):
            custom_names.add(key.split(':', 1)[1])
        elif key == 'customXml:__folder__':
            customxml_all = True

    removed_paths = set()
    removed_prefixes = []
    if customxml_all:
        removed_prefixes.append('customXml/')
    if custom_all:
        removed_prefixes.append('docProps/custom.xml')

    input_zip = zipfile.ZipFile(io.BytesIO(file_bytes), 'r')
    output = io.BytesIO()
    output_zip = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)

    for item in input_zip.infolist():
        name = item.filename

        skip = False
        if name in removed_paths:
            skip = True
        else:
            for prefix in removed_prefixes:
                if name.startswith(prefix):
                    skip = True
                    break
        if skip:
            continue

        data = input_zip.read(name)

        if name == 'docProps/core.xml' and core_remove:
            data = _clean_simple(data, core_remove)
        elif name == 'docProps/app.xml' and app_remove:
            data = _clean_simple(data, app_remove)
        elif name == 'docProps/custom.xml':
            if custom_all:
                data = EMPTY_CUSTOM_XML
            elif custom_names:
                data = _clean_custom(data, custom_names)
        elif name.endswith('.rels') and (removed_paths or removed_prefixes):
            data = _clean_rels(data, removed_paths, removed_prefixes)
        elif name == '[Content_Types].xml' and (removed_paths or removed_prefixes):
            data = _clean_content_types(data, removed_paths, removed_prefixes)

        output_zip.writestr(item, data)

    output_zip.close()
    input_zip.close()
    return output.getvalue()