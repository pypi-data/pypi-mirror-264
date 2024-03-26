class Wallet(object):
    """docstring for Wallet"""

    def __init__(self, *args, **kwargs):
        super(Wallet, self).__init__(*args, **kwargs)

    def gen(self):
        print("""
            Usage: namada wallet gen [OPTIONS] --alias <alias>

            --chain-id <chain-id>  The chain ID.
            --scheme <scheme>      For the transparent pool, the type of key that should be generated.
                                   Not applicable for the shielded pool.
            --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
            --shielded             Generate a spending key for the shielded pool.
            --raw                  Generate a random non-HD secret / spending key. No mnemonic code is generated.
            --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
            --alias <alias>        The key and address alias.
            --pre-genesis          Dispatch pre-genesis specific logic.
            --alias-force          Override the alias without confirmation if it already exists.
            --unsafe-dont-encrypt  UNSAFE: Do not encrypt the keypair. Do not use this for keys used in a live network.
            --hd-path <hd-path>    HD key derivation path. Use keyword `default` to refer to a scheme default path:
                                   - m/44'/60'/0'/0/0 for the transparent secp256k1 scheme
                                   - m/44'/877'/0'/0'/0' for the transparent ed25519 scheme
                                   - m/32'/877'/0' for the shielded setting
                                   For ed25519 scheme, all path indices will be promoted to hardened indexes. If none is specified, the scheme default path is used.
            --allow-non-compliant  Allow non-compliant HD derivation path. The compliant derivation path schemes include:
                                   - m/44'/60'/account'/change/address_index for the transparent secp256k1 scheme
                                   - m/44'/877'/account'/change'/address_index' for the transparent ed25519 scheme
                                   - m/32'/877'/account' and
                                   - m/32'/877'/account'/address_index for the shielded setting
            --bip39-passphrase     Use an additional passphrase for HD-key generation.
        """)

    def derive(self):
        print("""
            Usage: namada wallet derive [OPTIONS] --alias <alias>

            --chain-id <chain-id>  The chain ID.
            --scheme <scheme>      For the transparent pool, the type of key that should be derived.
                                   Not applicable for the shielded pool.
            --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
            --shielded             Derive a spending key for the shielded pool.
            --alias <alias>        The key and address alias.
            --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
            --alias-force          Force overwrite the alias if it already exists.
            --pre-genesis          Dispatch pre-genesis specific logic.
            --unsafe-dont-encrypt  UNSAFE: Do not encrypt the keypair. Do not use this for keys used in a live network.
            --use-device           Derive an address and public key from the seed stored on the connected hardware wallet.
            --hd-path <hd-path>    HD key derivation path. Use keyword `default` to refer to a scheme default path:
                                   - m/44'/60'/0'/0/0 for the transparent secp256k1 scheme
                                   - m/44'/877'/0'/0'/0' for the transparent ed25519 scheme
                                   - m/32'/877'/0' for the shielded setting
                                   For ed25519 scheme, all path indices will be promoted to hardened indexes. If none is specified, the scheme default path is used.
            --allow-non-compliant  Allow non-compliant HD derivation path. The compliant derivation path schemes include:
                                   - m/44'/60'/account'/change/address_index for the transparent secp256k1 scheme
                                   - m/44'/877'/account'/change'/address_index' for the transparent ed25519 scheme
                                   - m/32'/877'/account' and
                                   - m/32'/877'/account'/address_index for the shielded setting
            --bip39-passphrase     Use an additional passphrase for HD-key generation.
        """)

    def gen_payment_addr(self):
        print("""
            Usage: namada wallet gen-payment-addr [OPTIONS] --alias <alias> --key <key>

            --alias <alias>        An alias to be associated with the payment address.
            --chain-id <chain-id>  The chain ID.
            --alias-force          Override the alias without confirmation if it already exists.
            --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
            --key <key>            The viewing key.
            --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
            --pin                  Require that the single transaction to this address be pinned.
            --pre-genesis          Dispatch pre-genesis specific logic.
        """)

    def list(self):
        print("""
            Usage: namada wallet list [OPTIONS]

            --chain-id <chain-id>  The chain ID.
            --transparent          List transparent keys / addresses only.
            --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
            --shielded             List keys / addresses of the shielded pool only.
            --keys                 List keys only.
            --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
            --addr                 List addresses only.
            --pre-genesis          Dispatch pre-genesis specific logic.
            --decrypt              Decrypt keys that are encrypted.
            --unsafe-show-secret   UNSAFE: Print the secret / spending keys.
        """)

    def find(self):
        print("""
            Usage: namada wallet find [OPTIONS] <--alias <alias>|--address <address>|--public-key <public-key>|--public-key-hash <public-key-hash>|--payment-address <payment-address>>

            --alias <alias>                      An alias associated with the keys / addresses.
            --chain-id <chain-id>                The chain ID.
            --address <address>                  The bech32m encoded string of a transparent address.
            --base-dir <base-dir>                The base directory is where the nodes, client and wallet configuration and state is stored.
            --public-key <public-key>            A public key associated with the transparent keypair.
            --wasm-dir <wasm-dir>                Directory with built WASM validity predicates, transactions.
            --public-key-hash <public-key-hash>  A public key hash associated with the transparent keypair.
            --payment-address <payment-address>  The bech32m encoded string of a shielded payment address.
            --keys                               Find keys only.
            --addr                               Find addresses only.
            --pre-genesis                        Use pre-genesis wallet, instead of for the current chain, if any.
            --decrypt                            Decrypt keys that are encrypted.
            --unsafe-show-secret                 UNSAFE: Print the secret / spending key.
        """)

    def export(self):
        print("""
            --alias <alias>        The alias of the key you wish to export.
            --chain-id <chain-id>  The chain ID.
            --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
            --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
            --pre-genesis          Dispatch pre-genesis specific logic.
        """)

    def convert(self):
        print("""
            --alias <alias>        The alias of the key you wish to export.
            --chain-id <chain-id>  The chain ID.
            --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
            --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
            --pre-genesis          Dispatch pre-genesis specific logic.
        """)

    def import_(self):
        print("""
            Usage: namada wallet export [OPTIONS] --alias <alias>

            --chain-id <chain-id>  The chain ID.
            --file <file>          Path to the file containing the key you wish to import.
            --alias <alias>        The alias assigned to the.
            --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
            --alias-force          An alias to be associated with the imported entry.
            --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
            --pre-genesis          Dispatch pre-genesis specific logic.
            --unsafe-dont-encrypt  UNSAFE: Do not encrypt the imported keys. Do not use this for keys used in a live network.
        """)

    def add(self):
        print("""
            Usage: namada wallet add [OPTIONS] --alias <alias> --value <value>

            --alias <alias>        An alias to be associated with the new entry.
            --chain-id <chain-id>  The chain ID.
            --alias-force          Override the alias without confirmation if it already exists.
            --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
            --value <value>        Any value of the following:
                                   - transparent pool secret key
                                   - transparent pool public key
                                   - transparent pool address
                                   - shielded pool spending key
                                   - shielded pool viewing key
                                   - shielded pool payment address 
            --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
            --pre-genesis          Dispatch pre-genesis specific logic.
            --unsafe-dont-encrypt  UNSAFE: Do not encrypt the added keys. Do not use this for keys used in a live network.
        """)

    def remove(self):
        print("""
            Usage: namada wallet remove [OPTIONS] --alias <alias> --do-it

            --alias <alias>        An alias to be removed.
            --chain-id <chain-id>  The chain ID.
            --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
            --do-it                Confirm alias removal.
            --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
            --pre-genesis          Dispatch pre-genesis specific logic.
        """)

    def help(self):
        print("""
            Usage: namada wallet [OPTIONS] <COMMAND>

            Functions:
              gen               Generates a new transparent / shielded secret key.
              derive            Derive transparent / shielded key from the mnemonic code or a seed stored on the hardware wallet device.
              gen_payment_addr  Generates a payment address from the given spending key.
              list              List known keys and addresses in the wallet.
              find              Find known keys and addresses in the wallet.
              export            Exports a transparent keypair / shielded spending key to a file.
              convert           Convert to tendermint priv_validator_key.json with your consensus key alias
              import_           Imports a transparent keypair / shielded spending key from a file.
              add               Adds the given key or address to the wallet.
              remove            Remove the given alias and all associated keys / addresses from the wallet.
              help              Print this message or the help of the given subcommand(s)

            Options:
                  --chain-id <chain-id>  The chain ID.
                  --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
                  --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
                  --pre-genesis          Dispatch pre-genesis specific logic.

        """)