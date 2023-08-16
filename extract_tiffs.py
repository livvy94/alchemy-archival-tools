import os
from secrets import list_of_TIFF_blobs
from pathlib import Path

def main():
    for filename in list_of_TIFF_blobs:
        cdrom_name = get_cdrom_name(filename) # This should be identical to the folder name extract_metadata.py gets

        with open(filename, 'rb') as f:
            data = f.read() # This "data" variable is where the entire file's contents is going to be stored

        all_TIFFs = extract(data)
        save_tiff_files(all_TIFFs, cdrom_name)

def save_tiff_files(all_TIFFs, output_folder):
    os.makedirs(output_folder, exist_ok=True) # The folder we're saving the TIFFs to
    for index, tiff_data in enumerate(all_TIFFs):
        tiff_filename = f"{output_folder}/page{index + 1}.tiff"
        with open(tiff_filename, 'wb') as tiff_file:
            tiff_file.write(tiff_data) # Save the file!
        print(f"Extracted {tiff_filename}")


def extract(data):
    separated_TIFF_files = []
    TIFF_offsets = get_list_of_offsets(data, '49492A00')

    for index, offset in enumerate(TIFF_offsets):
        # The next line figures out where the end of the current file is.
        # If this is in the middle of the list, it's just the next offset.
        # If we're at the end of the list, though, we can't do that - index + 1 doesn't exist.
        # To make it work, we can just use the length of the file itself as the last offset.
        second_offset = TIFF_offsets[index + 1] if index + 1 < len(TIFF_offsets) else len(data)
        print(f"{offset} to {second_offset}")  # debug, delete this line
        separated_TIFF_files.append(data[offset:second_offset])  # Slice out the individual file

    return separated_TIFF_files

########################################################################

# Helper methods!
def get_cdrom_name(filename):
    return Path(filename).resolve().parents[2].name # This takes the whole filepath and returns just the name of the folder.

def convert_to_bytes(input):
    return bytes.fromhex(input) # Converts a string that contains a hex number into that number. Simple but this looks cleaner.

def get_list_of_offsets(data, header_hex):
    start_code = convert_to_bytes(header_hex) # Convert it to a byte array so we can use data.find with it

    offset_list = [] # Find the location of each time these bytes show up in the given file
    pos = data.find(start_code) # Find the first instance of the start code

    while pos != -1: # Loop until it can't find any more
      offset_list.append(pos)
      pos = data.find(start_code, pos + 1) # Look for another one!

    return offset_list



# Now that everything's defined, run the dang thing!
if __name__ == "__main__":
    main()

# NOTES
# Here's an example of someone doing this sort of thing in a different
# programming language:
# https://superuser.com/questions/405449/split-concatenated-tiff-file
# And here's a useful page linked in one of the answers here:
# https://www.fileformat.info/format/tiff/corion.htm

# The tiff header is [49 49 2A 00]
# In ASCII, [49 49] is II. This indicates that the TIFF file is Intel byte-order.
# Other options include MM, which indicates Motorola byte-order. For the purposes
# of this project, I'm assuming all of them start with II.
# The [2A 00] is hex for the number 42, chosen for its deep philosophical value.
# Next in the header, the offset of the first image directory. Since this is
# different for each file, I'm not putting anything in for it when searching
# through the file.

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

# TODO: Put copied and pasted helper methods into a common place?
