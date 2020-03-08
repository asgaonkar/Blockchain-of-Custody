import os
import struct
import argparse
from datetime import datetime
from collections import namedtuple

# Import modules
import error
from initiate import initiate
from verify import verify

#Declare arguements
parser = argparse.ArgumentParser()
parser.add_argument("action") # Action = ["add", "checkout", "checkin", "log", "remove", "init", "verify"]
parser.add_argument('-c') # Case ID
parser.add_argument('-i', action='append') # Item ID
parser.add_argument('-n') # Number of entries for log
parser.add_argument('-y') # Reason for removing
parser.add_argument('-o') # Owner Info
parser.add_argument('-r', action="store_true") # Reverse log
args = parser.parse_args()

action = args.action
arguements = {}


# file_path = os.getenv('BCHOC_FILE_PATH') # Read using environment variable in Gradescope
file_path = "chain"

block_head_format = struct.Struct('20s d 16s I 11s I')
block_head = namedtuple('Block_Head', 'hash timestamp case_id item_id state length')
block_data = namedtuple('Block_Data', 'data')

# Initialise necessary arguements
if action not in ["init", "verify"]:
    
    if action == "add":
        arguements["case_id"] = args.c
        arguements["item_id"] = args.i
    elif action == "checkout" or action == "checkin":
        arguements["item_id"] = args.i
    elif action == "log":
        arguements["reverse"] = args.r
        arguements["number"] = args.n
        arguements["case_id"] = args.c
        arguements["item_id"] = args.i
    else:
        arguements["item_id"] = args.i
        arguements["reason"] = args.y
        arguements["owner"] = args.o
else:
    if action == "init":
        to_initiate = initiate(file_path)

        if not to_initiate:
            print("Blockchain file found with INITIAL block.")
            raise error.Initial_Block_Error
        else:
            #Initiate a NULL Block
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            value = (str.encode(""), timestamp, str.encode(""), 0, str.encode("INITIAL"), 14)
            packed_values = block_head_format.pack(*value)
            curr_block_head = block_head._make(block_head_format.unpack(packed_values))
            print(packed_values)
            print(curr_block_head)    
      
    else:
        count = 0 # Number of Transactions
        block_chain_state = "CLEAN" # CLEAN or ERROR 
        verified = verify(file_path)

print(arguements)
