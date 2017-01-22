#!/usr/bin/python
#
# Copyright (c) 2016, Berk Ozbalci
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import codecs
import fileinput
import os
import sys

from lxml import etree

# Edit this line to change the dictionary path
DICTIONARY_PATH = "~/.local/share/ji/kanji_all.xml"

def _is_kanji(char):
    """ Check if given character is a Kanji. """

    return ord("\u4e00") < ord(char) < ord("\u9fff")

def _uniq(lst):
    """ Return the unique elements from a list. 
        Retrieved from https://www.peterbe.com/plog/uniqifiers-benchmark """

    seen = set()
    seen_add = seen.add

    return [i for i in lst if not (i in seen or seen_add(i))]

def _filter_kanji(text):
    """ Return a list of all unique Kanji in a string. """
    
    return _uniq([c for c in text if _is_kanji(c)])

# Information fields in Kanji, where the contents are strings.
str_fields = [
    "kanji", "kunyomi", "onyomi", "nanori",
    "english", "jlpt-level", "jouyou-grade", "frequency",
    "number-of-strokes", "kanji-radical", "radical-number",
    "radical-strokes", "radical-reading", "traditional-form",
    "classification", "keyword", "koohii-story-1", "koohii-story-2", "rtk-index"
]

# Fields in Kanji where the content is a list of strings.
list_fields = ["examples", "components"]

def _absolute_path(path):
    """ Converts path to absolute paths, expands variables and users. """

    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)

    return path

class Kanji(object):
    """ Class for Chinese characters. """

    def __init__(self, entry):
        """ Builds a Kanji object from an XML element. """

        self._entry = entry

        self.str_data = {}
        for f in str_fields:
            self.str_data[f] = entry.find(f).text

        self.list_data = {}
        for f in list_fields:
            self.list_data[f] = []
            
            for e in entry.find(f).getchildren():
                self.list_data[f] += [e.text]

        # Flatten the list data for printing later
        self.list_data = {f: "\n".join(e) for f, e in self.list_data.items()
            if not None in e}

        self.data = {}
        self.data.update(self.str_data)
        self.data.update(self.list_data)

    def __str__(self):
        try:
            return self.formatter.process()
        except:
            return self.kanji

class FormatDefault(dict):
    """ Empty entries in the placeholder dictionary will be replaced
        empty strings to avoid raising KeyError, while using format_map. """

    def __missing__(self, key):
        return ""

class KanjiFormatter(object):
    """ Takes Kanji and returns a string formatted in a way specified by
        the user. """

    def __init__(self, output_format):
        self.output_format = output_format

    def load(self, kanji):
        self.kanji = kanji

    def process(self, kanji=None):
        if kanji is None:
            kanji = self.kanji

        return self.output_format.format_map(FormatDefault(kanji.data))

class KanjiDictionary(object):
    """ Parses the dictionary file and provides wrappers for search
        functions. """

    def __init__(self):
        self.root = etree.parse(_absolute_path(DICTIONARY_PATH))

    def _search_text_exact(self, tag, query):
        return self.root.xpath(".//{}[text()=\"{}\"]".format(tag, query))
    
    def _search_text_contains(self, tag, query):
        return self.root.xpath(".//{}[contains(text(),\"{}\")]".format(tag,
            query))

    def _search_text_nonempty(self, tag):
        return self.root.xpath(".//{}[string-length(text()) > 0]".format(tag))

    def _get_entries(self, search):
        result = []
        for match in search:
            entry = match.getparent()
            result += [Kanji(entry)]

        return result

    def _entries_exact(self, tag, query):
        return self._get_entries(self._search_text_exact(tag, query))
    
    def _entries_contains(self, tag, query):
        return self._get_entries(self._search_text_contains(tag, query))

    def _entries_nonempty(self, tag):
        return self._get_entries(self._search_text_nonempty(tag))

    # Bunch of wrappers for public usage
    def by_kanji(self, query):
        return self._entries_exact("kanji", query)
    
    def by_jlpt_level(self, query):
        return self._entries_exact("jlpt-level", query)
    
    def by_jouyou_grade(self, query):
        return self._entries_exact("jouyou-grade", query)
    
    def by_keyword(self, query):
        return self._entries_contains("keyword", query)
    
    def by_number_of_strokes(self, query):
        return self._entries_exact("number-of-strokes", query)
    
    def by_rtk_index(self, query):
        return self._entries_exact("rtk-index", query)

    def all_rtk_index(self):
        return self._entries_nonempty("rtk-index")

