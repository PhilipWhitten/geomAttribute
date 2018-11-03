# -*- coding: utf-8 -*-
"""
/***************************************************************************
 geomAttribute
                                 A QGIS plugin
 An attribute table with geometry descriptions
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-09-14
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philip Whitten
        email                : philipwhitten@wollondilly.nsw.gov.au
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.utils import *
from qgis.gui import QgsAttributeTableModel, QgsAttributeTableFilterModel
from .modelVectorLayers import *


# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .geomAttribute_window import geomAttributeWindow
import os.path
__version__ = '1.0.0'

class geomAttribute:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'geomAttribute_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Geometry Attribute Table')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'geomAttribute')
        self.toolbar.setObjectName(u'geomAttribute')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('geomAttribute', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/geomAttribute/icons/attribute_table.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Geometry Attribute Table'),
            callback=self.run,
            parent=self.iface.mainWindow())
        icon_modelData = ':/plugins/geomAttribute/icons/model_data.png'
        self.add_action(
            icon_modelData,
            text=self.tr(u'Load Model Data'),
            callback=self.addModelData,
            add_to_toolbar=False,
            parent=self.iface.mainWindow()
        )
        # self.addModelData_action = QAction(QIcon(icon_modelData), u"Load Model Data", parent=self.iface.mainWindow())
        # self.iface.addPluginToMenu("&Geometry Attribute Table", self.addModelData_action)
        # self.addModelData_action.triggered.connect(self.addModelData)

    def addModelData(self):
        #Add Dialog box for multi_lines##################################################################################
        QMessageBox.warning(None, "Message", "found addModelData")
        QgsProject.instance().addMapLayer(createMultiLines())
        QgsProject.instance().addMapLayer(createMultiPoints())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Geometry Attribute Table'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        self.layer = self.iface.activeLayer()
        self.canvas = self.iface.mapCanvas()

        # Create the dialog window (after translation) and keep reference
        self.window = geomAttributeWindow()

        #look for help icon clicks
        self.window.actionHelp.triggered.connect(self.helpPage)


        ## Add virtual field to layer

        from .parseQGISGeometry import layerAddVirtualGeometryField

        #the try/except tests that the layer is a vector layer.
        try:
            layerAddVirtualGeometryField(self.layer)

            #######################################################self.setWindowTitle('First Attribute Table')

            # create a cache of the vector layer data of size 10000
            self.vector_layer_cache = QgsVectorLayerCache(self.layer, 10000)
            # cache geometry is true by default (print(self.vector_layer_cache.cacheGeometry()))

            # QgsAttributeTableModel is a subclass of QAbstractTableModel
            self.attribute_table_model = QgsAttributeTableModel(self.vector_layer_cache)

            self.attribute_table_model.loadLayer()

            self.attribute_table_filter_model = QgsAttributeTableFilterModel(
            self.iface.mapCanvas(), self.attribute_table_model)
            # The QgsAttributeTableFilterModel() is used to synchronize any selection.  Probably some
            # form of custom model to reduce duplication of data.

            self.attribute_table_view = self.window.tableView #The table view is instantiated via a promotion in QT Designer

            self.attribute_table_view.setModel(self.attribute_table_filter_model)
            # MyDelegate class below is used to put symbols and colors into the geometry column.
            self.attribute_table_view.setItemDelegateForColumn(self.layer.geometryIndex, myDelegate(self.attribute_table_view))

            # show the dialog
            self.window.show()

        except AttributeError:
            QMessageBox.warning(None, 'Warning', 'This tool will only work on vector layers')

    def helpPage(self):
        """Opens the help html file in a web browser.  This requires an internet connection"""
        url = QUrl('https://philipwhitten.github.io/geomAttribute/')
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open Help Page', 'Could not open Help Page.  The help page requires an internet connection.')

########################################################################################################################
class myDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    # class method for painting geometry row attributes.  Where is this method called?
    def paint(self, painter, option, index):
        '''option is a QStyleOptionViewItem, painter is a QPainter object'''

        value = index.data(Qt.DisplayRole)

        iconDict = {
            "MultiPoint": "point_2x",
            "Point": 'point_1x',
            "MultiLine": 'line_2x',
            "Line": 'line_1x',
            "MultiPolygon": 'polygon_2x',
            "Polygon": 'polygon_1x'
        }

        #for iconKey in iconDict:
        geometry = next(filter(value.__contains__, iconDict.keys()), None)
        if geometry is not None:
            icon = QIcon(':/plugins/geomAttribute/icons/{}.png'.format(iconDict.get(geometry)))
            icon.paint(painter, option.rect, Qt.AlignCenter)
        else:
            # set background color
            painter.setPen(QPen(Qt.NoPen))
            backgroundColor = Qt.lightGray
            geometry = next(filter(value.__eq__, ['Null', 'Empty']), None)
            if geometry is not None:
                if value.__eq__('Null'):
                    backgroundColor = Qt.red
                else:
                    backgroundColor = Qt.darkYellow
            painter.setBrush(backgroundColor)
            painter.drawRect(option.rect)
            # set text color - order is important.  If done before background color will not show
            painter.setPen(QPen(Qt.black))

            painter.drawText(option.rect, Qt.AlignCenter, value)

#######################################################################################################################







