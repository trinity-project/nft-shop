# -*- coding: utf-8 -*-

import binascii
import rlp
from ethereum import utils
from ethereum.utils import ecsign, normalize_key, int_to_big_endian, checksum_encode
from web3 import Web3, HTTPProvider
from ethereum.transactions import Transaction
from .config import setting

class Client(object):
    # 必须确用于提币的地址 在商城以外不产生 out 交易
    nonce_dict = {}

    def __init__(self, eth_url):
        self.web3 = Web3(HTTPProvider(eth_url))



    def get_contract_instance(self, contract_address, abi):
        contract = self.web3.eth.contract(address=checksum_encode(contract_address), abi=abi)
        return contract

    def invoke_contract(self, invoker, contract, method, args,gasLimit=800000):
        tx_dict = contract.functions[method](*args).buildTransaction({
            "gas": gasLimit,
            'gasPrice': self.web3.eth.gasPrice,
            'nonce': self.web3.eth.getTransactionCount(checksum_encode(invoker)),
        })
        tx = Transaction(
            nonce=tx_dict.get("nonce"),
            gasprice=tx_dict.get("gasPrice"),
            startgas=tx_dict.get("gas"),
            to=tx_dict.get("to"),
            value=tx_dict.get("value"),
            data=binascii.unhexlify(tx_dict.get("data")[2:]))

        UnsignedTransaction = Transaction.exclude(['v', 'r', 's'])
        unsigned_tx = rlp.encode(tx, UnsignedTransaction)

        return binascii.hexlify(unsigned_tx).decode()

    def sign(self, unsigned_tx, privtKey):
        before_hash = utils.sha3(binascii.unhexlify(unsigned_tx.encode()))
        v,r,s=ecsign(before_hash,normalize_key(privtKey))
        signature = binascii.hexlify(int_to_big_endian(r) + int_to_big_endian(s) +
                                     bytes(chr(v).encode())).decode()
        return signature

    def broadcast(self, unsigned_tx,signature):
        signature=binascii.unhexlify(signature.encode())
        unsigned_tx=binascii.unhexlify(unsigned_tx.encode())
        r = signature[0:32]
        s = signature[32:64]
        v = bytes(chr(signature[64]).encode())

        unsigned_items = rlp.decode(unsigned_tx)
        unsigned_items.extend([v, r, s])
        signed_items = unsigned_items

        signed_tx_data = rlp.encode(signed_items)
        tx_id = self.web3.eth.sendRawTransaction(signed_tx_data)
        return "0x"+binascii.hexlify(tx_id).decode()

    def sign_args(self,typeList, valueList, privtKey):
        '''

        :param typeList: ['bytes32', 'bytes32', 'uint256', 'uint256']
        :param valueList: ["0x3ae88fe370c39384fc16da2c9e768cf5d2495b48", "0x9da26fc2e1d6ad9fdd46138906b0104ae68a65d8", 1, 1]
        :param privtKey: "095e53c9c20e23fd01eaad953c01da9e9d3ed9bebcfed8e5b2c2fce94037d963"
        :return:
        '''
        data_hash = Web3.soliditySha3(typeList, valueList)
        v, r, s = ecsign(data_hash, normalize_key(privtKey))
        signature = binascii.hexlify(int_to_big_endian(r) + int_to_big_endian(s)
                                     + bytes(chr(v - 27).encode()))
        return signature

    def call_contract(self,contract,method,args):
        return contract.functions[method](*args).call()

    def estimate_gas(self, dict_transaction):
        return self.web3.eth.estimateGas(dict_transaction)


    # def contruct_Transaction(self, invoker, method, args,gasLimit=800000,privateKey=None):
    def contruct_Transaction(self, token_name, gasLimit=800000, **kwargs):
        """
        :param token_name:  代币名称  
        :param args:        调用合约函数实参  
        :param method:      合约方法名称  
        :param invoker:     合约调用者(地址)  
        :param private_key: 私钥  

        :return TX HASH
        """
        invoker = kwargs["invoker"]
        args = kwargs["args"]
        method = kwargs["method"]
        private_key = kwargs["private_key"]
        contract_instance = self.get_contract_instance(
            setting.SmartContract[token_name][0],
            setting.SmartContract[token_name][1]
        )
        if not self.nonce_dict.get(invoker):
            self.nonce_dict[invoker] = self.web3.eth.getTransactionCount(checksum_encode(invoker))
        tx = contract_instance.functions[method](*args).buildTransaction({
            "gas": gasLimit,
            'gasPrice': self.web3.eth.gasPrice,
            'nonce': self.nonce_dict[invoker]
        })
        # print(tx)
        signed = self.web3.eth.account.signTransaction(tx, private_key)
        tx_id = self.web3.eth.sendRawTransaction(signed.rawTransaction)
        self.nonce_dict[invoker] = self.nonce_dict[invoker] + 1
        return  "0x" + binascii.hexlify(tx_id).decode()

    def transfer_erc20(self, tokenName, addressFrom, addressTo, value, privtKey):
        '''
        erc20转账
        '''
        contract_instance=self.get_contract_instance(setting.SmartContract[tokenName][0],
                                                    setting.SmartContract[tokenName][1])
        if not self.nonce_dict.get(addressFrom):
            self.nonce_dict[addressFrom] = self.web3.eth.getTransactionCount(checksum_encode(addressFrom))
        tx = contract_instance.functions.transfer(
            checksum_encode(addressTo),
            int(value*(10**8))
        ).buildTransaction({
            'gasPrice': self.web3.eth.gasPrice,
            'gas':800000,
            'nonce': self.nonce_dict[addressFrom]
        })

        signed = self.web3.eth.account.signTransaction(tx, privtKey)
        tx_id=self.web3.eth.sendRawTransaction(signed.rawTransaction)
        self.nonce_dict[addressFrom] = self.nonce_dict[addressFrom] + 1
        return {
            "txId": "0x" + binascii.hexlify(tx_id).decode()
        }

    def transfer_eth(self, addressFrom, addressTo, value, privtKey, data=b''):
        '''
        eth转账
        '''
        dict_tx = {
            "from":addressFrom,
            "to":addressTo,
            "value":int(value*(10**18)),
            "data":data
        }
        if not self.nonce_dict.get(addressFrom):
            self.nonce_dict[addressFrom] = self.web3.eth.getTransactionCount(checksum_encode(addressFrom))
        print(self.nonce_dict[addressFrom])
        gas_limit = self.estimate_gas(dict_tx) * 2
        print(gas_limit)
        tx = Transaction(
            nonce=self.nonce_dict[addressFrom],
            gasprice=self.web3.eth.gasPrice,
            startgas=gas_limit,
            to=addressTo,
            value=int(value*(10**18)),
            data=data
        )

        tx.sign(privtKey)
        raw_tx = self.web3.toHex(rlp.encode(tx))
        tx_id = self.web3.eth.sendRawTransaction(raw_tx)
        self.nonce_dict[addressFrom] = self.nonce_dict[addressFrom] + 1
        return {
            "txId": "0x" + binascii.hexlify(tx_id).decode()
        }


