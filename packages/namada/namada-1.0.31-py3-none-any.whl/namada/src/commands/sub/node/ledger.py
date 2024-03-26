class Ledger():
    """docstring for Ledger"""
    def __init__(self, *args, **kwargs):
        super(Ledger, self).__init__(*args, **kwargs)

    def run(self):
        pass

    def run_until(self):
        pass

    def reset(self):
        pass

    def dump_db(self):
        pass

    def rollback(self):
        pass

    def help(self):
        print("""
            Usage: namada node ledger [OPTIONS] [COMMAND]

            Commands:
              run        Run Namada ledger node.
              run_until  Run Namada ledger node until a given height. Then halt or suspend.
              reset      Delete Namada ledger node's and Tendermint node's storage data.
              dump_db    Dump Namada ledger node's DB from a block into a file.
              rollback   Roll Namada state back to the previous height. This command does not create a backup of neither the Namada nor the Tendermint state before execution: for extra safety, it is recommended to make a backup in advance.
              help       Print this message or the help of the given subcommand(s)

            Options:
                  --chain-id <chain-id>  The chain ID.
                  --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
                  --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
                  --pre-genesis          Dispatch pre-genesis specific logic.
        """)
