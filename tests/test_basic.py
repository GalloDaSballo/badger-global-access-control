import brownie

"""
Test:
- Is dev multisig admin
- Can they change roles
- Can they pause
- Add pauser
  - Can they pause
  - They cannot unpause

"""

def test_admin_is_admin(deployed, admin):
  """
    Little basic test to prove OZ works
  """
  assert deployed.hasRole(deployed.DEFAULT_ADMIN_ROLE(), admin) == True

def test_setup_initialized_roles(deployed, admin, tech_ops, war_room, rando, hacker):
  """
    Proves we set up the basic roles from initialize
  """

  ## Verify dev multi is admin
  ## Verify dev multi is pauser
  ## Verify dev multi is unpauser
  ## Verify dev multi is blacklister
  ## Verify dev multi is not blacklisted
  assert deployed.hasRole(deployed.DEFAULT_ADMIN_ROLE(), admin) == True
  assert deployed.hasRole(deployed.PAUSER_ROLE(), admin) == True
  assert deployed.hasRole(deployed.UNPAUSER_ROLE(), admin) == True
  assert deployed.hasRole(deployed.BLACKLIST_MANAGER_ROLE(), admin) == True
  assert deployed.hasRole(deployed.BLACKLISTED_ROLE(), admin) == False


  ## Verify techops is pauser
  ## Verify techops is blacklister
  ## Verify techops is not admin
  ## Verify techops is not unpauser
  ## Verify techops is not blacklisted
  assert deployed.hasRole(deployed.DEFAULT_ADMIN_ROLE(), tech_ops) == False
  assert deployed.hasRole(deployed.PAUSER_ROLE(), tech_ops) == True
  assert deployed.hasRole(deployed.UNPAUSER_ROLE(), tech_ops) == False
  assert deployed.hasRole(deployed.BLACKLIST_MANAGER_ROLE(), tech_ops) == True
  assert deployed.hasRole(deployed.BLACKLISTED_ROLE(), tech_ops) == False

  ## Verify war_room is not admin
  ## Verify war_room is pauser
  ## Verify war_room is not unpauser
  ## Verify war_room is not blacklister
  ## Verify war_room is not blacklisted
  assert deployed.hasRole(deployed.DEFAULT_ADMIN_ROLE(), war_room) == False
  assert deployed.hasRole(deployed.PAUSER_ROLE(), war_room) == True
  assert deployed.hasRole(deployed.UNPAUSER_ROLE(), war_room) == False
  assert deployed.hasRole(deployed.BLACKLIST_MANAGER_ROLE(), war_room) == False
  assert deployed.hasRole(deployed.BLACKLISTED_ROLE(), war_room) == False
  

  ## Verify random user is not admin
  ## Verify random user is not pauser
  ## Verify random user is not unpauser
  ## Verify random user is not blacklister

  assert deployed.hasRole(deployed.DEFAULT_ADMIN_ROLE(), rando) == False
  assert deployed.hasRole(deployed.PAUSER_ROLE(), rando) == False
  assert deployed.hasRole(deployed.UNPAUSER_ROLE(), rando) == False
  assert deployed.hasRole(deployed.BLACKLIST_MANAGER_ROLE(), rando) == False
  assert deployed.hasRole(deployed.BLACKLISTED_ROLE(), rando) == False

  ## Same for hacker, no settings as of now so all False
  assert deployed.hasRole(deployed.DEFAULT_ADMIN_ROLE(), hacker) == False
  assert deployed.hasRole(deployed.PAUSER_ROLE(), hacker) == False
  assert deployed.hasRole(deployed.UNPAUSER_ROLE(), hacker) == False
  assert deployed.hasRole(deployed.BLACKLIST_MANAGER_ROLE(), hacker) == False
  assert deployed.hasRole(deployed.BLACKLISTED_ROLE(), hacker) == False

def test_pause_unpause_permissions_work_with_roles(deployed, admin, tech_ops, rando):
    ## If rando can't pause
    assert deployed.hasRole(deployed.PAUSER_ROLE(), rando) == False
    
    ## Then pausing should revert
    with brownie.reverts():
      deployed.pause({"from": rando})

    ## If tech_ops can pause
    assert deployed.hasRole(deployed.PAUSER_ROLE(), tech_ops) == True

    ## And we haven't paused yet
    assert deployed.paused() == False

    ## Calling pause pausues
    deployed.pause({"from": tech_ops})

    assert deployed.paused() == True

    ## If we can't unpause 
    assert deployed.hasRole(deployed.UNPAUSER_ROLE(), tech_ops) == False

    ## Then it reverts
    with brownie.reverts():
      deployed.unpause({"from": tech_ops})

    ## Same for rando
    with brownie.reverts():
      deployed.unpause({"from": rando})

    ## If we do have the permission to unpause
    assert deployed.hasRole(deployed.UNPAUSER_ROLE(), admin) == True
    deployed.unpause({"from": admin})

    ## Then we can unpause
    assert deployed.paused() == False


def test_blacklist(deployed, admin, tech_ops, war_room, hacker, rando):
  # Verify setting blacklist works for techops and admin
  # And that after setup the list is enforced as expected

  assert deployed.isBlacklisted(rando) == False
  assert deployed.isBlacklisted(hacker) == False

  ## Admin and tech_ops can blacklist the hacker
  deployed.grantRole(deployed.BLACKLISTED_ROLE(), rando, {"from": admin})
  deployed.grantRole(deployed.BLACKLISTED_ROLE(), hacker, {"from": tech_ops})

  assert deployed.isBlacklisted(rando) == True
  assert deployed.isBlacklisted(hacker) == True

  ## The hacker can't remove the role by themselves
  with brownie.reverts():
    deployed.revokeRole(deployed.BLACKLISTED_ROLE(), hacker, {"from": hacker})

  ## But the tech_ops and admin can
  deployed.revokeRole(deployed.BLACKLISTED_ROLE(), rando, {"from": admin})
  assert deployed.isBlacklisted(rando) == False

  deployed.grantRole(deployed.BLACKLISTED_ROLE(), rando, {"from": tech_ops})
  assert deployed.isBlacklisted(rando) == True
  deployed.revokeRole(deployed.BLACKLISTED_ROLE(), rando, {"from": tech_ops})
  assert deployed.isBlacklisted(rando) == False


