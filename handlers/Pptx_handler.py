"""
PPTX handler — ZIP + XML dengan tier-based cleanup lengkap.
Termasuk: thumbnail, commentAuthors, comments, people, notesSlides,
          media (EXIF strip), tags, extLst IDs, slide names.
"""
import io
import zipfile
import xml.etree.ElementTree as ET
from PIL import Image


NS_CP = 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'
NS_DC = 'http://purl.org/dc/elements/1.1/'
NS_DCTERMS = 'http://purl.org/dc/terms/'
NS_EP = 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'
NS_VT = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_P14 = 'http://schemas.microsoft.com/office/powerpoint/2010/main'

ET.register_namespace('cp', NS_CP)
ET.register_namespace('dc', NS_DC)
ET.register_namespace('dcterms', NS_DCTERMS)
ET.register_namespace('vt', NS_VT)
ET.register_namespace('', NS_EP)
ET.register_namespace('p', NS_P)
ET.register_namespace('p14', NS_P14)


CORE_TIERS = {
    'creator': 1, 'lastModifiedBy': 1, 'created': 1, 'modified': 1,
    'lastPrinted': 1, 'revision': 1, 'subject': 1, 'description': 1,
    'keywords': 1, 'category': 1, 'contentStatus': 1,
    'title': 3, 'language': 3, 'identifier': 3, 'version': 3,
}

