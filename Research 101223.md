This is research I did after discovering that the extracted metadata started being garbled after reaching Mss005_0020. 

# Observations of Mss005_0020 and the next few files:
The header (located at 0x2000) always starts with ALW and ends with 00 0A (data in between those things is always different though)

EIN numbers are always nine numbers long. Thanks, IRS!

## End codes after the EIN:
**(starting at Mss005_0020)**
```
[00 07 01 24 00 07]
[00 07 01 DE 00 07]
[00 07 01 DE 00 07]
[00 07 01 DE 00 07]
```


## End codes after the year:
```
[00 07 01 25 00 1A]
[00 07 01 DF 00 0E]
[00 07 01 DF 00 1A]
[00 07 01 DF 00 1C]
```

It seems Mss005_0020 has a variation, but all of them use [00 07 01] at the beginning. The end codes are always six bytes long, so it'll be possible to search for [00 07 01] (or maybe get the next three digits after the EIN and store it on the fly in case it changes again??) and then add 6 to the offset.

## End codes after the nonprofit name:
```
[00 07 01 26 00 03]
[00 07 01 E0 00 03]
[00 07 01 E0 00 03]
[00 07 01 E0 00 03]
```

WAIT A MINUTE. There's a 24, 25, 26 pattern in Mss005_0020, but not in the next few files. It seems to be using the fourth byte of the end code as an index number? Or something that increments. It's weird that this only happens for one file and not all of them. (Then again, it's also weird that there's this stupid inconsistency/sudden shift in the order in which all the fields are stored...)

# Comparison with Mss005_0001, the one I based my initial extraction code on
Header is still at 0x2000, starting with "ALW" and ending with [00 0A].

## End code after the EIN:
```[00 07 01 24 00 06]```
## End code after the return type:
```[00 07 01 25 00 03]```
## End code after the state:
```[00 07 01 26 00 02]```

As you can see, the order of the fields is completely different in the first 20 CD-ROMs. This is what caused the extracted metadata to be garbled once I hit number 20...
It seems to also be incrementing the fourth byte (or at least in this file), and the first three bytes of the end code are [00 07 01]. At least that's dependable...

I think the plan forward is to make a CSV dumper instead of a JSON dumper. I think I want to keep the JSON files for the ones where it worked, though.

# Brainstorming:
- Load the file into memory
- Seek to 0x2000 and search for the [00 0A].
- Seek to the byte directly after that. This will be where the start of the EIN is.

LOOP:
- Get the offset of the next [00]. This is where the current feild ends.
- Start grabbing text, letter by letter, stopping at the end offset we just got.
- Save the text in a list of strings named "result".
- Get the offset of the next [00 07 01], and add 6 to it (or would it be 7?). This is where the next field starts. 
  - If there isn't one to be found, exit the program. This is the end of the file. If there is one, seek to it!

END LOOP

- Create a new text file called unsorted_metadata.txt
- Assuming each record is the same number of fields (oh god), sort the contents of the list of strings to the file, 
- Maybe check each one to see if it's an EIN, and if it is, add a newline. (I'll have to double-check that the CSV opens in Excel...)
- Done!