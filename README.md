These tools can be used to extract TIFF files and metadata from a legacy database called **Alchemy**, created by **Image Management Systems, Inc.**

A website advertising this software can still be [found here](https://www.imagemgt.com/alchemy.html) in all its crusty Web 1.0 glory.

This is part of a research project I'm doing with my academic advisor at [IUPUI](https://luddy.iupui.edu/). The goal is to preserve 900+ CD-ROMs of scanned nonprofit tax forms. 

Each CD-ROM stores the documents as a single gigantic binary file, which is actually countless TIFF files concatenated together. This tool separates them and also extracts relevant metadata as [JSON](https://en.wikipedia.org/wiki/JSON).

Eventually, the documents will be digitally preserved in the PDF-A format and displayed in a searchable database for use by the public and by researchers.

To view our presentation, [click here](https://hdl.handle.net/1805/37104). The description of the event can be found [here](https://clirevents2023.sched.com/event/1On64/w02-combo-unlocking-archives-email-preservation-legacy-database-rescue-and-digital-project-management).

## EDIT 12/11/24: Summary for anyone working on this project in the future

In the repository, the two main files are extract_tiffs.py and extract_metadata.py.

I tried to be very descriptive in my code, leaving plenty of comments describing what the lines of code do. 

`extract_tiffs.py` searches a given file for TIFF headers - this is a four-digit code that can be found at the start of every TIFF file. Using this, it can tell where the individual files begin and end. It uses this to slice the file up and dump the individual files in a folder for you to examine, redact any sensitive information, and archive. I was very happy with this script, and consider it to be complete.

`extract_metadata.py`, on the other hand, was pretty frustrating and the script I struggled with the most. Alchemy shows various fields of metadata in its UI, and this script attempts to locate that data and dump it to a JSON file, for archiving and for potential use as a finding aid in the future. Unfortunately, I was never able to pinpoint the way the data is stored - the first few CD-ROMS stored the data in the same way, so it was easy for me write the script and dump it. However, other CD-ROMs in the collection store the data in a completely different order, resulting in my code breaking and either data being saved in the wrong order, or incorrectly, resulting in glitched text in the saved JSON file. It's been a while since I looked, but I seem to remember that some CD-ROMs didn't contain the same number of metadata fields. The script I wrote is built to look for EIN, Return Type, State, Submission Code, Submission Date, Tax Year, Taxpayer Name, Total Assets, and Zip Code, in that order.

It might be possible to reverse-engineer Alchemy itself to figure out what it's doing while it goes to get that data, parse it, and display it, or it might be simpler for someone to just examine the dumped TIFF files and write the data down manually.

`metadata_structure.py` is referenced by `extract_metadata.py` - it contains the expected structure of the data it looks for. It's separate from the latter for cleanliness's sake. There are two different versions of the structure, `recordtype` and `recordtype2` - this is leftover from my attempts at dumping the metadata that's stored in a different order. The first version works on the first group of CDs in the collection.

`paths.py` is a list of paths, referenced by both scripts. This is how you point the scripts at the files you want them to process. I intended for it to be possible to have a long list of paths to every CD-ROM in the collection, and to run it on everything at once, churning through each CD-ROM in turn. Realistically, though, I ended up putting a new path in and running the script one at a time.

The `Research` files in Markdown format are the notes I took while I was writing the scripts. I'm not sure if they'd be useful outside of understanding my thought process at the time.

If you're a programmer being brought on to work on this project, I'd love to be in touch! Since I finished my grad degree, I can't work as a student employee anymore, so I can't continue work on this project. I'm very interested in any new findings.
