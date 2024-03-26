import requests
from commands.node import Node
from .commands.relayer import Relayer
from .commands.client import Client
from .commands.wallet import Wallet
from .commands.ethereum_bridge_pool import EthereumBridgePool
from .commands.ledger import Ledger
from .commands.tx import TX
from .commands.transfer import Transfer
from .commands.ibc_transfer import IBCTransfer
from .commands.update_account import UpdateAccount
from .commands.init_proposal import InitProposal
from .commands.vote_proposal import VoteProposal
from .commands.reveal_pk import RevealPK


class Namada(object):
    """docstring for Namada Python package"""
    ENDPOINT = 'https://namada-explorer-api.stakepool.dev.br/node'

    def __init__(self, *args, **kwargs):
        super(Namada, self).__init__(*args, **kwargs)
        self.node = Node()
        self.relayer = Relayer()
        self.client = Client()
        self.wallet = Wallet()
        self.ethereum_bridge_pool = EthereumBridgePool()
        self.ledger = Ledger()
        self.tx = TX()
        self.transfer = Transfer()
        self.ibc_transfer = IBCTransfer()
        self.update_account = UpdateAccount()
        self.init_proposal = InitProposal()
        self.vote_proposal = VoteProposal()
        self.reveal_pk = RevealPK()

    def help(self):
        print("""
            Usage: namada [OPTIONS] <COMMAND>

            Commands:
              node                  Node sub-commands.
              relayer               Relayer sub-commands.
              client                Client sub-commands.
              wallet                Wallet sub-commands.
              ethereum_bridge_pool  Functionality for interacting with the Ethereum bridge pool.
              ledger                Ledger node sub-commands. If no sub-command specified, defaults to run the node.
              tx                    Send a transaction with custom WASM code.
              transfer              Send a signed transfer transaction.
              ibc_transfer          Send a signed IBC transfer transaction.
              update_account        Send a signed transaction to update account's validity predicate.
              init_proposal         Create a new proposal.
              vote_proposal         Vote a proposal.
              reveal_pk             Submit a tx to reveal the public key an implicit account.
              help                  Print this message or the help of the given subcommand(s)

            Options:
                  --chain-id <chain-id>  The chain ID.
                  --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
                  --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
                  --pre-genesis          Dispatch pre-genesis specific logic.
              -h, --help                 Print help
        """)


    def __get_data(self, url):
        response = requests.get(url)
        return response.json()

###############################################################################

    def get_latest_block(self):
        return self.__get_data(self.ENDPOINT + '/blocks/block/latest')

    def get_block_height(self, block_height):
        return self.__get_data(self.ENDPOINT + f'/blocks/block/{block_height}')

    def get_block_height_transactions(self, block_height):
        return self.__get_data(self.ENDPOINT + f'/blocks/block/{block_height}/transactions')

    def get_block_height_signatures(self, block_height):
        return self.__get_data(self.ENDPOINT + f'/blocks/block/{block_height}/signatures')

    def get_block_list_records(self, records):
        return self.__get_data(self.ENDPOINT + f'/blocks/list/{records}')

    def get_block_list_records_to_block(self, records, to_block):
        return self.__get_data(self.ENDPOINT + f'/blocks/list/{records}/{to_block}')

###############################################################################

    def get_latest_tx(self):
        return self.__get_data(self.ENDPOINT + f'/transactions/transaction/latest')

    def get_tx_hash(self, tx_hash):
        return self.__get_data(self.ENDPOINT + f'/transactions/transaction/{tx_hash}')

    def get_tx_list_records(self, records):
        return self.__get_data(self.ENDPOINT + f'/transactions/list/{records}')

    def get_tx_list_records_to_block(self, records, to_block):
        return self.__get_data(self.ENDPOINT + f'/transactions/list/{records}/{to_block}')

###############################################################################

    def get_validator_list(self):
        return self.__get_data(self.ENDPOINT + '/validators/list')

    def get_validator_address(self, address):
        return self.__get_data(self.ENDPOINT + f'/validators/validator/{address}')

    def get_validator_latest_block(self, address):
        return self.__get_data(self.ENDPOINT + f'/validators/validator/{address}/latestBlocks')

    def get_validator_latest_signatures(self, address):
        return self.__get_data(self.ENDPOINT + f'/validators/validator/{address}/latestSignatures')

###############################################################################