def parse_args():
    """ Parse the command-line arguments. """

    parser = argparse.ArgumentParser(
        prog="ji",
        usage="%(prog)s [options]",
        description="Look up Kanji information from the CLI.",
        epilog="Available placeholders: " + " ".join(
            ["{{{}}}".format(f) for f in str_fields + list_fields])
    )

    parser.add_argument("kanji", nargs="?", help="search by Kanji")
    parser.add_argument("-F", "--file", type=argparse.FileType('r'),
        default=sys.stdin, help="search for all Kanji contained in a file")
    parser.add_argument("-a", "--all", action="store_true",
        help="match all Kanji included in Remembering the Kanji books")
    parser.add_argument("-N", "--jlpt", metavar="level",
        type=int, help="match all Kanji in JLPT %(metavar)s")
    parser.add_argument("-J", "--jouyou", metavar="grade",
        type=int, help="match all Kanji in Jouyou grade %(metavar)s")
    parser.add_argument("-S", "--strokes", metavar="num",
        type=int, help="match all Kanji with %(metavar)s strokes")
    parser.add_argument("-k", "--keyword", help="search Kanji by Heisig keyword")
    parser.add_argument("-i", "--rtk-index", metavar="index",
        type=int, help="search Kanji by their Heisig index")
    parser.add_argument("-f", "--format", help="specify output formatting")
    parser.add_argument("-s", "--separator", metavar="string", default="\n",
        help="specify the output separator")
    parser.add_argument("-o", "--only-kanji", action="store_true",
        help="produce a wall of text which consists of Kanji")
    parser.add_argument("-m", "--minimal", action="store_true",
        help="produce minimal output (no examples, no mnemonics)")

    return parser.parse_args()

def main():
    options = parse_args()

    # Unescape newlines, tabs, etc.
    if options.format:
        options.format = codecs.getdecoder("unicode_escape")(options.format)[0]
    options.separator = codecs.getdecoder("unicode_escape")(options.separator)[0]

    # Construct the dictionary to make queries.
    kd = KanjiDictionary()

    # Determine the query from options passed to the script.
    if options.all:
        matches = kd.all_rtk_index()
    elif options.jlpt:
        matches = kd.by_jlpt_level(options.jlpt)
    elif options.jouyou:
        matches = kd.by_jouyou_grade(options.jouyou)
    elif options.strokes:
        matches = kd.by_number_of_strokes(options.strokes)
    elif options.keyword:
        matches = kd.by_keyword(options.keyword)
    elif options.rtk_index:
        matches = kd.by_rtk_index(options.rtk_index)
    elif options.kanji:
        matches = []

        for k in _filter_kanji(options.kanji):
            matches += kd.by_kanji(k)
    elif options.file:
        matches = []
        seen = []

        with options.file as f:
            for line in f:
                for k in _filter_kanji(line):
                    if k not in seen:
                        matches += kd.by_kanji(k)
                        seen += [k]
    else:
        matches = []

    if matches == []:
        sys.stderr.write("No kanji found.\n")
        sys.exit(1)

    # Determine the output format from options passed to the script.
    if options.only_kanji:
        output_format = "{kanji}"
    elif options.minimal:
        output_format = "{kanji} {english}"
    elif options.format:
        output_format = options.format
    else:
        output_format = ("{kanji}\n"
                         "{english} [{keyword}]\n"
                         "Kun: {kunyomi}\n"
                         "On: {onyomi}\n"
                         "JLPT N{jlpt-level}, Jouyou: {jouyou-grade}, "
                         "Freq.: {frequency}, Heisig: {rtk-index}, "
                         "Strokes: {number-of-strokes}\n")

    # Create a formatter object, and format the search results.
    formatter = KanjiFormatter(output_format)
    result = []
    for kanji in matches:
        formatter.load(kanji)
        result += [formatter.process()]

    if options.only_kanji:
        separator = ""
    else:
        separator = options.separator

    output = separator.join(result)
    print(output)

if __name__ == "__main__":
    main()
