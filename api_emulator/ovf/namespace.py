# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# XML Namespace

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
