from paths import list_of_TIFF_blobs
from pathlib import Path

def main():
    for filename in list_of_TIFF_blobs:
        cdrom_name = get_cdrom_name(filename) # This should be identical to the folder name extract_metadata.py gets

        with open(filename, 'rb') as f:
            data = f.read() # This "data" variable is where the entire file's contents is going to be stored

        all_TIFFs = extract(data)
        save_tiff_files(all_TIFFs, cdrom_name)

def save_tiff_files(all_TIFFs, output_folder):
    cwd = Path.cwd()
    filepath_to_use = cwd / "Extracted Data" / output_folder

    if not filepath_to_use.exists():
        filepath_to_use.mkdir(parents=True)

    for index, tiff_data in enumerate(all_TIFFs):
        tiff_filename = f"{filepath_to_use}/page{index + 1}.tiff"
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
        separated_TIFF_files.append(data[offset:second_offset])  # Slice out the individual file

    return separated_TIFF_files

########################################################################

# Helper methods!
def get_cdrom_name(filename):
    cdrom_name = Path(filename).resolve().parents[3].name # This takes the whole filepath and returns just the name of the folder.
    folder_name = Path(filename).resolve().parents[2].name
    # The next few lines get rid of weird characters that might cause bugs if they're in the folder name
    special_characters = '\\/*?:;"<>|'
    result = ""
    for char in folder_name:
        if char not in special_characters:
            result += char

    return cdrom_name + "\\" + result

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
# different for each TIFF file, I'm leaving it out of the search.

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
