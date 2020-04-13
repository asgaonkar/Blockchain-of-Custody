import os
import sys
import struct
import hashlib
import uuid
from error import *
from datetime import datetime
from collections import namedtuple

# Custom
from display_trial import display


def verify(file_path):


    block_head_format = struct.Struct('20s d 16s I 11s I')
    block_head = namedtuple('Block_Head', 'hash timestamp case_id item_id state length')
    block_data = namedtuple('Block_Data', 'data')
    blocks=[]
    hashes = []

    blocks_dict = {}

    fp = open(file_path, 'rb')

    unsuccess = False

    count = 0

    while True:

        try:
            try:
                head_content = fp.read(block_head_format.size)
            except:
                # Normal Break
                break
            curr_block_head = block_head._make(block_head_format.unpack(head_content))
            block_data_format = struct.Struct(str(curr_block_head.length) + 's')
            data_content = fp.read(curr_block_head.length)
            curr_block_data = block_data._make(block_data_format.unpack(data_content))
            # prev_hash = hashlib.sha1(head_content + data_content).digest()
            blocks.append((curr_block_head,curr_block_data))
            hashes.append(curr_block_head.hash)


            if str(uuid.UUID(bytes=curr_block_head.case_id)) in blocks_dict:
                
                
                if curr_block_head.item_id in blocks_dict[str(uuid.UUID(bytes=curr_block_head.case_id))].keys():
                    
                    # If an item is there    
                    print("--- Item Present. \nOld State:",blocks_dict[str(uuid.UUID(bytes=curr_block_head.case_id))][curr_block_head.item_id], "\nNew State:", (curr_block_head.state.decode()).rstrip('\x00'))



                    # Check Previous State
                    prev_state = blocks_dict[str(uuid.UUID(bytes=curr_block_head.case_id))][curr_block_head.item_id]
                    curr_state = (curr_block_head.state.decode()).rstrip('\x00')

                    if curr_state == "CHECKEDIN":
                        if prev_state != "CHECKEDOUT":
                            unsuccess = True
                            break    
                    elif curr_state == "CHECKEDOUT":
                        if prev_state != "CHECKEDIN":
                            unsuccess = True
                            break
                    elif curr_state in ["RELEASED", "DISPOSED", "DESTROYED"]:
                        if prev_state != "CHECKEDIN":
                            unsuccess = True
                            break
                        if curr_state == "RELEASED":
                            # Look for Owner Info
                            if not curr_block_head.length:
                                unsuccess = True
                                break
                    blocks_dict[str(uuid.UUID(bytes=curr_block_head.case_id))][curr_block_head.item_id] = (curr_block_head.state.decode()).rstrip('\x00')


                    pass
                else:

                    print("--- New Item . \nState: (Should be CHECKEDIN)",(curr_block_head.state.decode()).rstrip('\x00'), " ***: ",(curr_block_head.state.decode()).rstrip('\x00') in ["RELEASED", "DISPOSED", "DESTROYED"])

                    # Check for Remove before adding
                    if (curr_block_head.state.decode()).rstrip('\x00') in ["RELEASED", "DISPOSED", "DESTROYED"]:
                        unsuccess = True
                        break
                        

                    # Add new item to case
                    blocks_dict[str(uuid.UUID(bytes=curr_block_head.case_id))][curr_block_head.item_id] = (curr_block_head.state.decode()).rstrip('\x00')
                    

            else:
                
                print("--- 1st Item of Case. \nState: (Should be CHECKEDIN)",(curr_block_head.state.decode()).rstrip('\x00'), " ***: ",(curr_block_head.state.decode()).rstrip('\x00') in ["RELEASED", "DISPOSED", "DESTROYED"])

                # Check for Remove before adding
                if (curr_block_head.state.decode()).rstrip('\x00') in ["RELEASED", "DISPOSED", "DESTROYED"]:
                    unsuccess = True
                    break

                blocks_dict[str(uuid.UUID(bytes=curr_block_head.case_id))] = {}
                blocks_dict[str(uuid.UUID(bytes=curr_block_head.case_id))][curr_block_head.item_id] = (curr_block_head.state.decode()).rstrip('\x00')

            print(blocks_dict)
            count+=1
        except:

            if not count:
                # Invalid Initial Block
                unsuccess = True
                break
            
            # Invalid Block
            unsuccess = True
    
    fp.close()
    
    if unsuccess:
        Invalid_Chain()

    if len(hashes) != len(set(hashes)):
        Duplicate_Hashes()

    print(blocks)