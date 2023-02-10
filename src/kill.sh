#!/bin/bash

# @Author: lnorb.com
# @Date:   2023-02-10 11:34:19
# @Last Modified by:   w
# @Last Modified time: 2023-02-10 12:47:20

./simnet-workbench -H lnd docker 'rm -f alice bob carol btcd'
./simnet-workbench -H lnd docker 'rmi lnd'
