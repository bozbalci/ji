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
import os
import sys

from lxml import etree

# Edit this line to change the dictionary path
DICTIONARY_PATH = "~/.local/share/ji/kanji_all.xml"

def _absolute_path(path):
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)

    return path

class Kanji(object):
    def __init__(self, entry):
        """ Builds a Kanji object from an XML element. """

        self._entry = entry
        self.kanji = entry.find("kanji").text
        self.kunyomi = entry.find("kunyomi").text
        self.onyomi = entry.find("onyomi").text
        self.nanori = entry.find("nanori").text
        self.english = entry.find("english").text

        # default value for max examples is -1, prints all examples
        self.max_examples = -1
        self.examples = []
        for ex in entry.find("examples").getchildren():
            self.examples.append(ex.text)

        self.jlpt_level = entry.find("jlpt-level").text
        self.jouyou_grade = entry.find("jouyou-grade").text
        self.frequency = entry.find("frequency").text

        self.components = []
        for cp in entry.find("components").getchildren():
            self.components.append(cp.text)

        self.number_of_strokes = entry.find("number-of-strokes").text
        self.kanji_radical = entry.find("kanji-radical").text
        self.radical_number = entry.find("radical-number").text
        self.radical_strokes = entry.find("radical-strokes").text
        self.radical_reading = entry.find("radical-reading").text
        self.traditional_form = entry.find("traditional-form").text
        self.classification = entry.find("classification").text
        self.keyword = entry.find("keyword").text
        self.koohii_story_1 = entry.find("koohii-story-1").text
        self.koohii_story_2 = entry.find("koohii-story-2").text
        self.rtk_index = entry.find("rtk-index").text

    def _examples(self):
        result = []

        if self.max_examples > 0:
            for _, ex in zip(range(self.max_examples), self.examples):
                result.append(ex)
        else:
            if self.max_examples == -1:
                for ex in self.examples:
                    result.append(ex)
            if self.max_examples == 0:
                result = []

        # remove empty examples
        result = [ex for ex in result if ex is not None]

        return "\n".join(result)
    
    def _components(self):
        result = self.components

        if result[0] is None:
            return "None"

        return "\n".join(result)

    def _replace_format(self):
        placeholders = {
            "%kanji%": self.kanji,
            "%kun%": self.kunyomi,
            "%on%": self.onyomi,
            "%nanori%": self.nanori,
            "%meaning%": self.english,
            "%examples%": self._examples(),
            "%jlpt%": self.jlpt_level,
            "%jouyou%": self.jouyou_grade,
            "%freq%": self.frequency,
            "%components%": self._components(),
            "%strokes%": self.number_of_strokes,
            "%radical%": self.kanji_radical,
            "%radical_number%": self.radical_number,
            "%radical_strokes%": self.radical_strokes,
            "%radical_reading%": self.radical_reading,
            "%traditional_form%": self.traditional_form,
            "%classification%": self.classification,
            "%keyword%": self.keyword,
            "%story1%": self.koohii_story_1,
            "%story2%": self.koohii_story_2,
            "%index%": self.rtk_index,
        }

        result = self.format
        for k, v in placeholders.items():
            try:
                result = result.replace(k, v)
            except:
                result = result.replace(k, "")

        return result

    def __str__(self):
        try:
            return self._replace_format()
        except AttributeError:
            return self.kanji

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
            result.append(Kanji(entry))

        return result

    def _entries_exact(self, tag, query):
        return self._get_entries(self._search_text_exact(tag, query))
    
    def _entries_contains(self, tag, query):
        return self._get_entries(self._search_text_contains(tag, query))

    def _entries_nonempty(self, tag):
        return self._get_entries(self._search_text_nonempty(tag))

    # bunch of wrappers for public usage
    def by_kanji(self, query):
        return self._entries_exact("kanji", query)
    
    def by_kunyomi(self, query):
        return self._entries_contains("kunyomi", query)
    
    def by_onyomi(self, query):
        return self._entries_contains("onyomi", query)
    
    def by_meaning(self, query):
        return self._entries_contains("english", query)
    
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

