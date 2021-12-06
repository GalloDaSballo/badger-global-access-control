import time

from brownie import (
    accounts,
    network,
    GlobalAccessControl,
    AdminUpgradeabilityProxy
)
import click
from rich.console import Console

console = Console()

sleep_between_tx = 1

DEV_MULTISIG = "0xB65cef03b9B89f99517643226d76e286ee999e77"
TECHOPS_MULTISIG = "0x86cbD0ce0c087b482782c181dA8d191De18C8275"
WAR_ROOM_ACL = "0x6615e67b8B6b6375D38A0A3f937cd8c1a1e96386"
proxyAdmin = "0x20Dce41Acca85E8222D6861Aa6D23B6C941777bF"

def main():
    args = [DEV_MULTISIG, TECHOPS_MULTISIG, WAR_ROOM_ACL]

    dev = connect_account()

    gac_logic = GlobalAccessControl.deploy({"from": dev})
    time.sleep(sleep_between_tx)
    console.print("[green]Gac Logic was deployed at: [/green]", gac_logic.address)


    gac_proxy = AdminUpgradeabilityProxy.deploy(
        gac_logic,
        proxyAdmin,
        gac_logic.initialize.encode_input(*args),
        {"from": dev}
    )
    time.sleep(sleep_between_tx)

    ## We delete from deploy and then fetch again so we can interact
    AdminUpgradeabilityProxy.remove(gac_proxy)
    gac_proxy = GlobalAccessControl.at(gac_proxy.address)

    console.print("[green]Gac Proxy was deployed at: [/green]", gac_proxy.address)

    return gac_proxy



def connect_account():
    click.echo(f"You are using the '{network.show_active()}' network")
    dev = accounts.load(click.prompt("Account", type=click.Choice(accounts.load())))
    click.echo(f"You are using: 'dev' [{dev.address}]")
    return dev
