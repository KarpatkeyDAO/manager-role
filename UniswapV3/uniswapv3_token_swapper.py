from defi_protocols.functions import get_symbol, balance_of, get_data, get_node
from defi_protocols.constants import USDC_ETH, DAI_ETH, WETH_ETH, ETHEREUM
from defi_protocols.UniswapV3 import UNISWAPV3_ROUTER2
from txn_uniswapv3_helpers import COMP, AAVE, RETH2, SWISE, SETH2, bcolors, swap_selected_token, json_file_download, restart_end
from datetime import datetime
import math

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LITERALS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
TOKENS = [SETH2, COMP, AAVE, RETH2, SWISE]

PATHS = {
    COMP: {
        USDC_ETH: [COMP, WETH_ETH, USDC_ETH],
        DAI_ETH: [COMP, WETH_ETH, DAI_ETH]
    },
    AAVE: {
        USDC_ETH: [AAVE, WETH_ETH, USDC_ETH],
        DAI_ETH: [AAVE, WETH_ETH, DAI_ETH]
    },
    RETH2: {
        USDC_ETH: [RETH2, SETH2, WETH_ETH, USDC_ETH],
        DAI_ETH: [RETH2, SETH2, WETH_ETH, DAI_ETH]
    },
    SWISE: {
        USDC_ETH: [SWISE, SETH2, WETH_ETH, USDC_ETH],
        DAI_ETH: [SWISE, SETH2, WETH_ETH, DAI_ETH]
    },
    SETH2: {
        WETH_ETH: [SETH2, WETH_ETH]
    }
}


# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # swap_selected_token
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def swap_selected_token():
    
#     rate = get_rate(path)

#     expected_amount = rate * token_balance
    
#     message = 'Expected amount of %s for the %f of %s is: %f' % (swap_token_symbol, token_balance, token_symbol, expected_amount)
#     print(f"{bcolors.OKGREEN}{bcolors.BOLD}{message}{bcolors.ENDC}")

#     print()

#     print('Do you wish to proceed: ')
#     print('1- Yes')
#     print('2- No')
#     print()

#     option = input('Enter the option: ')
#     while option not in ['1','2']:
#         option = input('Enter a valid option (1, 2): ')
    
#     print()
    
#     if option == '1':
#         slippage = input('Enter the MAX amount of slippage tolerance: ')
#         while True:
#             try:
#                 slippage = float(slippage)
#                 break
#             except:
#                 slippage = input('Enter a valid amount: ')

#         approve_tokens(avatar_address, roles_mod_address, selected_token, swap_token, json_file, web3=web3)

#         tx_data = get_data(UNISWAPV3_ROUTER2, 'swapExactTokensForTokens', [token_balance, amount_out_min, path, avatar_address])
#         if tx_data is not None:
#             add_txn_with_role(roles_mod_address, tx_data, 0, json_file, web3=web3)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------                       
web3 = get_node(ETHEREUM)

proceed = True
print(f"{bcolors.HEADER}{bcolors.BOLD}-------------------------------{bcolors.ENDC}")
print(f"{bcolors.HEADER}{bcolors.BOLD}--- UniswapV3 Token Swapper ---{bcolors.ENDC}")
print(f"{bcolors.HEADER}{bcolors.BOLD}-------------------------------{bcolors.ENDC}")
print()

avatar_address = input('Enter the Avatar Safe address: ')
while not web3.isAddress(avatar_address):
    avatar_address = input('Enter a valid address: ')

web3.toChecksumAddress(avatar_address)
print()

roles_mod_address = input('Enter the Roles Module address: ')
while not web3.isAddress(roles_mod_address):
    roles_mod_address = input('Enter a valid address: ')

web3.toChecksumAddress(roles_mod_address)

while True:
    print()
    print('Select the token to swap: ')
    print(f"{bcolors.WARNING}If you choose sETH2, it will automatically be swapped by WETH{bcolors.ENDC}")
    print()
    valid_token_options = []
    for i in range(len(TOKENS)):
        print('%d- %s' % (i+1, get_symbol(TOKENS[i], ETHEREUM, web3=web3)))
        valid_token_options.append(str(i+1))

    print()
    token_option = input('Enter the token: ') 
    while token_option not in valid_token_options:
        message = 'Enter a valid option (' + ','.join(option for option in valid_token_options) + '): '
        token_option = input(message)

    print()
    selected_token = TOKENS[int(token_option)-1]
    token_symbol = get_symbol(selected_token, ETHEREUM, web3=web3)
    token_balance = balance_of(avatar_address, selected_token, 'latest', ETHEREUM, web3=web3)
    message = 'Selected Token: %s\nBalance: %f' % (token_symbol, token_balance)
    print(f"{bcolors.OKBLUE}{bcolors.BOLD}{message}{bcolors.ENDC}")
    print()

    if selected_token != SETH2:
        print('Select the token to swap the %s balance for: ' % token_symbol)
        print('1- USDC')
        print('2- DAI')
        print()
        swap_option = input('Enter the option: ')
        while swap_option not in ['1','2']:
            swap_option = input('Enter a valid option (1, 2): ')
        
        if swap_option == '1':
            swap_token = USDC_ETH
            swap_token_symbol = 'USDC'
        elif swap_option == '2':
            swap_token = DAI_ETH
            swap_token_symbol = 'DAI'

    else:
        swap_token = WETH_ETH
        swap_token_symbol = 'WETH'
        
    path = PATHS[selected_token][swap_token]

    json_file = {
        'version': '1.0',
        'chainId': '1',
        'meta': {
            'name': None,
            'description': '',
            'txBuilderVersion': '1.8.0'
        },
        'createdAt': math.floor(datetime.now().timestamp()*1000),
        'transactions': []
    }

    print()

    swap_selected_token(avatar_address, roles_mod_address, path, selected_token, token_balance, token_symbol, swap_token, swap_token_symbol, json_file, web3=web3)

    if json_file['transactions'] != []:
        json_file_download(json_file)
        break
    else:
        restart_end()
