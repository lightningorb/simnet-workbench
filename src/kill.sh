#!/bin/bash

# @Author: lnorb.com
# @Date:   2023-02-10 11:34:19
# @Last Modified by:   w
# @Last Modified time: 2023-02-10 11:34:53

./clusterlnd -H lnd docker 'rm -f alice bob carol btcd'
./clusterlnd -H lnd docker 'rmi lnd'
