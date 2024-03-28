from geth.accounts import (
    parse_geth_accounts,
)

raw_accounts = b"""Account #0: {d3cda913deb6f67967b99d67acdfa1712c293601}
Account #1: {6f137a71a6f197df2cbbf010dcbd3c444ef5c925}\n"""
accounts = (
    b"0xd3cda913deb6f67967b99d67acdfa1712c293601",
    b"0x6f137a71a6f197df2cbbf010dcbd3c444ef5c925",
)


def test_parsing_accounts_output():
    assert parse_geth_accounts(raw_accounts) == accounts
