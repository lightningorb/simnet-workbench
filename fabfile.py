# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2023-02-10 08:00:59
# @Last Modified by:   lnorb.com
# @Last Modified time: 2023-02-10 11:44:48

# Fabric uses PyInvoke. This is a collection of tasks.
from invoke import Collection

# PyInvoke still suffers from annotation related bugs.
from src.clusterlnd.monkey_patch import fix_annotations

fix_annotations()

# We use a bunch of syntax sugar to work with Fabric.
from src.clusterlnd.utils import docker, lncli

# Import LND commands
from src.clusterlnd import lnd

# Declare our command namespace
namespace = Collection(lnd, docker, lncli)
