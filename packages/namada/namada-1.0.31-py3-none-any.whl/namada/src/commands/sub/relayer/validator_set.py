class ValidatorSet(object):
    """docstring for ValidatorSet"""

    def __init__(self, *args, **kwargs):
        super(ValidatorSet, self).__init__(*args, **kwargs)

    def bridge(self):
        pass

    def governance(self):
        pass

    def proof(self):
        pass

    def relay(self):
        pass

    def help(self):
        print("""
            Usage: namada relayer validator-set [OPTIONS] <COMMAND>

            Commands:
              bridge      Query the Bridge validator set in Namada, at the given epoch, or the latest one, if none is provided.
              governance  Query the Governance validator set in Namada, at the given epoch, or the latest one, if none is provided.
              proof       Query an Ethereum ABI encoding of a proof of the consensus validator set in Namada, at the requested epoch, or the next one, if no epoch is provided.
              relay       Relay a validator set update to Namada's Ethereum bridge smart contracts.
              help        Print this message or the help of the given subcommand(s)

            Options:
                  --chain-id <chain-id>  The chain ID.
                  --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
                  --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
                  --pre-genesis          Dispatch pre-genesis specific logic.
        """)
