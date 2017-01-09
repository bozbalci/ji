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
      kanji                 search by kanji

    optional arguments:
      -h, --help            show this help message and exit
      -N LEVEL, --jlpt LEVEL
                            list all kanji in JLPT LEVEL
      -J GRADE, --jouyou GRADE
                            list all kanji in Jouyou grade GRADE
      -f FORMAT, --format FORMAT
                            specify output formatting
      -o, --only-kanji      only print the matching kanji characters
      -m, --minimal         produce minimal output (no examples, no mnemonics)
      -e NUM, --examples NUM
                            prints the first NUM examples

    Available placeholders are: %kanji% %kunyomi% %onyomi% %nanori% %english%
    %examples% %jlpt_level% %jouyou_grade% %frequency% %components%
    %number_of_strokes% %kanji_radical% %radical_number% %radical_strokes%
    %radical_reading% %traditional_form% %classification% %keyword%
    %koohii_story_1% %koohii_story_2% %rtk_index%

## Examples

Minimal output:

    $ ji -m 人
    人
    person [person]
    On: ジン、ニン
    Kun: ひと、-り、-と
    JLPT N5, Jouyou: 1, Freq.: 5, Heisig: 1023, Strokes: 2

Limiting examples to a certain number:

    $ ji -e 3 字

    字
    character, letter, word, section of village [character]
    On: ジ
    Kun: あざ、あざな、-な
    JLPT N4, Jouyou: 1, Freq.: 485, Heisig: 197, Strokes: 6

    Examples:
    文字(もんじ): (1) letter (of alphabet); character (2) literal
    黒字(くろじ): balance (figure) in the black
    数字(すうじ): numeral; figure; digit; numeric character

    Mnemonics:
    CHILDren learn Kanji characters underneath a HOUSE.
    Why do I have to wear this roof on my head all the time father? "Shut up! It builds character!".

Listing kanji by JLPT level or Jouyou grade:

    $ ji -N5 -o
    一二三四五六七八九十口日月目古白百中千上下見万左右子女母小少大多外名川水土時火魚安木本先金道車前高週学書言話語読雨天立北毎東電午国店手友会出山入分耳買男行人休花何年社半父校足空後食飲新生今西南間聞円来気長駅

    $ ji -J1 -o
    一二三四五六七八九十口日月田目早白百中千上下貝見左右町子女小大夕名石川水土火字木林森村本草犬先王玉金車学正雨天立音虫手出山入耳力男竹人休花年校足空糸青生文赤円気

Special formatting:

    $ ji -N5 -f "%kanji%,%number_of_strokes%"
    一,1
    二,2
    三,3
    四,5
    五,4
    六,4
    七,2
    ... # redacted
    
    $ ji -J1 -f "%kanji%" | wc -l
    80

## Tips

You may use ji from Vim to look up the kanji in the text file you are currently editing. Add this line to your `.vimrc`,

    nmap <leader>j "jyl:!ji -m <Ctrl+R>j<CR>

(Note: replace Ctrl+R with the actual key combination!)

Then, when your cursor is on a kanji in normal mode, you can type `<leader>j` and the kanji information will be shown in the terminal screen.

Kanji information retrieved from [All in One Kanji Deck (Heisig's RTK Order, 6th Edition)](https://ankiweb.net/shared/info/1862058740).
