from secrets import list_of_files
from pathlib import Path

def main():
    print("Ta-da!")
########################################################################

# Now that everything's defined, run the dang thing!
if __name__ == "__main__":
    main()

# NOTES
# It might be possible to use PFAL000S.TOB to get the name
# of each record, and each filename as it appears when you
# open it in Alchemy. However, the Fall semester is about
# to start and I need to make quicker progress. So I'm going
# to locate the start of each TIFF header and dump the files
# that way.

# Program logic:
# Load the 00001.PRO file as a byte array
# Make a list of offsets of each instance of [49 49 2A 00]
# Dump from [offset] to [next offset]
# If it's the last file, dump from [offset] to the end of
# the file
