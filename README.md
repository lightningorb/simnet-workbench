# simnet-workbench

simnet-workbench remotely creates an LND cluster for dev / ops / fun etc. It uses the [fabric3](https://www.fabfile.org/installing.html). If follows the [LND Docker readme](https://github.com/lightningnetwork/lnd/blob/master/docker/README.md), and is somewhat inspired by [cmdruid/regtest-workbench](https://github.com/cmdruid/regtest-workbench).

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


- Clusters created remotely via SSH.
- Automated opening of channels.
- Provides handy aliases (bob, alice etc.)

## Requires

- A modern docker version, e.g 20.10.17
- A modern ubuntu version, e.g 20.04

### Python dependencies

simnet-workbench only requires two depedencies: `fabric` and `simple_chalk`.

```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip3 install -r requirements.txt
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

