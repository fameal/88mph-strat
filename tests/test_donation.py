import brownie
from brownie import Contract
import pytest


def test_want_donation(
    chain, accounts, user, amount, token, reserve, vault, strategy, RELATIVE_APPROX
):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    assert token.balanceOf(vault.address) == amount

    chain.sleep(1)

    # donate want tokens
    donation_amount = 1_000 * 10 ** token.decimals()
    token.transfer(strategy, donation_amount, {"from": reserve})

    # harvest
    before_pps = vault.pricePerShare()
    strategy.harvest()
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount
    chain.sleep(3600 * 6)
    chain.mine(1)
    assert before_pps < vault.pricePerShare()


def test_dai_donation(
    chain,
    accounts,
    user,
    token,
    amount,
    dai,
    reserve_dai,
    vault,
    strategy,
    RELATIVE_APPROX,
):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    assert token.balanceOf(vault.address) == amount

    # Harvest 1: Send funds through the strategy
    chain.sleep(1)

    # donate DAI tokens
    dai.transfer(strategy, 1_000 * 10 ** dai.decimals(), {"from": reserve_dai})

    # harvest
    before_pps = vault.pricePerShare()
    strategy.harvest()
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount
    chain.sleep(3600 * 6)
    chain.mine(1)
    assert before_pps < vault.pricePerShare()
