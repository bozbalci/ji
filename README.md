# ji

Look up Kanji information from the CLI.

## Features

* Has 3793 kanji in its dictionary!
* Lists the most common on'yomi and kun'yomi readings.
* Search by kanji literals, Heisig index, stroke count, JLPT level, etc.
* Works well with other command-line programs such as `sort`, `column`, etc.

## Dependencies

* Python >= 3.2
* lxml

You may install lxml as follows,

On Arch Linux:

    sudo pacman -S python-lxml

On Debian/Ubuntu:

    sudo apt-get install python3-lxml

Using pip:

    sudo pip install lxml

## Usage

    usage: ji [options]

    Look up Kanji information from the CLI.

    positional arguments:
      kanji                 search by Kanji

    optional arguments:
      -h, --help            show this help message and exit
      -F FILE, --file FILE  search for all Kanji contained in a file
      -a, --all             match all Kanji included in Remembering the Kanji
                            books
      -N level, --jlpt level
                            match all Kanji in JLPT level
      -J grade, --jouyou grade
                            match all Kanji in Jouyou grade grade
      -S num, --strokes num
                            match all Kanji with num strokes
      -k KEYWORD, --keyword KEYWORD
                            search Kanji by Heisig keyword
      -i index, --rtk-index index
                            search Kanji by their Heisig index
      -f FORMAT, --format FORMAT
                            specify output formatting
      -s string, --separator string
                            specify the output separator
      -o, --only-kanji      produce a wall of text which consists of Kanji
      -m, --minimal         produce minimal output (no examples, no mnemonics)

    Available placeholders: {kanji} {kunyomi} {onyomi} {nanori} {english} {jlpt-
    level} {jouyou-grade} {frequency} {number-of-strokes} {kanji-radical}
    {radical-number} {radical-strokes} {radical-reading} {traditional-form}
    {classification} {keyword} {koohii-story-1} {koohii-story-2} {rtk-index}
    {examples} {components}

## Examples

Find Kanji by its Heisig index:

    $ ji -i 2
    二
    two [two]
    Kun: ふた、ふた.つ、ふたたび
    On: ニ、ジ
    JLPT N5, Jouyou: 1, Freq.: 9, Heisig: 2, Strokes: 2

Minimal output:

    $ ji -m 方
    方 direction, person, alternative

Minimum output (equivalent to `-f {kanji} -s ""`):

    $ ji -o "「浦島太郎」は、日本の古い話です。"
    浦島太郎日本古話

You can read from files:

    $ ji -oF haiku.txt
    水無月虚空涼時鳥

... or from stdin:

    $ echo "外国人" | ji -m
    外 outside
    国 country
    人 person

You can customize your output, and use coreutils to prettify it:

    $ ji -S2 -f "{kanji},{keyword},{rtk-index}" | tac | head -5 | column -ts,
    人  person    1023
    力  power     922
    入  enter     842
    又  or again  752
    了  complete  101

You can search Kanji by their Jouyou grade or JLPT level:

    $ ji -o -J1 | sed 's/.\{20\}/&\n/g'
    一二三四五六七八九十口日月田目早白百中千
    上下貝見左右町子女小大夕名石川水土火字木
    林森村本草犬先王玉金車学正雨天立音虫手出
    山入耳力男竹人休花年校足空糸青生文赤円気

You can search Kanji by their Heisig keywords:

    $ ji -k "water" -f "{kanji},{keyword},{rtk-index}" | column -ts,
    水  water            137
    滝  waterfall        576
    湯  hot water        585
    洵  swirling waters  2387
    汀  water's edge     2405
    汲  draw water       2413

You can customize your output to include examples, radical information, mnemonics and much more. There is a list of all available placeholders found at `ji -h`.

## Tips

You may use ji from Vim to look up the kanji in the text file you are currently editing. Add this line to your `.vimrc`,

    nmap <leader>j "jyl:!ji -m <Ctrl+R>j<CR>

(Note: replace Ctrl+R with the actual key combination!)

Then, when your cursor is on a kanji in normal mode, you can type `<leader>j` and the kanji information will be shown in the terminal screen.

Kanji information retrieved from [All in One Kanji Deck (Heisig's RTK Order, 6th Edition)](https://ankiweb.net/shared/info/1862058740).
