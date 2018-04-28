# -*- coding: utf-8 -*-

'''
This script initializes the plugin, making it known to QGIS.
'''

__author__ = 'Petr Tsymbarovich'
__date__ = '2018-04-28'
__copyright__ = '(C) 2018 by Petr Tsymbarovich'


# noinspection PyPep8Naming
def classFactory(iface):
    '''Load OmzProcessing class from file OmzProcessing.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    '''

    from .plugin import OmzProcessingPlugin
    return OmzProcessingPlugin()
