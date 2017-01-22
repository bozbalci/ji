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
      -a, --all             match all Kanji included in Remembering the Kanji
                            books
      -N int, --jlpt int    match all Kanji in JLPT int
      -J grade, --jouyou grade
                            match all Kanji in Jouyou grade grade
      -S num, --strokes num
                            match all Kanji with num strokes
      -s string, --separator string
                            specify the output separator
      -i index, --rtk-index index
                            search Kanji by their Heisig index
      -f FORMAT, --format FORMAT
                            specify output formatting
      -o, --only-kanji      produce a wall of text which consists of Kanji
      -m, --minimal         produce minimal output (no examples, no mnemonics)
      -M, --mnemonics       when combined with -m, print mnemonics as well

    Available placeholders: {kanji} {kunyomi} {onyomi} {nanori} {english} {jlpt-
    level} {jouyou-grade} {frequency} {number-of-strokes} {kanji-radical}
    {radical-number} {radical-strokes} {radical-reading} {traditional-form}
    {classification} {classification} {keyword} {koohii-story-1} {koohii-story-2}
    {rtk-index} {examples} {components}

## Examples

Find Kanji by its Heisig index:

    $ ji -i 2
    二
    two [two]
    On: ニ、ジ
    Kun: ふた、ふた.つ、ふたたび
    JLPT N5, Jouyou: 1, Freq.: 9, Heisig: 2, Strokes: 2

    Examples:
    二(に): two
    二人(ふたり): two persons; two people; pair; couple
    二つ(ふたつ): two
    二十歳(はたち): (1) 20 years old (2) twenty
    二階建て(にかいだて): two-storied building
    真っ二つ(まっぷたつ): in two equal parts
    二日(ふつか): (1) second day of the month (2) two days
    二十日(はつか): (1) twentieth (day of the month) (2) twenty days

    Mnemonics:
    Two lines.
    Roman numeral II, written on its side.

Minimal output:

    $ ji -m 人
    人
    person [person]
    On: ジン、ニン
    Kun: ひと、-り、-と
    JLPT N5, Jouyou: 1, Freq.: 5, Heisig: 1023, Strokes: 2

Get all Kanji from a string:

    # -o is equivalent to -f "{kanji}" -s ""

    $ ji -o "「浦島太郎」は日本の古い話です。"
    島本話郎古日太浦

Pretty output:

    $ ji -S2 -f "{kanji},{keyword},{rtk-index}" | column -ts,
    二  two       2
    七  seven     7
    八  eight     8
    九  nine      9
    十  ten       10
    刀  sword     87
    丁  street    95
    了  complete  101
    又  or again  752
    入  enter     842
    力  power     922
    人  person    1023

Searching by Jouyou grade:

    $ ji -J3 -f "{kanji},{number-of-strokes}" | sort -rnk 2 | column -ts, | head
    鼻  14
    駅  14
    館  16
    飲  12
    題  18
    面  9
    集  12
    階  12
    陽  12
    院  10

## Tips

You may use ji from Vim to look up the kanji in the text file you are currently editing. Add this line to your `.vimrc`,

    nmap <leader>j "jyl:!ji -m <Ctrl+R>j<CR>

(Note: replace Ctrl+R with the actual key combination!)

Then, when your cursor is on a kanji in normal mode, you can type `<leader>j` and the kanji information will be shown in the terminal screen.

Kanji information retrieved from [All in One Kanji Deck (Heisig's RTK Order, 6th Edition)](https://ankiweb.net/shared/info/1862058740).
