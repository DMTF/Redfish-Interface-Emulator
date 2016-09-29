#
# Copyright (c) 2016 Intel Corporation. All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# Neither the name of the Distributed Management Task Force (DMTF) nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""
Utilities used through out the library
"""
import os
import json
import datetime
from functools import wraps


def timestamp():
    """
    Return an ISO timestamp with milliseconds removed
    """
    return datetime.datetime.now().isoformat().split('.')[0]


def process_id(odata_id, base_dir, rest_base):
    """
    Gets the index.html associated with the odata_id
    """
    index_dir = os.path.abspath(os.path.join(
        base_dir, odata_id.split(rest_base)[-1]))
    index_html = os.path.join(index_dir, 'index.json')
    assert os.path.exists(index_html), \
        '"{0}" does not exist'.format(index_html)
    with open(index_html, 'r') as f:
        index = json.load(f)
    return index


def check_initialized(func):
    """
    Wrapper function to check if the initialized member variable
    has been set to True in a class.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        cls = args[0]
        if cls.initialized:
            raise RuntimeError('Object has already been initialized')
        return func(*args, **kwargs)
    return wrapper
