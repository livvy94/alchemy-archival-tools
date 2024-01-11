from metadata_structure import record
from paths import list_of_metadata_files
from pathlib import Path
import csv

def main():
    for filename in list_of_metadata_files:
        cdrom_name = get_cdrom_name(filename)
        with open(filename, 'rb') as f:
            data = f.read() # This "data" variable is where the entire file's contents is going to be stored

        records = extract(data)
        save_csv_file(records, cdrom_name)

########################################################################

def extract(data):
    extracted_text = []

    thousands = thousands_generator() # This returns 0x2000, 0x4000, etc.
    thousands_index = 1

    # Because there's an "ALW" header every 0x2000 bytes, even in the middle of a record,
    # we're having to work through the file in chunks of that size
    for thousand in thousands:
        offset = thousand
        if offset > len(data): # Stop if the offset is greater than how big the file is
            print("End of file reached.")
            break

        # Check for the ALW header
        header = get_text(data, offset, offset + 3)
        if (header != "ALW"):
            raise ValueError(f"This doesn't look like an Alchemy metadata file. 'ALW' not found at {hex(offset)}")

        #Navigate to where the first field will be
        offset + offset + 17

        while offset < thousands[thousands_index + 1]:
            #TODO: extract the text, using the length codes
            print("foo")

#############################################################################################################################
# Helper methods!

def get_cdrom_name(filename):
    cdrom_name = Path(filename).resolve().parents[2].name # This takes the whole filepath and returns just the name of the folder.

    # The next few lines get rid of weird characters that might cause bugs if they're in the folder name
    special_characters = '\\/*?:;"<>|'
    result = ""
    for char in cdrom_name:
        if char not in special_characters:
            result += char

    return result

def get_list_of_offsets(data, header_hex):
    start_code = convert_to_bytes(header_hex) # Convert it to a byte array so we can use data.find with it

    offset_list = [] # Find the location of each time these bytes show up in the given file
    pos = data.find(start_code) # Find the first instance of the start code

    while pos != -1: # Loop until it can't find any more
      offset_list.append(pos)
      pos = data.find(start_code, pos + 1) # Look for another one!

    return offset_list

def get_text(data, start_offset, end_offset):
    return data[start_offset:end_offset].decode('unicode_escape')

def convert_to_bytes(input):
    return bytes.fromhex(input) # Converts a string that contains a hex number into that number. Simple but this looks cleaner.

def save_csv_file(records, directory_name):
    cwd = Path.cwd()
    filepath_to_use = cwd / "Extracted Data" / directory_name
    filename_to_use = filepath_to_use / "unsorted_metadata.csv"

    if not filepath_to_use.exists():
        filepath_to_use.mkdir(parents=True)

    print(f"Extracted {filename_to_use}")
    with open(filename_to_use, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for record in records:
            print(record)
            writer.writerow(record)

def thousands_generator():
    thousands = []
    current_number = 2
    for _ in range(40): # 40 is a pretty high number. There probably won't be any metadata files huger than that.
        thousands.append(0x1000 * current_number)
        current_number += 2
    return thousands

# def save_json_file(records, directory_name):
#     cwd = Path.cwd()
#     filepath_to_use = cwd / "Extracted Data" / directory_name
#     filename_to_use = filepath_to_use / "metadata.jsonl"

#     if not filepath_to_use.exists():
#         filepath_to_use.mkdir(parents=True)

#     print(f"Extracted {filename_to_use}")
#     with jsonlines.open(filename_to_use, mode='w') as writer:
#         for record in records:
#             writer.write(record.__dict__)

# Now that everything's defined, run the dang thing!
if __name__ == "__main__":
    main()

# TODO: Generally clean up the code.

# TODO: Remove convert_to_bytes from get_list_of_offsets, it has no reason to be there.
#       The data should already be bytes when passed into it.

# 12/18/23
# I have discovered that every 2000 bytes, there is another "ALW" header.
# This is always right smack dab in the middle of a record, and when this happens it throws off the record it's currently dumping.
# It doesn't throw off the entire dump, thankfully! But this is still a big obstacle.
# TODO: Make a method that generates a list, 2000, 4000, 6000, etc. - DONE!
# Make an index number for the current one you're in
# Sanity check - is the current offset greater than the filesize? If so, break.
# Sanity check - are the first three bytes of the current block "ALW"? If not, break. 
# After dumping each string, run a check against the next offset and the upcoming index.
#    If you haven't gone past it yet, carry on as usual.
#    If you have, make the current offset to that thousand, plus 17 (this is where the next field will be!) and carry on.



