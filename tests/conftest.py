import pytest
import time
from brownie import config, Contract, interface


# Snapshots the chain before each test and reverts after test completion.
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.fixture
def gov(accounts):
    yield accounts.at("0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52", force=True)


@pytest.fixture
def user(accounts):
    yield accounts[0]


@pytest.fixture
def rewards(accounts):
    yield accounts[1]


@pytest.fixture
def guardian(accounts):
    yield accounts[2]


@pytest.fixture
def management(accounts):
    yield accounts[3]


@pytest.fixture
def strategist(accounts):
    yield accounts[4]


@pytest.fixture
def keeper(accounts):
    yield accounts[5]


@pytest.fixture
def user_2(accounts):
    yield accounts[6]


@pytest.fixture
def reserve(accounts):
    yield accounts.at("0xc2Be79CF419CF48f447320D5D16f5115bBb58B03", force=True)


@pytest.fixture
def reserve_dai(accounts):
    yield accounts.at("0xF977814e90dA44bFA03b6295A0616a897441aceC", force=True)


@pytest.fixture
def rewards_distribution(accounts):
    yield accounts.at("0x1Bb67aA336F21cfa5bD328C5930e5202Ed35dDEB", force=True)


@pytest.fixture
def rewards_contract():
    yield interface.IRewards("0x98df8D9E56b51e4Ea8AA9b57F8A5Df7A044234e1")


@pytest.fixture
def token():
    token_address = "0x8888801aF4d980682e47f1A9036e589479e835C5"  # MPH
    yield Contract(token_address)


@pytest.fixture
def dai():
    token_address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    yield Contract(token_address)


@pytest.fixture
def amount(reserve, token, user):
    amount = 500 * 10 ** token.decimals()
    token.transfer(user, amount, {"from": reserve})
    yield amount


@pytest.fixture
def amount_2(reserve, token, user_2):
    amount = 750 * 10 ** token.decimals()
    token.transfer(user_2, amount, {"from": reserve})
    yield amount


@pytest.fixture
def weth():
    token_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    yield Contract(token_address)


@pytest.fixture
def weth_amout(user, weth):
    weth_amout = 10 ** weth.decimals()
    user.transfer(weth, weth_amout)
    yield weth_amout


@pytest.fixture(scope="function")
def vault(pm, gov, rewards, guardian, management, token):
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault)
    vault.initialize(token, gov, rewards, "", "", guardian, management)
    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    vault.setManagement(management, {"from": gov})
    yield vault


@pytest.fixture(scope="function")
def strategy(
    strategist, keeper, vault, Strategy, gov, rewards_contract, rewards_distribution
):
    strategy = strategist.deploy(Strategy, vault)
    strategy.setKeeper(keeper)
    vault.addStrategy(strategy, 10_000, 0, 2 ** 256 - 1, 1_000, {"from": gov})

    # If rewards distribution is over, let's restart it ;)
    if rewards_contract.periodFinish() <= time.time():
        rewards_contract.notifyRewardAmount(
            10_000 * 10 ** 18, {"from": rewards_distribution}
        )

    yield strategy


@pytest.fixture(scope="session")
def RELATIVE_APPROX():
    yield 1e-5