APP_TIERS = {
    'Company': 1, 'Manager': 1, 'Application': 1, 'AppVersion': 1,
    'Template': 1, 'TotalTime': 1, 'HyperlinkBase': 1,
    'Slides': 2, 'Notes': 2, 'HiddenSlides': 2, 'MMClips': 2,
    'Words': 2, 'Characters': 2, 'Lines': 2, 'Paragraphs': 2,
    'HeadingPairs': 2, 'TitlesOfParts': 2, 'PresentationFormat': 2,
    'SharedDoc': 2, 'HyperlinksChanged': 2, 'LinksUpToDate': 2,
    'ScaleCrop': 2, 'DocSecurity': 2,
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


def _normalize_path(base, target):
    if target.startswith('http://') or target.startswith('https://'):
        return None
    if target.startswith('/'):
        full = target.lstrip('/')
    else:
        full = base + target
    full = full.replace('\\', '/')
    parts = full.split('/')
    norm = []
    for p in parts:
        if p == '..':
            if norm:
                norm.pop()
        elif p in ('', '.'):
            continue
        else:
            norm.append(p)
    return '/'.join(norm)


# ============ Parsing ============
def read_metadata(file_bytes):
    meta = {}
    tiers = {'tier1': [], 'tier2': [], 'tier3': []}

    with zipfile.ZipFile(io.BytesIO(file_bytes)) as zf:
        names = set(zf.namelist())

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

        if any(n.startswith('customXml/') for n in names):
            cx = [n for n in names if n.startswith('customXml/')]
            meta['customXml:__folder__'] = f'({len(cx)} file)'
            tiers['tier1'].append('customXml:__folder__')

        if 'docProps/thumbnail.jpeg' in names:
            meta['extras:thumbnail'] = 'Thumbnail present'
            tiers['tier1'].append('extras:thumbnail')

        if 'ppt/commentAuthors.xml' in names:
            meta['extras:commentAuthors'] = 'Ada'
            tiers['tier1'].append('extras:commentAuthors')

        comments = [n for n in names if n.startswith('ppt/comments/')]
        if comments:
            meta['extras:comments'] = f'({len(comments)} file)'
            tiers['tier1'].append('extras:comments')

        if 'ppt/people.xml' in names:
            meta['extras:people'] = 'Ada'
            tiers['tier1'].append('extras:people')

        notes = [n for n in names if n.startswith('ppt/notesSlides/notesSlide') and n.endswith('.xml')]
        if notes:
            meta['extras:notesSlides'] = f'({len(notes)} slide catatan)'
            tiers['tier1'].append('extras:notesSlides')

        media = [n for n in names if n.startswith('ppt/media/')]
        if media:
            meta['extras:media_exif'] = f'({len(media)} file media)'
            tiers['tier1'].append('extras:media_exif')

        has_ext_ids = False
        for n in names:
            if n.startswith('ppt/slides/slide') and n.endswith('.xml'):
                try:
                    d = zf.read(n)
                    if b'creationId' in d or b'modId' in d:
                        has_ext_ids = True
                        break
                except Exception:
                    pass
        if has_ext_ids:
            meta['extras:extLst_ids'] = 'Ada di slide'
            tiers['tier1'].append('extras:extLst_ids')

        if any(n.startswith('ppt/tags/') for n in names):
            meta['extras:tags'] = 'Ada'
            tiers['tier2'].append('extras:tags')

    return meta, tiers


# ============ Cleaners ============
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


def _clear_notes_text(data):
    try:
        root = ET.fromstring(data)
        for elem in root.iter():
            if _localname(elem.tag) == 't':
                elem.text = ''
        return _xml_bytes(root)
    except Exception:
        return data


def _strip_image_exif(data):
    try:
        img = Image.open(io.BytesIO(data))
        fmt = (img.format or 'JPEG').upper()
        if fmt not in ('JPEG', 'JPG', 'PNG', 'WEBP', 'TIFF', 'BMP', 'GIF'):
            return data
        if img.mode in ('P', 'LA'):
            img = img.convert('RGBA')
        clean = Image.new(img.mode, img.size)
        clean.putdata(list(img.getdata()))
        out = io.BytesIO()
        if fmt in ('JPEG', 'JPG'):
            clean.save(out, format='JPEG', quality=95)
        elif fmt == 'PNG':
            clean.save(out, format='PNG')
        elif fmt == 'WEBP':
            clean.save(out, format='WEBP')
        elif fmt == 'TIFF':
            clean.save(out, format='TIFF')
        elif fmt == 'BMP':
            clean.save(out, format='BMP')
        elif fmt == 'GIF':
            clean.save(out, format='GIF')
        return out.getvalue()
    except Exception:
        return data


def _clean_slide_xml(data, remove_extLst_ids, remove_slide_names):
    try:
        root = ET.fromstring(data)

        if remove_extLst_ids:
            for parent in list(root.iter()):
                for child in list(parent):
                    if _localname(child.tag) == 'extLst':
                        for ext in list(child):
                            if _localname(ext.tag) == 'ext':
                                has_id = False
                                for sub in ext.iter():
                                    if _localname(sub.tag) in ('creationId', 'modId'):
                                        has_id = True
                                        break
                                if has_id:
                                    child.remove(ext)
                        if len(child) == 0:
                            try:
                                parent.remove(child)
                            except ValueError:
                                pass

        if remove_slide_names:
            for elem in root.iter():
                if _localname(elem.tag) == 'cSld' and 'name' in elem.attrib:
                    del elem.attrib['name']

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


def _clean_rels_generic(data, rels_path, removed_paths, removed_prefixes):
    try:
        root = ET.fromstring(data)
        if '/_rels/' in rels_path:
            base = rels_path.split('/_rels/')[0] + '/'
        else:
            base = ''
        for child in list(root):
            if _localname(child.tag) == 'Relationship':
                target = child.get('Target', '')
                full = _normalize_path(base, target)
                if full is None:
                    continue
                remove = full in removed_paths
                if not remove:
                    for prefix in removed_prefixes:
                        if full.startswith(prefix.rstrip('/')):
                            remove = True
                            break
                if remove:
                    root.remove(child)
        return _xml_bytes(root)
    except Exception:
        return data


def remove_metadata(file_bytes, selected_keys=None, remove_all=False):
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
        selected.update([
            'custom:__all__', 'customXml:__folder__',
            'extras:thumbnail', 'extras:commentAuthors', 'extras:comments',
            'extras:people', 'extras:notesSlides', 'extras:media_exif',
            'extras:extLst_ids', 'extras:tags',
        ])

    core_remove = set()
    app_remove = set()
    custom_all = False
    custom_names = set()
    delete_customXml = False
    delete_thumbnail = False
    delete_commentAuthors = False
    delete_comments = False
    delete_people = False
    clear_notes = False
    strip_media = False
    remove_extLst_ids = False
    delete_tags = False

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
            delete_customXml = True
        elif key == 'extras:thumbnail':
            delete_thumbnail = True
        elif key == 'extras:commentAuthors':
            delete_commentAuthors = True
        elif key == 'extras:comments':
            delete_comments = True
        elif key == 'extras:people':
            delete_people = True
        elif key == 'extras:notesSlides':
            clear_notes = True
        elif key == 'extras:media_exif':
            strip_media = True
        elif key == 'extras:extLst_ids':
            remove_extLst_ids = True
        elif key == 'extras:tags':
            delete_tags = True

    removed_paths = set()
    removed_prefixes = []
    if delete_customXml:
        removed_prefixes.append('customXml/')
    if custom_all:
        removed_prefixes.append('docProps/custom.xml')
    if delete_thumbnail:
        removed_paths.add('docProps/thumbnail.jpeg')
    if delete_commentAuthors:
        removed_paths.add('ppt/commentAuthors.xml')
    if delete_comments:
        removed_prefixes.append('ppt/comments/')
    if delete_people:
        removed_paths.add('ppt/people.xml')
    if delete_tags:
        removed_prefixes.append('ppt/tags/')

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
        elif name.startswith('ppt/notesSlides/notesSlide') and name.endswith('.xml') and clear_notes:
            data = _clear_notes_text(data)
        elif name.startswith('ppt/media/') and strip_media:
            data = _strip_image_exif(data)
        elif name.startswith('ppt/slides/slide') and name.endswith('.xml') and remove_extLst_ids:
            data = _clean_slide_xml(data, remove_extLst_ids, False)
        elif name.endswith('.rels') and (removed_paths or removed_prefixes):
            data = _clean_rels_generic(data, name, removed_paths, removed_prefixes)
        elif name == '[Content_Types].xml' and (removed_paths or removed_prefixes):
            data = _clean_content_types(data, removed_paths, removed_prefixes)

        output_zip.writestr(item, data)

    output_zip.close()
    input_zip.close()
    return output.getvalue()