from .sub.relayer.ethereum_bridge_pool import EthereumBridgePool
from .sub.relayer.validator_set import ValidatorSet

class Relayer(object):
    """docstring for Relayer"""
    def __init__(self, *args, **kwargs):
        super(Relayer, self).__init__(*args, **kwargs)
        self.ethereum_bridge_pool = EthereumBridgePool()
        self.validator_set = ValidatorSet()


    def help(self):
        print("""
            Usage: namada relayer [OPTIONS] <COMMAND>

            Commands:
              ethereum_bridge-pool  Functionality for interacting with the Ethereum bridge pool. This pool holds transfers waiting to be relayed to Ethereum.
              validator_set         Validator set queries, that return data in a format to be consumed by the Namada Ethereum bridge smart contracts.
              help                  Print this message or the help of the given subcommand(s)

            Options:
                  --chain-id <chain-id>  The chain ID.
                  --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
                  --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
                  --pre-genesis          Dispatch pre-genesis specific logic.
        """)
