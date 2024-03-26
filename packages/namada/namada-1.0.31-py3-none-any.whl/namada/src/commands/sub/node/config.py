class Config(object):
    """docstring for Config"""

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

    def gen(self):
        pass

    def update_local_config(self):
        pass

    def help(self):
        print("""
            Usage: namada node config [OPTIONS] <COMMAND>

            Commands:
              gen                  Generate the default configuration file.
              update_local_config  Update the validator's local configuration.
              help                 Print this message or the help of the given subcommand(s)

            Options:
                  --chain-id <chain-id>  The chain ID.
                  --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
                  --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
                  --pre-genesis          Dispatch pre-genesis specific logic.
        """)
