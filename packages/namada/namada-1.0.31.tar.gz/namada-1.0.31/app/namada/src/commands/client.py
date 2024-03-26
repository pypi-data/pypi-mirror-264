class Client(object):
    """docstring for Client"""
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)

    def help(self):
        print("""
            Usage: namada client [OPTIONS] <COMMAND>

            Commands:
              ibc_transfer               Send a signed IBC transfer transaction.
              init_account               Send a signed transaction to create a new established account.
              init_proposal              Create a new proposal.
              reveal_pk                  Submit a tx to reveal the public key an implicit account. Typically, you don't have to do this manually and the client will detect when a tx to reveal PK is needed and submit it automatically. This will write the PK into the account's storage so that it can be used for signature verification on transactions authorized by this account.
              transfer                   Send a signed transfer transaction.
              tx                         Send a transaction with custom WASM code.
              update_account             Send a signed transaction to update account's validity predicate.
              vote_proposal              Vote a proposal.
              become_validator           Send a signed transaction to become a validator.
              bond                       Bond tokens in PoS system.
              change_commission_rate     Change commission rate.
              change_consensus_key       Change consensus key.
              change_metadata            Change validator's metadata, including the commission rate if desired.
              claim_rewards              Claim available rewards tokens from bonds that contributed in consensus.
              deactivate_validator       Send a signed transaction to deactivate a validator.
              init_validator             Send a signed transaction to create an established account and then become a validator.
              reactivate_validator       Send a signed transaction to reactivate an inactive validator.
              redelegate                 Redelegate bonded tokens from one validator to another.
              unbond                     Unbond tokens from a PoS bond.
              unjail_validator           Send a signed transaction to unjail a jailed validator.
              withdraw                   Withdraw tokens from previously unbonded PoS bond.
              add_erc20_transfer         Add a new transfer to the Ethereum Bridge pool.
              resign_steward             Craft a transaction to resign as a steward.
              update_steward_rewards     Update how steward commissions are split.
              balance                    Query balance(s) of tokens.
              block                      Query the last committed block.
              bonded_stake               Query PoS bonded stake.
              bonds                      Query PoS bond(s).
              commission_rate            Query a validator's commission rate.
              conversions                Query currently applicable conversions.
              delegations                Find PoS delegations from the given owner address.
              epoch                      Query the epoch of the last committed block.
              find_validator             Find a PoS validator and its consensus key by its native address or Tendermint address.
              masp_reward_tokens         Query the tokens which can earn MASP rewards while shielded.
              next_epoch_info            Query some info to help discern when the next epoch will begin.
              query_account              Query the substorage space of a specific enstablished address.
              query_bytes                Query the raw bytes of a given storage key
              query_pgf                  Query pgf stewards and continuous funding.
              query_proposal             Query proposals.
              query_proposal_result      Query proposals result.
              query_proposal_votes       Query votes for the proposal.
              query_protocol_parameters  Query protocol parameters.
              rewards                    Query the latest rewards available to claim for a given delegation (or self-bond).
              show_transfers             Query the accepted transfers to date.
              slashes                    Query PoS applied slashes.
              status                     Query the node's status.
              
              tx_result                  Query the result of a transaction.
              validator_metadata         Query a validator's metadata.
              validator_state            Query the state of a PoS validator.
              ibc_gen_shielded           Generate shielded transfer for IBC.
              shielded_sync              Sync the local shielded context with MASP notes owned by the provided viewing / spending keys up to an optional specified block height.
              sign_tx                    Sign a transaction offline.
              utils                      Utilities.
              help                       Print this message or the help of the given subcommand(s)

            Options:
                  --chain-id <chain-id>  The chain ID.
                  --base-dir <base-dir>  The base directory is where the nodes, client and wallet configuration and state is stored.
                  --wasm-dir <wasm-dir>  Directory with built WASM validity predicates, transactions.
                  --pre-genesis          Dispatch pre-genesis specific logic.
        """)

    def ibc_transfer(self):
        pass

    def init_account(self):
        pass

    def init_proposal(self):
        pass

    def reveal_pk(self):
        pass

    def transfer(self):
        pass

    def tx(self):
        pass

    def update_account(self):
        pass

    def vote_proposal(self):
        pass

    def become_validator(self):
        pass

    def bond(self):
        pass

    def change_commission_rate(self):
        pass

    def change_consensus_key(self):
        pass

    def change_metadata(self):
        pass

    def claim_rewards(self):
        pass

    def deactivate_validator(self):
        pass

    def init_validator(self):
        pass

    def reactivate_validator(self):
        pass

    def redelegate(self):
        pass

    def unbond(self):
        pass

    def unjail_validator(self):
        pass

    def withdraw(self):
        pass

    def add_erc20_transfer(self):
        pass

    def resign_steward(self):
        pass

    def update_steward_rewards(self):
        pass

    def balance(self):
        pass

    def block(self):
        pass

    def bonded_stake(self):
        pass

    def bonds(self):
        pass

    def commission_rate(self):
        pass

    def conversions(self):
        pass

    def delegations(self):
        pass

    def epoch(self):
        pass

    def find_validator(self):
        pass

    def masp_reward_tokens(self):
        pass

    def next_epoch_info(self):
        pass

    def query_account(self):
        pass

    def query_bytes(self):
        pass

    def query_pgf(self):
        pass

    def query_proposal(self):
        pass

    def query_proposal_result(self):
        pass

    def query_proposal_votes(self):
        pass

    def query_protocol_parameters(self):
        pass

    def rewards(self):
        pass

    def show_transfers(self):
        pass

    def slashes(self):
        pass

    def status(self):
        pass

    def tx_result(self):
        pass

    def validator_metadata(self):
        pass

    def validator_state(self):
        pass

    def ibc_gen_shielded(self):
        pass

    def shielded_sync(self):
        pass

    def sign_tx(self):
        pass

    def utils(self):
        pass
