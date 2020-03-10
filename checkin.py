import os
import struct
import hashlib
from datetime import datetime
from collections import namedtuple


def checkin(item_id, file_path):

    success = True
    state = ''
    prev_hash = b''
    case_id = ''

    block_head_format = struct.Struct('20s d 16s I 11s I')
    block_head = namedtuple(
        'Block_Head', 'hash timestamp case_id item_id state length')
    block_data = namedtuple('Block_Data', 'data')

    fp = open(file_path, 'rb')

    while True:

        try:
            head_content = fp.read(block_head_format.size)
            curr_block_head = block_head._make(
                block_head_format.unpack(head_content))
            block_data_format = struct.Struct(str(curr_block_head.length)+'s')
            data_content = fp.read(curr_block_head.length)
            curr_block_data = block_data._make(
                block_data_format.unpack(data_content))

            prev_hash = hashlib.sha1(head_content+data_content).digest()

            if int(item_id[0]) == curr_block_head.item_id:
                case_id = curr_block_head.case_id
                state = curr_block_head.state
        except:
            break

    fp.close()

    if state.decode('utf-8').rstrip('\x00') == "CHECKEDOUT":

        now = datetime.now()

        timestamp = datetime.timestamp(now)
        head_values = (prev_hash, timestamp, case_id, int(
            item_id[0]), str.encode("CHECKEDIN"), 35)
        data_value = (str.encode("Checkin Item: ") + str.encode(item_id[0]) +
                      str.encode(" to Case: ") + case_id)
        block_data_format = struct.Struct('35s')
        packed_head_values = block_head_format.pack(*head_values)
        packed_data_values = block_data_format.pack(data_value)
        curr_block_head = block_head._make(
            block_head_format.unpack(packed_head_values))
        curr_block_data = block_data._make(
            block_data_format.unpack(packed_data_values))

        # print(curr_block_head, curr_block_data)

        fp = open(file_path, 'ab')
        fp.write(packed_head_values)
        fp.write(packed_data_values)
        fp.close()

        print("Case:", case_id.decode('utf-8'))
        print("Checked in item:", item_id[0])
        print("\tStatus:", "CHECKEDIN")
        print("\tTime of action:", now.strftime(
            '%Y-%m-%dT%H:%M:%S.%f') + 'Z')

        success = True

    elif state.decode('utf-8').rstrip('\x00'):
        # Not removed due to incorrect state
        # Error: Cannot check out a checked out item. Must check it in first.
        # print("Error")
        pass
    else:
        # Item ID not found
        pass

    if success:
        return True
    else:
        return False