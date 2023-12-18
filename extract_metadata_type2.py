import jsonlines
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
    # Validate that this is an Alchemy metadata file
    offset = 0x2000
    header = get_text(data, offset, offset + 3)
    if (header != "ALW"):
        raise ValueError("This doesn't look like an Alchemy metadata file. 'ALW' not found at 0x2000")

    start_code = '0000002300' # Every record starts with these hex numbers. MIGHT NOT ALWAYS BE THE SAME!
    metadata_offsets = get_list_of_offsets(data, start_code)
    records = [] # This will store the extracted data, and will eventually be saved to a file
    
    index = 0 #TODO: Figure out how to make this more Pythonic... You're not supposed to use indices like this
    #Extract each record present
    for start_offset in metadata_offsets:
        single_record = [] # This will store a single record. I think doing it like this will make saving the CSV file easier
        try:
            next_offset = metadata_offsets[index + 1]
        except IndexError as e: # This will happen after processing the last offset.
            break # Breaking out of the loop here is not best practice, but I want to get this working. 
        offset = start_offset + 5 # Keep track of where we are, starting at the start of the current record. +5 skips to the first number of the EIN
        
        while offset < next_offset: # Stop if it starts to bleed into the next record
            current_string_length = data[offset] # Save this number, which is how many characters the string we're about to save has
            offset = offset + 1 # Now that we have the length, seek to the first character in the string
            end_offset = offset + current_string_length - 1 # Use the number we just saved to work out where the end of the string is

            result = get_text(data, offset, end_offset) # Interpret the data between the two offsets as text, and save it!
            single_record.append(result)
            offset = end_offset + 5 # Skip ahead to the next field

        records.append(single_record)
        index = index + 1 # Again, this needs to be more Pythonic.

    return records

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
        writer = csv.writer(filename_to_use)
        for record in records:
            print(record)
            writer.writerow(record)
    
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