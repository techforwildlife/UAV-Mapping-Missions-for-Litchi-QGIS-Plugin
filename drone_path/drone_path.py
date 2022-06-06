# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DronePath
                                 A QGIS plugin
 This plugin draws a drone flight path based on certain required inputs. The paths must be fed into drone mission planning softwares for adding further attributes.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-05-24
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Technology for Wildlife Foundation
        email                : sravanthi@techforwildlife.com
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject
from PyQt5.QtWidgets import QAction,QMessageBox,QTableWidgetItem,QApplication,QFileDialog
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt,QPoint, QRegExp,QPointF
from PyQt5.QtGui import QIcon,QRegExpValidator,QPolygonF
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .drone_path_dialog import DronePathDialog
import os.path
import math

class DronePath:
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
            'DronePath_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Drone Path')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        self.dlg = None
        self.dlg = DronePathDialog()
        
        self.dlg.pushButton.clicked.connect(self.CalculateD)
        self.dlg.pushButton_2.clicked.connect(self.BrowseAOI)
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
        return QCoreApplication.translate('DronePath', message)


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
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/drone_path/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Draw grid lines'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Drone Path'),
                action)
            self.iface.removeToolBarIcon(action)

    def CalculateD(self):
        if (self.dlg.lineEdit_3.text()=='') and (self.dlg.lineEdit.text()==''):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Camera Field Paramaeters Error")
            msg.setText("Please enter Camera Field Parameters and calculate again.")
            msg.setStandardButtons(QMessageBox.Ok )
            return msg.exec_()
        alt = self.dlg.lineEdit.text()
        fov = self.dlg.lineEdit_3.text()
        D = 2*int(alt)*math.tan((float(fov))/2)
        self.dlg.lineEdit_4.setText(str(D))
        
    def BrowseAOI(self):
        aoi = QFileDialog.getOpenFileName(self.dlg, "Select AOI file ","", '*.shp')
        self.dlg.lineEdit_5.setText(aoi[0])
        
    def loadAOI(self):
        
    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = DronePathDialog()
            
        self.dlg.pushButton.clicked.connect(self.CalculateD)
        self.dlg.pushButton_2.clicked.connect(self.BrowseAOI)   
        self.dlg.lineEdit_4.setReadOnly(True)
        self.dlg.lineEdit.clear()
        reg_ex = QRegExp("(\d\d\d\.[0-9]{,2})") #3 digits and 2 decimals
        input_validator = QRegExpValidator(reg_ex)
        self.dlg.lineEdit.setValidator(input_validator)
        self.dlg.lineEdit_3.clear()
        reg_ex = QRegExp("(\d\.[0-9]{,2})") #two digit with two decimals
        input_validator = QRegExpValidator(reg_ex)
        self.dlg.lineEdit_3.setValidator(input_validator)
        self.dlg.lineEdit_2.clear()
        reg_ex = QRegExp("(\d{2})") #two digit with two decimals
        input_validator = QRegExpValidator(reg_ex)
        self.dlg.lineEdit_2.setValidator(input_validator)   
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
