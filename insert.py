import os
import struct
import hashlib
from datetime import datetime
from collections import namedtuple

def insert(case_id, item_id, file_path):

    print_case_count = 0

    success = ''

    fp = open(file_path, 'rb')

    block_head_format = struct.Struct('20s d 16s I 11s I')

    # Check how many string characters for Case-ID (16 or more) !!!
    # Check for same Case_ID and same Item_ID or Just same Item_ID !!!

    block_head = namedtuple('Block_Head', 'hash timestamp case_id item_id state length')
    block_data = namedtuple('Block_Data', 'data')

    prev_hash = ''
    prev_id = []

    while True:

        try:
            head_content = fp.read(block_head_format.size)
            curr_block_head = block_head._make(block_head_format.unpack(head_content))
            prev_id.append(curr_block_head.item_id)
            block_data_format = struct.Struct(str(curr_block_head.length)+'s')
            data_content = fp.read(curr_block_head.length)
            curr_block_data = block_data._make(block_data_format.unpack(data_content))
            
            prev_hash = hashlib.sha1(head_content+data_content).digest()

        except:
            # print("Last Block Recorded")
            break


    for i in item_id:
    
        if int(i) in prev_id:
            # print("----Nope----")
            continue

        if not print_case_count:
            print("Case: ", case_id)
            print_case_count += 1

        now = datetime.now()
        
        timestamp = datetime.timestamp(now)
        head_values = (prev_hash, timestamp, str.encode(case_id), int(i), str.encode("CHECKEDIN"), 35)
        data_value = (str.encode("Add Item: ") + str.encode(i) + str.encode(" to Case: ") + str.encode(case_id))
        block_data_format = struct.Struct('35s')
        packed_head_values = block_head_format.pack(*head_values)
        packed_data_values = block_data_format.pack(data_value)
        curr_block_head = block_head._make(block_head_format.unpack(packed_head_values))
        curr_block_data = block_data._make(block_data_format.unpack(packed_data_values))

        prev_hash = hashlib.sha1(packed_head_values+packed_data_values).digest()

        # print(curr_block_head)
        # print(curr_block_data)

        fp = open(file_path, 'ab')
        fp.write(packed_head_values)
        fp.write(packed_data_values)
        fp.close()


        print("Added item:", i)
        print("\tStatus: CHECKEDIN")
        print("\tTime of action:", now.strftime(
            '%Y-%m-%dT%H:%M:%S.%f') + 'Z')

        success = True

    if success:
        return True
    else:
        return False