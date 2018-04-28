# -*- coding: utf-8 -*-

'''
This script loads and unloads the plugin and its translations.
'''

import os
import sys
import inspect

from PyQt5.QtCore import QSettings, QLocale, QTranslator, QCoreApplication
from qgis.core import QgsProcessingAlgorithm, QgsApplication
from .provider import OmzProcessingProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class OmzProcessingPlugin(object):

    def __init__(self):
        self.provider = OmzProcessingProvider()

    def initGui(self):
        locale = QLocale(QSettings().value('locale/userLocale'))
        self.translator = QTranslator()
        i18n_dir = os.path.join(cmd_folder, 'i18n')
        if self.translator.load(locale, 'omzprocessing', '_', i18n_dir):
            QCoreApplication.installTranslator(self.translator)
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
