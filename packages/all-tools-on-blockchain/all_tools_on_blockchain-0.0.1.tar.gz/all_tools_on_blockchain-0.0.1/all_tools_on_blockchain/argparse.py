import argparse


# def main_argparse():
#     main_parser = argparse.ArgumentParser(description='All-in-one toolset for blockchain.')
#     main_parser.add_argument('--rc', action='store_true', dest='readConstant',
#                         help='Read the bytes type constant in the contract.')
#     main_parser.add_argument('-i', default='', dest='inputFile', help='Input file path and name.')
#     main_parser.add_argument('-s', default='', dest='string', help='Choose a string as input.')
#     main_parser.add_argument('--config', action='store_true', dest='config', help='See config.')
#     return main_parser.parse_args()


def read_argparse():
    read_parser = argparse.ArgumentParser(description='All-in-one toolset for blockchain.')
    read_parser.add_argument('-a', default='', dest='inputAddress', help='Input contract address.')
    read_parser.add_argument('-s', default='', dest='slot', help='Input slot to read.')
    return read_parser.parse_args()
