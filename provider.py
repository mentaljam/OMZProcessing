# -*- coding: utf-8 -*-

'''
This script initializes the provider of the algorithms.
'''

import os.path
from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingProvider
from .algs.densitymap import DensityMapAlgorithm


class OmzProcessingProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

        # Load algorithms
        self.alglist = [
            DensityMapAlgorithm()
        ]

    def unload(self):
        '''
        Unloads the provider.
        '''
        pass

    def loadAlgorithms(self):
        '''
        Loads all algorithms belonging to this provider.
        '''
        for alg in self.alglist:
            self.addAlgorithm(alg)

    def id(self):
        '''
        Returns the unique provider id, used for identifying the provider.
        '''
        return 'ntsomz'

    def name(self):
        '''
        Returns the provider name, which is used to describe the provider
        within the GUI.
        '''
        return self.tr('NTs OMZ')

    def longName(self):
        '''
        Returns the a longer version of the provider name.
        '''
        return self.tr('NTs OMZ algorithms')

    def icon(self):
        iconpath = os.path.join(os.path.dirname(__file__), 'icon.png')
        return QIcon(iconpath)
