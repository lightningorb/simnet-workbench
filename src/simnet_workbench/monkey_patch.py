# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-25 11:17:33
# @Last Modified by:   lnorb.com
# @Last Modified time: 2023-02-10 08:36:09

# Import the patch function from the unittest.mock library
from unittest.mock import patch

# Import the getfullargspec and ArgSpec functions from the inspect library
from inspect import getfullargspec, ArgSpec

# Import the invoke library
import invoke


def fix_annotations():
    """
    Pyinvoke doesnt accept annotations by default, this fix that
    Based on: https://github.com/pyinvoke/invoke/pull/606
    """

    # A function that patches the getfullargspec function in the inspect library
    def patched_inspect_getargspec(func):
        # Get the argument specifications of the passed function
        spec = getfullargspec(func)
        # Return an ArgSpec object using the first 4 items of the returned tuple
        return ArgSpec(*spec[0:4])

    # Store the original argspec property of the Task class in the invoke library
    org_task_argspec = invoke.tasks.Task.argspec

    # A function that patches the argspec property of the Task class in the invoke library
    def patched_task_argspec(*args, **kwargs):
        # Use the patch function to replace the getargspec function in the inspect library
        # with the patched_inspect_getargspec function
        with patch(target="inspect.getargspec", new=patched_inspect_getargspec):
            # Return the result of calling the original argspec property
            return org_task_argspec(*args, **kwargs)

    # Replace the argspec property of the Task class in the invoke library with the patched_task_argspec function
    invoke.tasks.Task.argspec = patched_task_argspec
