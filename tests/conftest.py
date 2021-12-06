from brownie import (
  GlobalAccessControl,
  accounts
)
import pytest

DEV_MULTISIG = "0xB65cef03b9B89f99517643226d76e286ee999e77"
TECHOPS_MULTISIG = "0x86cbD0ce0c087b482782c181dA8d191De18C8275"
WAR_ROOM_ACL = "0x6615e67b8B6b6375D38A0A3f937cd8c1a1e96386"


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
  contract.initialize(DEV_MULTISIG, TECHOPS_MULTISIG, WAR_ROOM_ACL, {"from": deployer})

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