class EthereumBridgePool(object):
    """docstring for EthereumBridgePool"""

    def __init__(self, *args, **kwargs):
        super(EthereumBridgePool, self).__init__(*args, **kwargs)

    def construct_proof(self):
        pass

    def query(self):
        pass

    def query_relayed(self):
        pass

    def query_signed(self):
        pass

    def recommend_batch(self):
        pass

    def relay_proof(self):
        pass

    def help(self):
        print("""
            Usage: namada relayer ethereum-bridge-pool [OPTIONS] <COMMAND>

            Commands:
              construct_proof  Construct a merkle proof that the given transfers are in the pool.
              query            Get the contents of the Ethereum Bridge pool.
              query_relayed    Get the confirmation status of transfers to Ethereum.
              query_signed     Get the contents of the Ethereum Bridge pool with a signed Merkle root.
              recommend_batch  Get a recommended batch of transfers from the bridge pool to relay to Ethereum.
              relay_proof      Construct a merkle proof that the given transfers are in the pool and relay it to Ethereum.
              help             Print this message or the help of the given subcommand(s)

            Options:
                  --chain-id <chain-id>  The chain ID.
                  --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
                  --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
                  --pre-genesis          Dispatch pre-genesis specific logic.
        """)
