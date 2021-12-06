from brownie import (
  GlobalAccessControl,
  accounts
)
import pytest


@pytest.fixture
def deployer():
  return accounts[0]

@pytest.fixture
def rando():
  return accounts[1]

@pytest.fixture
def hacker():
  return accounts[6]

@pytest.fixture
def deployed(deployer):
  contract = GlobalAccessControl.deploy({"from": deployer})
  contract.initialize({"from": deployer})

  return contract
  
@pytest.fixture
def admin(deployed):
  return accounts.at(deployed.DEV_MULTISIG(), force=True)

@pytest.fixture
def tech_ops(deployed):
  return accounts.at(deployed.TECHOPS_MULTISIG(), force=True)

@pytest.fixture
def war_room(deployed):
  return accounts.at(deployed.WAR_ROOM_ACL(), force=True)

@pytest.fixture(scope="module", autouse=True)
def shared_setup(module_isolation):
    pass