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
Redfish Emulator Role Service.
Temporary version, to be removed when AccountService goes dynamic
"""

class AccountService(object):

    def __init__(self):
        self._accounts = { 'Administrator': 'Password',
                           'User': 'Password' }
        self._roles = { 'Administrator': 'Admin',
                        'User': 'ReadOnlyUser' }
        
    def checkPriviledgeLevel(self, user, level):
        if self._roles[user] == level:
            return True
        else: 
            return False
        
    def getPassword(self, username):
        if self._accounts.has_key(username):
            return self._accounts[username]
        else:
            return None
    
    def checkPrivilege(self, privilege, username, errorResponse):
        def wrap(func):
            def inner(*args, **kwargs):
                if self.checkPriviledgeLevel(username(), privilege):
                    return func(*args, **kwargs)
                else:
                    return errorResponse()
            return inner
        return wrap
