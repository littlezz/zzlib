__author__ = 'zz'

import re


class SafeString:
    """
    sanitize string
    """
    dirname_pat = re.compile('\?*\\*\.*<*>*/*\|*')

    def sanitized_dirname(self, value, replace_by=''):
        """replace unsafe char with 'replace_by'
        """
        return self.dirname_pat.sub(replace_by, value)