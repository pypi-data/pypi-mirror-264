class VoteProposal(object):
    """docstring for VoteProposal"""
    def __init__(self, *args, **kwargs):
        super(VoteProposal, self).__init__(*args, **kwargs)

    def help(self):
        print("""
            Usage: namada vote-proposal [OPTIONS] --vote <vote> --address <address>

            Options:
                  --dry-run
                      Simulate the transaction application.
                  --base-dir <base-dir>
                      The base directory is where the nodes, client and wallet configuration and state is stored.
                  --dry-run-wrapper
                      Simulate the complete transaction application. This estimates the gas cost of the transaction.
                  --dump-tx
                      Dump transaction bytes to a file.
                  --wasm-dir <wasm-dir>
                      Directory with built WASM validity predicates, transactions. This value can also be set via `NAMADA_WASM_DIR` environment variable, but the argument takes precedence, if specified.
                  --force
                      Submit the transaction even if it doesn't pass client checks.
                  --pre-genesis
                      Dispatch pre-genesis specific logic.
                  --broadcast-only
                      Do not wait for the transaction to be applied. This will return once the transaction is added to the mempool.
                  --node <node>
                      Address of a ledger node as "{scheme}://{host}:{port}". If the scheme is not supplied, it is assumed to be TCP.
                  --alias <alias>
                      If any new account is initialized by the tx, use the given alias to save it in the wallet. If multiple accounts are initialized, the alias will be the prefix of each new address joined with a number.
                  --gas-price <gas-price>
                      The amount being paid, per gas unit, for the inclusion of this transaction
                  --gas-token <gas-token>
                      The token for paying the gas
                  --gas-spending-key <gas-spending-key>
                      The spending key to be used for fee unshielding. If none is provided, fee will be paid from the unshielded balance only.
                  --gas-limit <gas-limit>
                      The multiplier of the gas limit resolution defining the maximum amount of gas needed to run transaction.
                  --wallet-alias-force
                      Override the alias without confirmation if it already exists.
                  --expiration <expiration>
                      The expiration datetime of the transaction, after which the tx won't be accepted anymore. All of these examples are equivalent:
                      2012-12-12T12:12:12Z
                      2012-12-12 12:12:12Z
                      2012-  12-12T12:  12:12Z
                  --disposable-gas-payer
                      Generates an ephemeral, disposable keypair to sign the wrapper transaction. This keypair will be immediately discarded after use.
                  --signing-keys <signing-keys>...
                      Sign the transaction with the key for the given public key, public key hash or alias from your wallet.
                  --signatures <signatures>...
                      List of file paths containing a serialized signature to be attached to a transaction. Requires to provide a gas payer.
                  --output-folder-path <output-folder-path>
                      The output folder path where the artifact will be stored.
                  --chain-id <chain-id>
                      The chain ID.
                  --gas-payer <gas-payer>
                      The implicit address of the gas payer. It defaults to the address associated to the first key passed to --signing-keys.
                  --use-device
                      Use an attached hardware wallet device to sign the transaction.
                  --memo <memo>
                      Attach a plaintext memo to the transaction.
                  --proposal-id <proposal-id>
                      The proposal identifier.
                  --vote <vote>
                      The vote for the proposal. Either yay, nay, or abstain.
                  --offline
                      Flag if the proposal vote should run offline.
                  --data-path <data-path>
                      The data path file (json) that describes the proposal.
                  --address <address>
                      The address of the voter.
        """)
