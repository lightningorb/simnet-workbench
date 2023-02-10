# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2023-02-10 08:22:35
# @Last Modified by:   lnorb.com
# @Last Modified time: 2023-02-10 11:58:36

import os
from time import sleep
from pathlib import Path
from functools import lru_cache

from invoke import task
from simple_chalk import chalk

from src.clusterlnd.utils import j, wait, run, sudo, docker, exec, lncli


@task
def start(c, name: str = "", channels: str = ""):
    """
    This is our main function (it's called start to match regtest-workbench).
    Please note this is being run once per node.
    """

    # Create the required volume for the node
    create_volume(c, name)

    # Create the node itself
    create_node(c, name=name)

    # Fund the node with coins
    fund(c, name=name)

    # If we have requested channels
    if channels:
        for channel in channels.split(","):
            # Open the channel from us to them
            open_channel(c, name, channel)
            # Check that the channel was properly created
            check_channel(c, name, channel)


@task
def create_node(c, name: str):
    """
    This creates the node, basically creates the lnd container and runs it.
    """
    with c.cd("lnd/docker"):
        # Here we should called 'docker' instead of run, but fabric has an old bug
        # where sudo can't be called in a cd scope.
        run(
            c,
            f"sudo docker compose run -d --name {name} --volume simnet_lnd_{name}:/root/.lnd lnd",
        )


@task
def get_address(c, name):
    """
    Get a deposit address for the given node.
    """
    address = j(wait(lncli)(c, name, "newaddress np2wkh"))["address"]
    print(chalk.magenta(f"{name} mining address: {address}"))
    return address


@task
def get_pubkey(c, name):
    """
    Get the pubkey for the given node.
    """
    pubkey = j(lncli(c, name, f"getinfo"))["identity_pubkey"]
    print(chalk.magenta(f"{name} pubkey: {pubkey}"))
    return pubkey


@lru_cache(maxsize=0)
def get_ip(c, name):
    """
    Get the IP address of the given node.
    """
    ip = j(docker(c, f"inspect {name}"))[0]["NetworkSettings"]["Networks"][
        "docker_default"
    ]["IPAddress"]
    print(chalk.magenta(f"{name} ip: {ip}"))
    return ip


@task
def fund(c, name: str):
    """
    Mine some coins and send them over to the given node.
    """
    # Get the address of the node
    address = get_address(c, name)
    # Change to the lnd/docker directory
    with c.cd("lnd/docker"):
        # Start the btcd docker container
        run(c, f"sudo MINING_ADDRESS={address} docker compose up -d btcd")
    # Generate 400 coins
    exec(c, "btcd", "/start-btcctl.sh generate 400")
    # Check if the balance is greater than 0
    while True:
        # Get the balance of the wallet
        bal = int(j(lncli(c, name, f"walletbalance"))["total_balance"])
        if bal > 0:
            # Print the confirmed balance
            print(chalk.magenta(f"{name} confirmed balance: {bal:_}"))
            break
        sleep(1)


@task
def open_channel(c, from_name, to_name):
    """
    Open a channel from the given node to the given node.
    """
    # Get the public key of the node to connect to
    to_pk = get_pubkey(c, to_name)
    # Get the IP of the node to connect to
    to_ip = get_ip(c, to_name)
    # Execute the lncli command to connect to the node
    wait(lncli)(c, from_name, f"connect {to_pk}@{to_ip}")
    # Get the list of peers for the node
    peers = [x["pub_key"] for x in j(lncli(c, from_name, f"listpeers"))["peers"]]
    # Print whether the node is connected to the target node
    print(chalk.magenta(f"{from_name} is connected to {to_name}: {to_pk in peers}"))
    # Open a channel to the target node
    lncli(
        c,
        from_name,
        f"openchannel --node_key={to_pk} --local_amt=1000000 --push_amt=500000",
    )
    # Generate 3 blocks in the network
    exec(c, "btcd", "/start-btcctl.sh generate 3")


def check_channel(c, from_name, to_name):
    """
    Check that the channel was properly open.
    """
    # Get the public key of the `to_name` node
    to_pk = get_pubkey(c, to_name)

    # Keep checking for the channel in a loop
    while True:
        # Get the list of channels for the `from_name` node
        channels = [
            x["remote_pubkey"]
            for x in j(lncli(c, from_name, "listchannels"))["channels"]
        ]
        # Check if the `to_name` node is in the list of channels
        created = to_pk in channels
        # If the channel exists, print a message and return
        if created:
            print(
                chalk.blueBright(f"{from_name} has a channel with {to_name}: {created}")
            )
            return
        # Wait for 5 seconds before checking again
        sleep(5)


@task
def create_volume(c, name):
    """
    Create a volume for the given node.
    """
    docker(c, f"volume rm -f simnet_lnd_{name}")
    docker(c, f"volume create simnet_lnd_{name}")


@task
def clone(c):
    """
    Clone LND if the LND directory doesn't already exist
    """
    if not c.run("test -d lnd", warn=True):
        c.run("git clone https://github.com/lightningnetwork/lnd.git")


@task
def build(c, tag="myrepository/lnd-dev"):
    with c.cd("lnd"):
        c.run(f"sudo docker build --tag={tag} -f dev.Dockerfile .")
