# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://tcbscans.com/"""

from .common import ChapterExtractor, MangaExtractor
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:tcbscans|onepiecechapters)\.com"


class TcbscansChapterExtractor(ChapterExtractor):
    category = "tcbscans"
    root = "https://tcbscans.com"
    pattern = BASE_PATTERN + r"(/chapters/\d+/[^/?#]+)"
    example = "https://tcbscans.com/chapters/12345/MANGA-chapter-123"

    def images(self, page):
        return [
            (url, None)
            for url in text.extract_iter(
                page, '<img class="fixed-ratio-content" src="', '"')
        ]

    def metadata(self, page):
        manga, _, chapter = text.extr(
            page, 'font-bold mt-8">', "</h1>").rpartition(" - Chapter ")
        chapter, sep, minor = chapter.partition(".")
        return {
            "manga": text.unescape(manga),
            "chapter": text.parse_int(chapter),
            "chapter_minor": sep + minor,
            "lang": "en", "language": "English",
        }


class TcbscansMangaExtractor(MangaExtractor):
    category = "tcbscans"
    root = "https://tcbscans.com"
    chapterclass = TcbscansChapterExtractor
    pattern = BASE_PATTERN + r"(/mangas/\d+/[^/?#]+)"
    example = "https://tcbscans.com/mangas/123/MANGA"

    def chapters(self, page):
        data = {
            "manga": text.unescape(text.extr(
                page, 'class="my-3 font-bold text-3xl">', "</h1>")),
            "lang": "en", "language": "English",
        }

        results = []
        page = text.extr(page, 'class="col-span-2"', 'class="order-1')
        for chapter in text.extract_iter(page, "<a", "</a>"):
            url = text.extr(chapter, 'href="', '"')
            data["title"] = text.unescape(text.extr(
                chapter, 'text-gray-500">', "</div>"))
            chapter = text.extr(
                chapter, 'font-bold">', "</div>").rpartition(" Chapter ")[2]
            chapter, sep, minor = chapter.partition(".")
            data["chapter"] = text.parse_int(chapter)
            data["chapter_minor"] = sep + minor
            results.append((self.root + url, data.copy()))
        return results
