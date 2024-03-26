from .sub.node.ledger import Ledger
from .sub.node.config import Config

class Node():
    """docstring for Node"""
    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self.ledger = Ledger()
        self.config = Config()

    def help(self):
        print("""
            Usage: namada node [OPTIONS] <COMMAND>

            Commands:
              ledger  Ledger node sub-commands. If no sub-command specified, defaults to run the node.
              config  Configuration sub-commands.
              help    Print this message or the help of the given subcommand(s)

            Options:
                  --chain-id <chain-id>  The chain ID.
                  --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
                  --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
                  --pre-genesis          Dispatch pre-genesis specific logic.
        """)
