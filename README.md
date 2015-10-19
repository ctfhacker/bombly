# Bombly - Keep Talking and Nobody Explodes Robot

## Product

[Hardcore Bomb1](https://www.youtube.com/watch?v=ydQEb6zyAuE)

This is a "expert" robot written in Python to assist in playing Keep Talking and Nobody Explodes.

In its traditional form, the bomb defuse talks with an expert who holds the [Bomb Manual](http://www.bombmanual.com). Based on the information given by the defuser, the expert scrambles through the manual give information back to the defuser to correctly secure the bomb.

This is just a problem waiting to be solved with Python. Below is my attempt to solve this problem.

WARNING: This does ruin the fun of the game. You have been warned!

## Installation

### Windows only

Install dragonfly

```
git clone https://github.com/t4ngo/dragonfly
cd dragonfly
python setup.py install
```

Start the bot

```
python dfly-loader-wsr.py
```

I believe dragonfly should work with Dragon NaturrallySpeaking, however, I did not use it.

## Commands available

The general idea is to speak a `command` then a series of words about that command.

### Bomb variables

```
batteries <#>         - Number of batteries on bomb
serial <#>            - Last digit of serial
vowel <true/false>    - Vowel in serial number
car <true/false>      - CAR indicator on bomb
freak <true/false>    - FRK indicator on bomb
parallel <true/false> - Parallel port on bomb
```

### Metabomb

```
bomb reset  - Reset global bomb variables
bomb status - Print current values of global attributes
```

### Simple Wires

```
simple wires <wires> - Where wires is in (red, blue, yellow, black, white, yellow)
```

Example:

```
simple wires red red blue blue yellow black
```

### Complex Wires

```
complex wires <wires> - Where wires is in (light, red, blue, star, blank, next)
```

Seperate each wire from left to right with `next`. `blank` is the reserved word for no attributes

Example:

```
complex wires red next blue star next light red blue star next blank

4 Wires:
Red
Blue with Star
Red/Blue with Light/Star
No attributes
```

### Maze

```
maze <coords> - Where coords are 3 pairs of numbers for indicator, start, stop
```
Note: Coords start at upper left (1, 1) and go horizontally then vertically.


Example maze and command:

```
X O X X
X X X X
S X X X
X X X F
```

```
maze 2 1 1 3 4 4
```

### Simon

```
simon <colors> - Where colors are in (red, blue, yellow, green)
```

Example:

```
simon red blue blue red
```

### Wire sequence

Say each wire in increasing order.

```
wire sequence <color destination> - where color in (red, blue, black) and destination in (apple, bravo, charlie)
```

Example:

```
1 -blue-- A

2 -red--- B

3 -black- C
```

```
wire sequence blue apple red blue black charlie
```

If two wire sequences in the same bomb, be sure to reset the wire sequence state between sequences.

```
wire sequence reset
```

### Button

Step 1:
```
button <color of button> <word>
```

If press and hold:

```
button color <color of strip>
```

### Memory

```
memory <display> <numbers from left to right>
```

Example:

```
    4
 2 3 4 1
```

```
memory 4 2 3 4 1
```

If two memory modules in the same bomb, be sure to reset the memory state:

```
memory reset
```

### Morse

```
morse <0/1 for one letter> - Where 0 is short and 1 is long
```

Rules for morse:
* Give the morse module one morse letter at a time.
* Be sure the letters are in succession of each other. 
* Only three letters are necessary.

Example:

```
-... ... -.-.
```

```
morse 1 0 0 0 
morse 0 0 0 
morse 1 0 1 0
```

If two morse modules in the same bomb, be sure to reset the morse state:

```
morse reset
```

### Symbols

```
symbols <symbols>
```

![column1](images/column1)

```
tennis, a, l, lightning, kitty, h, c
```

![column2](images/column2)

```
e, tennis, c, o, star, h, question
```

![column3](images/column3)

```
copyright, butt, o, k, r, l, star
```

![column4](images/column4)

```
six, paragraph, b, kitty, k, question, smile
```

![column5](images/column5)

```
goblet, smile, b, c, paragraph, three, star
```

![column6](images/column6)

```
six, e, equals, smash, goblet, n, omega
```

### Who's on First

Now for the fun module. This was is still a work in progress (check out the code for all of the cases)

```
words one <words> - Step 1 of Who's on First, lookup position
```

```
words two <words> - Step 2 of Who's on First, start giving words from lookup table
```

Below is the table of what spoken words coorelate to the words necessary to complete the challenge.

```
you are words: you are
your words: you are
done: done
don: done
you are letters: ur
sure: sure
shore: sure
you word: you
hold: hold
you letter: u
yes: yes
first: first
display: display
okay: okay
OK: okay
says: says
nothing: nothing
literally blank:
blank: blank
no: no
L. E. D.: led
lead: lead
mead: lead
read: read
red short: red
read too: reed
hold on two: hold on
you're word: your
your word: your
your mark: you're
you are marked: you're
you are mark: you're
c s: see
they are words: they are
e i r: their
e r e: there
they are marked: they're
they mark: they're
c s : see
c letter: c
see letter: c
c c : cee
ready: ready
yes: yes
what no mark: what
three h: uhhh
left: left
right: right
write: right
middle: middle
metal: middle
wait: wait
press: press
five letters: uh huh
four letters: uh uh
what mark: what?
done: done
next: next
hold: hold
sure: sure
like: like
mike: like
might: like
white: like
light: like
```

### Needy knobs

```
knobs <0/1 of LEDs> - LEDs of bottom left 3 then upper right 3
```

Example:

```
    Up

<   .   >

    v

0 1 0 1 0 1
1 1 1 0 0 1
```

```
knobs 1 1 1 1 0 1
```

### Password

Not implemented...yet.
