# -*- coding: utf-8 -*-

'''
An abstract class for algorithms.
'''

__author__ = 'Petr Tsymbarovich'
__date__ = '2018-05-03'
__copyright__ = '(C) 2018 by Petr Tsymbarovich'


import os.path
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingAlgorithm
from importlib.util import find_spec


class OmzAlgorithm(QgsProcessingAlgorithm):
    '''
    The class implements the algorithm.
    '''

    ICON = None
    DEPENDENCIES = []

    def icon(self):
        '''
        Returns an icon for the algorithm.
        '''
        if self.icon:
            iconpath = os.path.join(os.path.dirname(__file__), OmzAlgorithm.ICON)
            return QIcon(iconpath)
        else:
            return QIcon()

    def group(self):
        '''
        Returns the name of the group this algorithm belongs to.
        '''
        return QCoreApplication.translate('OmzAlgorithm', 'NTs OMZ')

    def groupId(self):
        '''
        Returns the unique ID of the group this algorithm belongs to.
        '''
        return 'ntsomz'

    def canExecute(self):
        '''
        Returns True if the algorithm can execute otherwise
        returns False and an error message.
        '''

        errors = []
        for dep in OmzAlgorithm.DEPENDENCIES:
            if not find_spec(dep):
                errors.append(dep)

        if errors:
            msg = QCoreApplication.translate('OmzAlgorithm', '''\
<p>It requires next Python modules to be installed:</p>
<ul><li>{}</li></ul>
<p>The easiest way to install modules is to use <a href="https://docs.python.org/3/installing/">PIP</a>.</p>
<p>Linux users can also use their package manager (apt, dnf, etc.).</p>
<p>Windows users can use the OSGeo4W installer to manage packages:</p>
<ul>
<li>Run <code>OSGeo4W Shell</code></li>
<li>Type <code>setup</code> and press <code>Enter</code></li>
<li>Select <code>Advanced installation</code> and go to the list of packages and select the required ones</li>
<li>Finally press <code>Next</code> to install the selected packages</li>
</ul>
<p><b>Note</b> that you have to install packages for the Python3. For example: <code>python3-numpy</code>. \
For more information try to search in the Internet something like</p>
<blockquote>python3 install numpy</blockquote>
<p>But replace <code>numpy</code> with the name of the required module.</p>''')
            return False, msg.format('</li><li>'.join(errors))

        return True, ''