format_default = """\
%kanji%
%meaning% [%keyword%]
On: %on%
Kun: %kun%
JLPT N%jlpt%, Jouyou: %jouyou%, \
Freq.: %freq%, Heisig: %index%, \
Strokes: %strokes%

Examples:
%examples%

Mnemonics:
%story1%
%story2%
"""

format_minimal = """\
%kanji%
%meaning% [%keyword%]
On: %on%
Kun: %kun%
JLPT N%jlpt%, Jouyou: %jouyou%, \
Freq.: %freq%, Heisig: %index%, \
Strokes: %strokes%
"""

# parse command-line arguments
def _positive_integer(string):
    value = int(string)
    if value < 0:
        msg = "{} is not a positive number" % string
        raise argparse.ArgumentTypeError(msg)
    return value

def main():
    parser = argparse.ArgumentParser(
        prog="ji",
        usage="%(prog)s [options]",
        description="Look up kanji information from the CLI.",
        epilog="""Available placeholders are: %kanji% %kun% %on% %nanori% %meaning% \
                %examples% %jlpt% %jouyou% %freq% %components% %strokes% %radical% \
                %radical_number% %radical_strokes% %radical_reading% %traditional_form% \
                %classification% %keyword% %story1% %story2% %index% \
                """
    )
    parser.add_argument("kanji", nargs="?", help="search by kanji")
    parser.add_argument("-a", "--all", action="store_true",
            help="match every kanji with a Heisig index")
    parser.add_argument("-N", "--jlpt", metavar="LEVEL",
        type=_positive_integer, help="list all kanji in JLPT %(metavar)s")
    parser.add_argument("-J", "--jouyou", metavar="GRADE",
        help="list all kanji in Jouyou grade %(metavar)s")
    parser.add_argument("-i", "--rtk-index", metavar="INDEX",
        help="search kanji by Heisig index")
    parser.add_argument("-f", "--format", default=format_default,
        help="specify output formatting")
    parser.add_argument("-o", "--only-kanji", action="store_true",
        help="only print the matching kanji characters")
    parser.add_argument("-m", "--minimal", action="store_true",
        help="produce minimal output (no examples, no mnemonics)")
    parser.add_argument("-M", "--mnemonics", action="store_true",
        help="when combined with -m, print mnemonics as well")
    parser.add_argument("-e", "--examples", metavar="NUM", default=-1,
        type=_positive_integer, help="prints the first %(metavar)s examples")
    options = parser.parse_args()

    # Unescape newlines, tabs, etc.
    options.format = codecs.getdecoder("unicode_escape")(options.format)[0]

    # find and print the requested information, then exit
    kd = KanjiDictionary()

    if options.all:
        matches = kd.all_rtk_index()
    elif options.jlpt:
        matches = kd.by_jlpt_level(options.jlpt)
    elif options.jouyou:
        matches = kd.by_jouyou_grade(options.jouyou)
    elif options.rtk_index:
        matches = kd.by_rtk_index(options.rtk_index)
    else:
        matches = kd.by_kanji(options.kanji)

    if matches == []:
        sys.stderr.write("No kanji found.\n")
        sys.exit(1)

    search_results = []
    for kanji in matches:
        if options.only_kanji:
            search_results.append(str(kanji))
        else:
            if options.minimal:
                kanji.format = format_minimal
                
                if options.mnemonics:
                    kanji.format += "\n%story1%\n%story2%\n"
            else:
                kanji.format = options.format

            kanji.max_examples = options.examples
            search_results.append(str(kanji))

    if options.only_kanji:
        output = "".join(search_results)
        print(output)
    elif options.format != format_default:
        output = "\n".join(search_results)
        print(output)
    else:
        output = "\n".join(search_results)
        print(output, end="")

if __name__ == "__main__":
    main()
