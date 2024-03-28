# -*- coding: utf-8 -*-
from all_tools_on_blockchain.argparse import *
from all_tools_on_blockchain.read import *
from web3 import Web3


def read_contract():
    parser_instance = read_argparse()
    try:
        web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/c77b93a34625489b8a04b548c96369bf'))
        input_address = parser_instance.inputAddress
        read_slot = parser_instance.slot
        if input_address == '' and read_slot == '':
            print('Please input address or read slot')
            return
        else:
            if read_slot != '':
                read_contract_storage_data(input_address, read_slot)
            elif input_address != '':
                read_contract_onchain_public_view_data(input_address, web3)
    except Exception as e:
        print(e)


# def main():
#     parser_instance = main_argparse()
#     try:
#         file = parser_instance.inputFile
#         is_rc = parser_instance.readConstant
#         string_data = parser_instance.string
#         config = parser_instance.config
#         if is_rc:
#             return_data = get_bytes32_constant_from_contract(string_data, file)
#             for item in return_data:
#                 print(f"{item['hash']}\t{item['string']}")
#     except Exception as e:
#         print(e)

