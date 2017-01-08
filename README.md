# ji

Look up Kanji information from the CLI.

## Features

* Has 3793 kanji in its dictionary!
* Lists the most common on'yomi and kun'yomi readings.
* Can look up frequency, JLPT level, Jouyou grade, Heisig index.
* Can limit examples to a certain number.

## Dependencies

* Python >= 3.0
* lxml

You may install lxml as follows,

On Arch Linux:

    sudo pacman -S python-lxml

On Debian/Ubuntu:

    sudo apt-get install python3-lxml

Using pip:

    sudo pip install lxml

## Installation

    git clone https://github.com/bozbalci/ji
    chmod +x ji/ji
    cp ji/ji ~/bin # or to any other directory in $PATH

    # You can, alternatively, move the dictionary file to
    # somewhere else. Don't forget to edit the line in
    # the script to point to the new location.
    mkdir -p ~/.local/share/ji
    cp ji/kanji_all.xml ~/.local/share/ji

## Usage

    usage: ji [options]

    Look up kanji information from the CLI.

    positional arguments:
      kanji               the kanji to search for

    optional arguments:
      -h, --help          show this help message and exit
      -m, --minimal       produce minimal output
      -M, --mnemonics     show mnemonics
      -n, --nanori        list nanori readings
      -e N, --examples N  print the first N examples

## Examples

    $ ji -m 人
    人
    person
    On: ジン、ニン
    Kun: ひと、-り、-と
    JLPT N5, Jouyou: 1, Freq: 5, Heisig: 1023 [person]

    $ ji -e 3 字
    字
    character, letter, word, section of village
    On: ジ
    Kun: あざ、あざな、-な
    JLPT N4, Jouyou: 1, Freq: 485, Heisig: 197 [character]

    Examples:
    文字(もんじ): (1) letter (of alphabet); character (2) literal
    黒字(くろじ): balance (figure) in the black
    数字(すうじ): numeral; figure; digit; numeric character

## Tips

You may use ji from Vim to look up the kanji in the text file you are currently editing. Add this line to your `.vimrc`,

    nmap <leader>j "jyl:!ji -m <Ctrl+R>j<CR>

(Note: replace Ctrl+R with the actual key combination!)

Then, when your cursor is on a kanji in normal mode, you can type `<leader>j` and the kanji information will be shown in the terminal screen.

Kanji information retrieved from [All in One Kanji Deck (Heisig's RTK Order, 6th Edition)](https://ankiweb.net/shared/info/1862058740).
