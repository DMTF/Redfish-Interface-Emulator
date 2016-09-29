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
XML Namespace
"""
import re


class Namespace(object):
    """
    XML Namespace Class

    This class is meant to be used with the xml.etree.ElementTree module.
    Its purpose is to provide the tag() method which will replace any {<tag>}
    elements in the string with the corrent URI, provided it is in the
    namespace.

    Each prefix is simple an element in a dictionary, i.e. {<prefix>: <uri>}.

    See the tag method for the expected tag string.
    """
    def __init__(self, prefixes=None):
        """
        Namespace Constructor

        Arguments:
            prefixes - Dictionary of initial prefixes to load
        """
        self.prefixes = {}
        self.reg = re.compile('(?:.+|)(?:\{)(.+)(?:\}.+)')

        if prefixes is not None:
            self.register_prefixes(prefixes)

    def register_prefixes(self, prefixes):
        """
        Register more prefixes into the namespace.

        Throws an AssertionError exception if prefixes is not a dictionary.

        Arguments:
            prefixes -- Dictionary of prefixes to add
        """
        assert isinstance(prefixes, dict), 'prefixes must be a dictionary'
        self.prefixes.update(prefixes)

    def tag(self, xpath):
        """
        Generate the correct xpath for a tag. This method expects the xpath
        to have the namespaces defined in the following way: {<prefix>}.

        Example xPath:
            .//{xmlns}MyTag

        If the xmlns URI is: http://www.example.org/mytags, then the resulting
        xpath will be: .//{http://www.example.org/mytags}MyTag

        Arguments:
            xpath - xPath in the format described above to add in prefixes to
        """
        prefixes = self.reg.findall(xpath)
        kwargs = {}

        for p in prefixes:
            kwargs[p] = '{' + self.prefixes[p] + '}'

        return xpath.format(**kwargs)
