import time
import requests

# from config import setting
from app import app
from ethereum.utils import checksum_encode
from .config import setting
from .ethClient import Client

eth_client = Client(eth_url=setting.ETH_URL)
# wba_invoker = "0xBF3De70657B3C346E72720657Bbc75AbFc4Ec217"
wba_create = app.config["WBA_CREATE"]
# contract=eth_client.get_contract_instance(setting.CONTRACT_ADDRESS,setting.erc721_abi)

def create_nft(ids, rev, pk):
    """
    :param ids:         代币id(int) list  
    :param rev:         token创建后 接收该token的地址  
    :param pk:          合约调用者私钥

    :return TX HASH
    """
    rev=checksum_encode(rev)
    tx_id = eth_client.contruct_Transaction(
        "wba",
        invoker=wba_create,
        method="createToken",
        args=[ids, rev],
        private_key=pk
    )
    return {
        "txId": tx_id
    }


def set_nft_by_token_id(invoker, token_id, attribute, status, pk):
    tx_id = eth_client.contruct_Transaction(
        "wba",
        invoker=wba_create,
        method="setNFTbyTokenId",
        args=[token_id, attribute, status],
        private_key=pk
    )
    return {
        "txId": tx_id
    }

def transfer_from(addr_from, addr_to, token_id, pk):
    addr_from = checksum_encode(addr_from)
    addr_to = checksum_encode(addr_to)
    tx_id = eth_client.contruct_Transaction(
        "wba",
        invoker=addr_from,
        method="transferFrom",
        args=[addr_from, addr_to, token_id],
        private_key=pk
    )
    return {
        "txId": tx_id
    }


def transfer(addr_to, token_id, pk):
    addr_to = checksum_encode(addr_to)
    tx_id = eth_client.contruct_Transaction(
        "wba",
        invoker=wba_create,
        method="transfer",
        args=[addr_to, token_id],
        private_key=pk
    )
    return {
        "txId": tx_id
    }

# def approve(invoker,addressTo,tokenId,privateKey):
#     addressTo = checksum_encode(addressTo)
#     unsigned_tx_data = eth_client.contruct_Transaction(invoker, contract, "approve", [addressTo,tokenId])
#     return {
#         "txData":unsigned_tx_data
#     }

def balance_of(ownerAddress):
    ownerAddress=checksum_encode(ownerAddress)
    balance=eth_client.call_contract(contract,"balanceOf",[ownerAddress])
    return {
        "balance":balance
    }

def get_all_tokens():
    all_tokens=eth_client.call_contract(contract,"getAllTokens",[])
    return {
        "allTokens":all_tokens
    }

def get_nft_by_token_id(tokenId):
    token_info=eth_client.call_contract(contract,"getNFTbyTokenId",[tokenId])
    return {
        "tokenInfo":token_info
    }


def sign(unsignedTxData,privtKey):
    signature=eth_client.sign(unsignedTxData,privtKey)

    return {
        "signature":signature
    }

def broadcast(unsignedTxData,signature):
    res=eth_client.broadcast(unsignedTxData,signature)
    return {
        "txId":res
    }
