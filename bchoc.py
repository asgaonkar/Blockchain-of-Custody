import os
import struct
import argparse
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
        initialise = initiate(file_path)

        if initialise:
            raise error.Initial_Block_Error
    else:
        verified = verify(file_path)
