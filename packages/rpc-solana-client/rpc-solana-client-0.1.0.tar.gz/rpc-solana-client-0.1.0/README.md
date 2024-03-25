# Solana Client

A client for interacting with Solana RPC HTTP endpoint.

# Create client

from solana_client import SolanaClient

client = SolanaClient(endpoint="https://api.mainnet-beta.solana.com")

# Getting account information

account_info = await client.get_account_info("SOME_ACCOUNT_ADDRESS")

# Getting signatures for an address

signatures = await client.get_signatures_for_address("SOME_ACCOUNT_ADDRESS")

# Receiving a signature transaction

transaction = await client.get_transaction_by_signature("SOME_TRANSACTION_SIGNATURE")
