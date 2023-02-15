# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2023-02-10 08:00:59
# @Last Modified by:   lnorb.com
# @Last Modified time: 2023-02-10 12:46:33

# Fabric uses PyInvoke. This is a collection of tasks.
from invoke import Collection

# PyInvoke still suffers from annotation related bugs.
from src.simnet_workbench.monkey_patch import fix_annotations

fix_annotations()

# We use a bunch of syntax sugar to work with Fabric.
from src.simnet_workbench.utils import docker, lncli, run, test

# Import LND commands
from src.simnet_workbench import lnd

# Declare our command namespace
namespace = Collection(lnd, docker, lncli, run, test)
