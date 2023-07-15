Research on 7/14/23

## `PFAL000S.NDX`
Appears to contain data but no readable text. Surprisingly long, so it might be worth decoding if time allows.

## `PFLA000S.RID`
This file is very short compared to everything else. It appears to have data, but it's also unreadable.

## `PFAL000S.ROB`
Contains a Lookup Table of a bunch of commonly-used English words in alphabetical order. Might have to do with Alchemy's OCR support, which as far as I know is unused in all of these. 

## `PFAL00S.TID`
More unreadable data. It appears to be a bunch of 00s, and numbers and letters in sequence (i.e. 0, 1, 2, 3, 4, etc.) My guess is that it's a definition of which letters and numbers could have been used in the OCR, if whoever scanned these documents had chosen to use it. 

## `PFAL000S.TOB`
This contains a bunch of filepaths! But they're not useful, as all of these files are grouped together in the .DAT file and not actually visible to us. One of the paths is `\\netraid lx pro\ext_pf\00003201.001\00003201.001`

## `00001.DAT`
I think this is the binary file where all the image files are clumped together into one big blob of data. There's some human-readible text here: a filepath, which is different for each file (e.g "C:\TEMP\nna0071") and `Oi/GFS, writer v00.06.00P, (c) Wang Labs, Inc. 1990, 1991`. This string appears many times throughout the DAT file. From Googling this phrase, I can that it's a field of metadata present in each TIFF file meant to describe what software was used to generate it. Wang Labs must have made some image processing code at some point in the past, which then got used in Alchemy. 