if __name__ == "__main__":
    eth_client = Client(eth_url=setting.ETH_URL)
    # tx_id = client.transfer_erc20(
    #     "wbt",
    #     "0xBF3De70657B3C346E72720657Bbc75AbFc4Ec217",
    #     "0x3662B055A10ccFA6c098F23C4eEA3Bc36273B4d9",
    #     10,
    #     '9f56b1bc6c7ae9a715c7af2415f4c8c72ea3e2ebb8479b516918ae19dd3354ab'
    # )
    # tx_id = client.transfer_eth(
    #     # "wbt",
    #     "0xBF3De70657B3C346E72720657Bbc75AbFc4Ec217",
    #     "0x3662B055A10ccFA6c098F23C4eEA3Bc36273B4d9",
    #     0.0001,
    #     '9f56b1bc6c7ae9a715c7af2415f4c8c72ea3e2ebb8479b516918ae19dd3354ab',
    #     # b''
    #     'WOB 商城提币'.encode()
    # )

    def transfer_from(addr_from, addr_to, token_id, pk):
        addr_from = checksum_encode(addr_from)
        addr_to = checksum_encode(addr_to)
        tx_id = eth_client.contruct_Transaction(
            "wba",
            invoker="0xBF3De70657B3C346E72720657Bbc75AbFc4Ec217",
            method="transferFrom",
            args=[addr_from, addr_to, token_id],
            private_key=pk
        )
        return {
            "txId": tx_id
        }
    res = transfer_from(
        "0xF92daF55632579584f6ee34B99DE303742f22c81",
        "0xBF3De70657B3C346E72720657Bbc75AbFc4Ec217",
        71795507220047912011872197728,
        "0c9d8a0a5cf564f0f6ea5533a94fb109da0b00ed439c9ce882e1c5cae1144971"
    )
    print(res)