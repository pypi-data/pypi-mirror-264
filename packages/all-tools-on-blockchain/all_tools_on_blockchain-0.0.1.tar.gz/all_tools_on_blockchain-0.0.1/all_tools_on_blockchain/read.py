from prettytable import PrettyTable
import requests
import json

web3 = None
DEFAULT_SLOTS = [
    {"name": "_ROLLBACK_SLOT", "value": "0x4910fdfa16fed3260ed0e7147f7cc6da11a60208b5b9406d12a635614ffd9143"},
    {"name": "_IMPLEMENTATION_SLOT", "value": "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"},
    {"name": "_ADMIN_SLOT", "value": "0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103"},
    {"name": "_BEACON_SLOT", "value": "0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50"},
]
all_info_table = PrettyTable(['ABI From Which Contract', 'Data Type', 'Variable Name', 'Value｜Input Type'])
extra_data = {}


def safe_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network request error: {e}")
        return None


# 通过slot读取合约数据
def read_contract_by_slot(address, slot):
    try:
        storage_value = web3.eth.get_storage_at(address, slot)
        return storage_value.hex()
    except Exception as e:
        print(f"Error reading contract data: {e}")
        return None


def read_default_slot(address):
    temp = []
    for slot in DEFAULT_SLOTS:
        slot_value = read_contract_by_slot(address, slot['value'])
        temp.append({
            "slot": slot['name'],
            "value": slot_value
        })
    return temp


def has_data(table: PrettyTable) -> bool:
    empty_table_str = table.get_string(start=0, end=0)
    # Attempt to render the table including one row.
    one_row_table_str = table.get_string(end=1)
    # If the length of the string with one row is greater, it means there's at least one row.
    return len(one_row_table_str) > len(empty_table_str)


def is_contract(address):
    # 使用eth.get_code
    code = web3.eth.get_code(address)
    # 如果代码是'0x'或'0x0'，则它不是合约地址
    return code != b'' and code != '0x'


def get_contract_params_info(address, check_proxy_flag):
    contract_address = web3.to_checksum_address(address)
    if not is_contract(contract_address):
        print('The address entered is EOA! ! !')
        return

    # 合约地址和ABI（替换这里的值）
    imp = contract_address
    is_proxy = f'https://api.etherscan.io/api?module=contract&action=getsourcecode&address={contract_address}&apikey=Q8K1J5WIXHVQWV1XHVFF1INTPHWFZP5AZV'
    check_proxy = safe_request(is_proxy)
    result = check_proxy['result'][0]
    if check_proxy_flag:
        print(f'Contract Address: {contract_address}\nContract Name: {result["ContractName"]}')
        if result['Implementation'] != '':
            print(f"Proxy detected.\nImplement contract address:{result['Implementation']}")
            imp = result['Implementation']
            get_contract_params_info(contract_address, False)
        print("reading data...", end='')
        # read slot
        slot_table_data = read_default_slot(contract_address)
        for slot_data_item in slot_table_data:
            all_info_table.add_row([contract_address, "slot", slot_data_item['slot'], slot_data_item['value']])

    abi_url = f'https://api.etherscan.io/api?module=contract&action=getabi&address={imp}&apikey=Q8K1J5WIXHVQWV1XHVFF1INTPHWFZP5AZV'
    req = safe_request(abi_url)

    contract_abi = json.loads(req['result'])

    # 创建合约实例
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    for item in contract_abi:
        if item['type'] == 'function' and item.get('stateMutability') in ['view', 'pure']:
            try:
                if 'inputs' in item:
                    if len(item['inputs']) == 0:  # 无参数函数
                        func = contract.functions[item['name']]()
                        value = func.call()
                        if type(value) == bytes:
                            value = value.hex()
                        if len(str(value)) > 100:
                            extra_data[item['name']] = value
                            value = f'type: {type(value).__name__} length: {len(value)} (details see extra data)'
                        all_info_table.add_row([imp, "no params func", item['name'], value])
                        # if item['name'].lower().find("slot") and len(value)
                    else:  # 有参数函数
                        input_types = ', '.join([input['type'] for input in item['inputs']])
                        all_info_table.add_row([imp, "with params func", item['name'], input_types])
            except Exception as e:
                # print(f"Error calling {item['name']}: {str(e)}")
                pass


def read_contract_storage_data(address, slot, we3_instance):
    if slot == '' or address == '':
        print('Please input address and slot')
        return
    try:
        data = we3_instance.eth.get_storage_at(address, slot)
        print(f'address:{address}\nslot:{slot}\nvalue:{data.hex()}')
    except Exception as e:
        print(f"Failed to obtain stored data: {e}")


def read_contract_onchain_public_view_data(address, web3_instance):
    # 初始化Web3
    global web3
    web3 = web3_instance
    get_contract_params_info(address, True)
    # 打印表格
    print('\r', end='')
    if has_data(all_info_table):
        all_info_table.sortby = "Data Type"
        print(all_info_table)
    else:
        print("There is no data in the table...")
    if extra_data != {}:
        print("Extra data:", extra_data)


if __name__ == '__main__':
    from web3 import Web3
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/c77b93a34625489b8a04b548c96369bf'))
    read_contract_onchain_public_view_data("0x909A86f78e1cdEd68F9c2Fe2c9CD922c401abe82", web3)
