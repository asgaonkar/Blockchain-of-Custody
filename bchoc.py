import argparse

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

print(action)
print(arguements)
