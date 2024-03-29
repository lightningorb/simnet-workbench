[![test](https://github.com/lightningorb/simnet-workbench/actions/workflows/test.yaml/badge.svg)](https://github.com/lightningorb/simnet-workbench/actions/workflows/test.yaml)

# simnet-workbench

simnet-workbench remotely creates an LND cluster for dev / ops / fun etc. It uses [fabric3](https://www.fabfile.org/installing.html). If follows the [LND Docker readme](https://github.com/lightningnetwork/lnd/blob/master/docker/README.md), and is somewhat inspired by [cmdruid/regtest-workbench](https://github.com/cmdruid/regtest-workbench).

```
                   ┌───────┐
      ┌────────────┤ alice ├─────────────┐
      │            └───────┘             │
      │                                  │
      │                                  │
      │                                  │
      │                                  │
      │                                  │
      │                                  │
      │                                  │
  ┌───┴───┐                          ┌───┴───┐
  │ carol ├──────────────────────────┤  bob  │
  └───────┘                          └───────┘
```

[See Video](https://lnorb.s3.us-east-2.amazonaws.com/simnet.mp4)


- Clusters created remotely via SSH.
- Automated mining of coins (get rich quick).
- Automated opening of balanced channels.
- Provides handy aliases (bob, alice etc.)
- Remote CLI capability.

## Requires

- A modern docker version, e.g 20.10.17
- A modern ubuntu version, e.g 20.04

### Python dependencies

simnet-workbench only requires two depedencies: `fabric` and `simple_chalk`.

```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip3 install -r src/requirements.txt
```

## Running

The simplest and cleanest way is to use the `src/spawn.sh` script to avoid having to mess with long commands in bash.

```bash
$ . src/spawn.sh
```

We source the spawn script as it creates convenience aliases, for example you can run:

```
$ alice --help
$ alice getnetworkinfo
$ alice 'addinvoice --help'
$ alice 'addinvoice --amt 100000'
$ bob 'sendpayment -f --pay_req=<ln...>'
$ bob channelbalance
```

## How does it connect to the host?

The cleanest way to set up your host is with your `~/.ssh/config` file:

```
Host lnd
    HostName xx.xx.xx.xx
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/<my_cert_file>
```

## Can it run on my local machine?

Yes of course. Just strip out the `-H lnd` part of the commands in `spawn.sh`. At some point that'll be implemented properly as a flag.

## SQLite Support

SQLite support was recently added. To enable SQLite simply copy the sample file:

```
$ cp src/sample-lnd.conf src/lnd.conf
```

And enable SQL support by toggling on, in `src/lnd.conf`:

```
db.backend=sqlite
```

# Github actions

The simnet workbench works on Github actions. It only takes about 2 minutes to setup LND, the nodes, connect them in a state where payments can be made. See the github workflow for more details.

Soon these actions will be moved out and refactored so they can be used from any repo.