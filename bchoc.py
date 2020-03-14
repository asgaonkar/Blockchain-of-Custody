import os
import uuid
import struct
import hashlib
import argparse
from datetime import datetime
from collections import namedtuple

# Import modules
from error import *
from initiate import initiate
from insert import insert
from remove import remove
from checkin import checkin
from checkout import checkout
from display_trial import display

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


file_path = os.getenv('BCHOC_FILE_PATH') # Read using environment variable in Gradescope
# file_path = "chain"

block_head_format = struct.Struct('20s d 16s I 11s I')
block_head = namedtuple('Block_Head', 'hash timestamp case_id item_id state length')
block_data = namedtuple('Block_Data', 'data')
prev_hash = b''

# Initialise necessary arguements
if action not in ["init", "verify"]:
    
    if action == "add":
        arguements["case_id"] = args.c
        arguements["item_id"] = args.i
        insert(arguements["case_id"], arguements["item_id"], file_path)
    elif action == "checkout" or action == "checkin":
        arguements["item_id"] = args.i
        if action == "checkout":
            checkout(arguements["item_id"], file_path)
        else:
            checkin(arguements["item_id"], file_path)
    elif action == "log":
        arguements["reverse"] = args.r
        arguements["number"] = args.n
        arguements["case_id"] = args.c
        arguements["item_id"] = args.i
    else:
        arguements["item_id"] = args.i
        arguements["reason"] = args.y
        arguements["owner"] = args.o
        remove(arguements["item_id"],
               arguements["reason"], arguements["owner"], file_path)

else:
    if action == "init":
        to_initiate = initiate(file_path)

        if not to_initiate:
            print("Blockchain file found with INITIAL block.")
            Initial_Block_Error()
        else:
            #Initiate a NULL Block
            
            trial = '65cc391d-6568-4dcc-a3f1-86a2f04140f3'
            x_trial = uuid.UUID(trial)

            now = datetime.now()
            timestamp = datetime.timestamp(now)
            head_values = (str.encode(""), timestamp, str.encode(""), 0, str.encode("INITIAL"), 14)
            data_value = (str.encode("Initial block"))
            block_data_format = struct.Struct('14s')
            packed_head_values = block_head_format.pack(*head_values)
            packed_data_values = block_data_format.pack(data_value)
            curr_block_head = block_head._make(block_head_format.unpack(packed_head_values))
            curr_block_data = block_data._make(block_data_format.unpack(packed_data_values))

            # print(curr_block_head)
            # print(curr_block_data)

            fp = open(file_path, 'wb')
            fp.write(packed_head_values)
            fp.write(packed_data_values)
            fp.close()

            #Initiated
            prev_hash = hashlib.sha1(packed_head_values+packed_data_values).digest()
            print("Blockchain file not found. Created INITIAL block.")
      
    else:
        count = 0 # Number of Transactions
        block_chain_state = "CLEAN" # CLEAN or ERROR 

# print(arguements)

# display(file_path) #For trial and error purpose

sys.exit(0)