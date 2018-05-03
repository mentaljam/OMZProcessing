# -*- coding: utf-8 -*-

'''
This algorithm takes a vector layer of polygons and calculates a density map.
'''

__author__ = 'Petr Tsymbarovich'
__date__ = '2018-04-28'
__copyright__ = '(C) 2018 by Petr Tsymbarovich'


import os.path
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsRasterFileWriter,
    Qgis,
)
from PIL import (
    Image,
    ImageDraw,
)
import numpy


class DensityMapAlgorithm(QgsProcessingAlgorithm):
    '''
    The class implements the algorithm.
    '''

    INPUT = 'INPUT'
    RESOLUTION = 'RESOLUTION'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        '''
        Returns a translatable string with the self.tr() function.
        '''
        return QCoreApplication.translate('DensityMapAlgorithm', string)

    def createInstance(self):
        return DensityMapAlgorithm()

    def name(self):
        '''
        Returns the algorithm name, used for identifying the algorithm.
        '''
        return 'densitymap'

    def displayName(self):
        '''
        Returns the translated algorithm name.
        '''
        return self.tr('Density Map')

    def icon(self):
        iconpath = os.path.join(os.path.dirname(__file__), 'densitymap.png')
        return QIcon(iconpath)

    def group(self):
        '''
        Returns the name of the group this algorithm belongs to.
        '''
        return self.tr('NTs OMZ')

    def groupId(self):
        '''
        Returns the unique ID of the group this algorithm belongs to.
        '''
        return 'ntsomz_scripts'

    def shortHelpString(self):
        '''
        Returns the help message to be shown in the interface.
        '''
        return self.tr('''\
<p>This algorithm takes a vector layer of polygons and calculates a density map.</p>
<h3>Input layer</h3>
<p>A vector layer of polygons to process.</p>
<h3>Output resolution</h3>
<p>Resolution of the output raster. <b>Pay attention:</b> values of the CRS of input layer are used.</p>
<h3>Density map</h3>
<p>An output raster for saving the resulting density map.</p>\
''')

    def initAlgorithm(self, config=None):
        '''
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        '''

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.RESOLUTION,
                self.tr('Output resolution'),
                QgsProcessingParameterNumber.Double,
                1.0,
                False,
                0.000001,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr('Density map')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        '''
        Here is where the processing itself takes place.
        '''

        source = self.parameterAsSource(
            parameters,
            self.INPUT,
            context
        )
        resolution = self.parameterAsDouble(
            parameters,
            self.RESOLUTION,
            context
        )
        outpath = self.parameterAsOutputLayer(
            parameters,
            self.OUTPUT,
            context
        )
        result = {self.OUTPUT: outpath}

        # Compute the number of steps to display within the progress bar
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        
        # Calculate the output extent
        extent = source.sourceExtent()
        xmin  = extent.xMinimum()
        ymax  = extent.yMaximum()
        xsize = int((extent.xMaximum() - xmin) / resolution) + 1
        ysize = int((ymax - extent.yMinimum()) / resolution) + 1
        if xsize > 50000 or ysize > 50000:
            feedback.reportError(self.tr('Output raster size is too big: {}x{}!').format(xsize, ysize), True)
            # fatalError = true has no effect 
            feedback.cancel()
            return result
        feedback.pushConsoleInfo(self.tr('Output raster size is {}x{}').format(xsize, ysize))

        # Create output buffer
        density = numpy.zeros((ysize, xsize), dtype=numpy.uint16)
        # Create geometry mask buffer
        mask = Image.new('1', (xsize, ysize), 0)
        draw = ImageDraw.Draw(mask)

        # Iterate over features from source
        features = source.getFeatures()
        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                return result

            # Convert feature geometry to the image coordinates
            geometry = feature.geometry()
            geometry.convertToSingleType()
            polygon = geometry.asPolygon()
            points = []
            for p in polygon:
                for x, y in p:
                    x = (x - xmin) / resolution
                    y = (ymax - y) / resolution
                    points.append((x, y))

            # Generate geometry mask
            draw.polygon(points, 1)
            # Add geometry mask to the result raster
            density = numpy.add(density, numpy.array(mask))
            # Reset the mask
            draw.rectangle([0, 0, xsize, ysize], fill=0)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        # Write output raster
        writer = QgsRasterFileWriter(outpath)
        provider = writer.createOneBandRaster(Qgis.UInt16, xsize, ysize, extent, source.sourceCrs())
        provider.write(density.astype('H').tostring(), 1, xsize, ysize, 0, 0)
        density = None
        draw = None
        mask = None

        return result
