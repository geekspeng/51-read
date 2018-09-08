# -*- coding: utf-8 -*-
# @Time    : 2018/9/8 12:44
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
import os
import zipfile

import lxml.html
from iso639 import languages as isoLanguages

from app import uploads
from app.utils.book_meta import BookMeta

etree = lxml.html.etree


def extract_cover(zip_file, zip_cover_path, file_path):
    if zip_cover_path:
        cf = zip_file.read(zip_cover_path)
        prefix = os.path.splitext(file_path)[0]
        cover_path = prefix + '.jpg'
        with open(uploads.path(cover_path), 'wb') as image:
            image.write(cf)
        return cover_path
    else:
        return ''


def get_epub_meta(abs_file_path, file_path, file_name, file_extension):
    ns = {
        'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
        'pkg': 'http://www.idpf.org/2007/opf',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }

    epubZip = zipfile.ZipFile(abs_file_path)
    txt = epubZip.read('META-INF/container.xml')
    tree = etree.fromstring(txt)
    cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path', namespaces=ns)[0]
    cf = epubZip.read(cfname)
    tree = etree.fromstring(cf)

    cfpath = os.path.dirname(cfname)

    p = tree.xpath('/pkg:package/pkg:metadata', namespaces=ns)[0]

    epub_metadata = {}

    for s in ['title', 'description', 'creator', 'language', 'subject']:
        tmp = p.xpath('dc:%s/text()' % s, namespaces=ns)
        if len(tmp) > 0:
            epub_metadata[s] = p.xpath('dc:%s/text()' % s, namespaces=ns)[0]
        else:
            epub_metadata[s] = "Unknown"

    if epub_metadata['subject'] == "Unknown":
        epub_metadata['subject'] = ''

    if epub_metadata['description'] == "Unknown":
        description = tree.xpath("//*[local-name() = 'description']/text()")
        if len(description) > 0:
            epub_metadata['description'] = description
        else:
            epub_metadata['description'] = ""

    if epub_metadata['language'] == "Unknown":
        epub_metadata['language'] = ""
    else:
        lang = epub_metadata['language'].split('-', 1)[0].lower()
        if len(lang) == 2:
            epub_metadata['language'] = isoLanguages.get(part1=lang).name
        elif len(lang) == 3:
            epub_metadata['language'] = isoLanguages.get(part3=lang).name
        else:
            epub_metadata['language'] = ""

    series = tree.xpath("/pkg:package/pkg:metadata/pkg:meta[@name='calibre:series']/@content", namespaces=ns)
    if len(series) > 0:
        epub_metadata['series'] = series[0]
    else:
        epub_metadata['series'] = ''

    series_id = tree.xpath("/pkg:package/pkg:metadata/pkg:meta[@name='calibre:series_index']/@content", namespaces=ns)
    if len(series_id) > 0:
        epub_metadata['series_id'] = series_id[0]
    else:
        epub_metadata['series_id'] = '1'

    coversection = tree.xpath("/pkg:package/pkg:manifest/pkg:item[@id='cover-image']/@href", namespaces=ns)
    cover_path = ''
    if len(coversection) > 0:
        zip_cover_path = os.path.join(cfpath, coversection[0]).replace('\\', '/')
        cover_path = extract_cover(epubZip, zip_cover_path, abs_file_path)
    else:
        meta_cover = tree.xpath("/pkg:package/pkg:metadata/pkg:meta[@name='cover']/@content", namespaces=ns)
        if len(meta_cover) > 0:
            coversection = tree.xpath("/pkg:package/pkg:manifest/pkg:item[@id='" + meta_cover[0] + "']/@href",
                                      namespaces=ns)
            if len(coversection) > 0:
                filetype = coversection[0].rsplit('.', 1)[-1]
                if filetype == "xhtml" or filetype == "html":  # if cover is (x)html format
                    markup = epubZip.read(os.path.join(cfpath, coversection[0]))
                    markupTree = etree.fromstring(markup)
                    # no matter xhtml or html with no namespace
                    imgsrc = markupTree.xpath("//*[local-name() = 'img']/@src")
                    # imgsrc maybe startwith "../"" so fullpath join then relpath to cwd
                    zip_cover_path = os.path.relpath(
                        os.path.join(os.path.dirname(os.path.join(cfpath, coversection[0])), imgsrc[0])).replace('\\',
                                                                                                                 '/')
                    cover_path = extract_cover(epubZip, zip_cover_path, abs_file_path)
                else:
                    zip_cover_path = os.path.join(cfpath, coversection[0]).replace('\\', '/')
                    cover_path = extract_cover(epubZip, zip_cover_path, abs_file_path)

    if not epub_metadata['title']:
        title = file_name
    else:
        title = epub_metadata['title']

    return BookMeta(
        title=title,
        author=epub_metadata['creator'],
        cover_path=cover_path,
        description=epub_metadata['description'],
        tags=epub_metadata['subject'],
        series=epub_metadata['series'],
        series_id=epub_metadata['series_id'],
        languages=epub_metadata['language'],
        file_path=file_path,
        file_name=file_name,
        file_extension=file_extension,
        file_size=os.path.getsize(abs_file_path))
