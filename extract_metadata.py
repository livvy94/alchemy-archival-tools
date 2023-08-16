import jsonlines
from DocumentProfile import DocumentProfile
from secrets import list_of_metadata_files
from pathlib import Path

def main():
    for filename in list_of_metadata_files:
        cdrom_name = get_cdrom_name(filename)
        print(cdrom_name)
        with open(filename, 'rb') as f:
            data = f.read() # This "data" variable is where the entire file's contents is going to be stored

        records = extract(data)
        save_json_file(records, cdrom_name)

########################################################################

def extract(data):
    start_code = '0023000A' # Every record starts with these hex numbers
    metadata_offsets = get_list_of_offsets(data, start_code)
    
    # Extract each record present
    index = 0 # Keep track of how many records we've looked at
    records = [] # This will contain instances of DocumentProfile
    for start_offset in metadata_offsets: # Loop through each record
        result = []
        current_offset = start_offset + len(start_code) # Keep track of where we are, starting at the start of the current record
        
        # The EIN is the first field in each record. Get it and add it to the result
        ein_end_offset = data.find(00, current_offset + 1)
        ein = get_text(data, current_offset, ein_end_offset)
        result.append(ein)

        if index >= len(metadata_offsets):
            break # Skip the rest of this if there aren't any more records to read

        for x in range(8): # Each record has eight fields
            current_offset = data.find(00, current_offset) + 6
            next_offset = data.find(00, current_offset + 1) # This is where we'll be stopping. The +1 is just to get it to find the next one
            line = get_text(data, current_offset, next_offset) # Get the text!
            result.append(line)
        
        current_offset = data.find(convert_to_bytes(start_code), (current_offset + 1)) # Set the current offset to the start of the next record.

        temp = DocumentProfile(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8])
        records.append(temp)
        index = index + 1
    return records


# Helper methods!
def get_cdrom_name(filename):
    return Path(filename).resolve().parents[2].name # This takes the whole filepath and returns just the name of the folder.

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

def save_json_file(records, directory_name):
    filename_to_use = f"{directory_name}/metadata.jsonl"
    print(f"Saving {filename_to_use}...")
    with jsonlines.open(filename_to_use, mode='w') as writer:
        for record in records:
            writer.write(record.__dict__)

# Now that everything's defined, run the dang thing!
if __name__ == "__main__":
    main()

# TODO: Make it so you can just give it the folder name, like
#       "Mss005_0001". It seems there are variations in the names of the
#       subfolders... There's "PFAL000S", "PFFL0029", "PFMS001G",
#       "PA_2000_"... And not all of them start with "P", so we can't narrow
#       it down by that...
#       Some of them don't even have all the Alchemy EXEs and are just
#       a single data folder...
#       Worst-case scenario, whoever runs this to extract the data will need to go
#       into each CD and find the exact path of the .PRO file.

# TODO: Generally clean up the code.

# TODO: Download more disks and figure out the folder structure so users can specify
#       the location of the disk and not have to hunt down the specific file

# TODO: Lines 19-27 should be a helper method that returns all_start_offsets.
#       It is also used in extract_tiffs.py