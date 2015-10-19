# Bombly - Keep Talking and Nobody Explodes Robot

## Product

[![Hardcore Bomb Video](http://img.youtube.com/vi/ydQEb6zyAuE/0.jpg)](http://www.youtube.com/watch?v=ydQEb6zyAuE)

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

I believe dragonfly should work with Dragon NaturallySpeaking, however, I did not use it.

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
simple wires <wires> - Where wires is in (red, blue, yellow, black, white)
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
4 Wires:
Red
Blue with Star
Red/Blue with Light/Star
No attributes
```

```
complex wires red next blue star next light red blue star next blank
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

Indicator - (2, 1)
Start     - (1, 3)
Finish    - (4, 4)
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
wire sequence blue apple red bravo black charlie
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

![column1](https://raw.githubusercontent.com/thebarbershopper/bombly/master/images/column1.png)

```
tennis, a, l, lightning, kitty, h, c
```

![column2](https://raw.githubusercontent.com/thebarbershopper/bombly/master/images/column2.png)

```
e, tennis, c, o, star, h, question
```

![column3](https://raw.githubusercontent.com/thebarbershopper/bombly/master/images/column3.png)

```
copyright, butt, o, k, r, l, star
```

![column4](https://raw.githubusercontent.com/thebarbershopper/bombly/master/images/column4.png)

```
six, paragraph, b, kitty, k, question, smile
```

![column5](https://raw.githubusercontent.com/thebarbershopper/bombly/master/images/column5.png)

```
goblet, smile, b, c, paragraph, three, star
```

![column6](https://raw.githubusercontent.com/thebarbershopper/bombly/master/images/column6.png)

```
six, e, equals, smash, goblet, n, omega
```

### Who's on First

Now for the fun module. This is still a work in progress (check out the code for all of the cases)

```
words one <words> - Step 1 of Who's on First, lookup position
```

```
words two <words> - Step 2 of Who's on First, start giving words from lookup table
```

Below is the table of what spoken words coorelate to the words necessary to complete the challenge.

```
' ' - literally blank
blank - blank
c - c letter
c - see letter
cee - c c 
display - display
done - don
done - done
done - done
first - first
hold - hold
hold - hold
hold on - hold on two
lead - lead
lead - mead
led - L. E. D.
left - left
like - like
middle - middle
next - next
no - no
nothing - nothing
okay - OK
okay - okay
press - press
read - read
ready - ready
red - red short
reed - read too
right - right
right - write
says - says
see - c s 
sure - sure
their - e i r
there - e r e
they are - they are words
they're - they are marked
they're - they mark
u - you letter
uh huh - five letters
uh uh - four letters
uhhh - three h
ur - you are letters
wait - wait
what - what no mark
what? - what mark
yes - yes
yes - yes
you - you word
you are - you are words
you are - your words
you're - you are mark
you're - your mark
your - you're word
your - your word
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
