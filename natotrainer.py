import random, string

nato = {
	"a": "alpha",
	"b": "bravo",
	"c": "charlie",
	"d": "delta",
	"e": "echo",
	"f": "foxtrot",
	"g": "golf",
	"h": "hotel",
	"i": "india",
	"j": "juliet",
	"k": "kilo",
	"l": "lima",
	"m": "mike",
	"n": "november",
	"o": "oscar",
	"p": "papa",
	"q": "quebec",
	"r": "romeo",
	"s": "sierra",
	"t": "tango",
	"u": "uniform",
	"v": "victor",
	"w": "whiskey",
	"x": "x-ray",
	"y": "yankee",
	"z": "zulu",
	"0": "zero",
	"1": "one",
	"2": "two",
	"3": "three",
	"4": "four",
	"5": "five",
	"6": "six",
	"7": "seven",
	"8": "eight",
	"9": "niner",
}

thingies = "abcdefghijklmnopqrstuvwxyz0123456789"

while True:
    str = ""
    for i in range(0, random.randint(3, 5)):
        str += random.choice(thingies)
        
    print (str.upper())
    input()
    
    out = ""
    for i in str:
        out += nato[i] + " "
        
    print (out.upper())
    input ()
