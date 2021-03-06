from os import path
from core.main import  QtGui,QtCore
from datetime import datetime
from core.utils import Refactor
from collections import OrderedDict
from core.utility.threads import ThreadPopen
from core.widgets.docks.dockmonitor import (
    dockAreaAPI,dockUrlMonitor,dockCredsMonitor,dockPickleProxy,dockTCPproxy
)
from core.widgets.pluginssettings import PickleProxySettings
from core.utility.collection import SettingsINI
from plugins.external.scripts import *
from functools import partial
from plugins.analyzers import *
import core.utility.constants as C
from core.widgets.customiseds import AutoGridLayout
load_plugins = True
try:
    from plugins.extension import *
except ImportError:
    load_plugins = False
"""
Description:
    This program is a core for wifi-pickle.py. file which includes functionality
    for pickle-proxy,pumokin-monitor,pickle-settings tab.

Copyright:
    Copyright (C) 2018-2019 Shane W. Scott GoVanguard Inc.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

class StatusAccessPoint(QtGui.QVBoxLayout):
    ''' dashboard  infor Acccess Point '''
    def __init__(self,mainWindow ):
        QtGui.QVBoxLayout.__init__(self)
        self.mainLayout = QtGui.QFormLayout()
        self.main_method = mainWindow

        self.scrollwidget = QtGui.QWidget()
        self.scrollwidget.setLayout(self.mainLayout)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollwidget)
        self.split_window = QtGui.QHBoxLayout()

        guageWindow = QtGui.QGridLayout()
        self.currentThreadLabel = QtGui.QLabel('0')
        currentthread = self.create_info_box('CURRENT THREADS', 'infor',
            self.currentThreadLabel)

        self.sectionTimeLabel = QtGui.QLabel('00:00')
        currentTime = self.create_info_box('UPTIME', 'infor', self.sectionTimeLabel)
        guageWindow.addLayout(currentthread, 1, 1)
        guageWindow.addLayout(currentTime, 0, 1)

        self.AP_name = QtGui.QLabel(self.main_method.EditApName.text())
        self.AP_BSSID = QtGui.QLabel(self.main_method.EditApBSSID.text())
        self.AP_Channel = QtGui.QLabel(self.main_method.EditApChannel.text())
        self.AP_NetworkApdater = QtGui.QLabel(self.main_method.selectCard.currentText())
        self.AP_ROUTER = QtGui.QLabel(self.main_method.DHCP['router'])
        self.AP_DHCP_range = QtGui.QLabel(self.main_method.DHCP['range'])
        self.AP_Security  = QtGui.QLabel('')
        self.update_security_label(self.main_method.GroupApPassphrase.isChecked())

        self.group_AccessPoint = QtGui.QGroupBox()
        self.form_window = AutoGridLayout()
        self.form_window.setSpacing(10)
        self.group_AccessPoint.setTitle('Access Point')
        self.form_window.addNextWidget(QtGui.QLabel('AP Name:'))
        self.form_window.addNextWidget(self.AP_name)
        self.form_window.addNextWidget(QtGui.QLabel('BSSID:'))
        self.form_window.addNextWidget(self.AP_BSSID)
        self.form_window.addNextWidget(QtGui.QLabel('Channel:'))
        self.form_window.addNextWidget(self.AP_Channel)
        self.form_window.addNextWidget(QtGui.QLabel('Network Adapter:'))
        self.form_window.addNextWidget(self.AP_NetworkApdater)
        self.form_window.addNextWidget(QtGui.QLabel('Router:'))
        self.form_window.addNextWidget(self.AP_ROUTER)
        self.form_window.addNextWidget(QtGui.QLabel('DHCP:'))
        self.form_window.addNextWidget(self.AP_DHCP_range)
        self.form_window.addNextWidget(QtGui.QLabel('Security Password:'))
        self.form_window.addNextWidget(self.AP_Security)
        self.form_window.addItem(QtGui.QSpacerItem(40, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        self.group_AccessPoint.setLayout(self.form_window)

        self.split_window.addWidget(self.group_AccessPoint)
        self.split_window.addLayout(guageWindow)

        self.mainLayout.addRow(self.split_window)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.scroll)
        self.addLayout(self.layout)

    def update_labels(self):
        self.AP_name.setText(self.main_method.EditApName.text())
        self.AP_BSSID.setText(self.main_method.EditApBSSID.text())
        self.AP_Channel.setText(self.main_method.EditApChannel.text())
        self.AP_NetworkApdater.setText(self.main_method.selectCard.currentText())
        self.AP_ROUTER.setText(self.main_method.DHCP['router'])
        self.AP_DHCP_range.setText(self.main_method.DHCP['range'])
        self.update_security_label(self.main_method.GroupApPassphrase.isChecked())

    def start_timer(self):
        self.timer = QtCore.QTimer()
        self.now = 0
        self.update_timer()
        self.timer.timeout.connect(self.tick_timer)
        self.timer.start(1000)

    def update_timer(self):
        self.runtime = ('%d:%02d' % (self.now / 60, self.now % 60))
        self.sectionTimeLabel.setText(self.runtime)
        self.currentThreadLabel.setText(str(len(self.main_method.Apthreads['RougeAP'])-1))

    def tick_timer(self):
        self.now += 1
        self.update_timer()

    def stop_timer(self):
        self.timer.stop()
        self.sectionTimeLabel.setText('00:00')
        self.currentThreadLabel.setText('0')

    def update_security_label(self, bool):
        if bool:
            self.AP_Security.setText('[ON]')
            self.AP_Security.setStyleSheet('QLabel {  color : green; }')
        else:
            self.AP_Security.setText('[OFF]')
            self.AP_Security.setStyleSheet('QLabel {  color : #df1f1f; }')

    def create_info_box(self, labelText, objectName, valueLabel):
        infoBox = QtGui.QVBoxLayout()
        infoBox.setSpacing(0)
        label = QtGui.QLabel(labelText)
        label.setObjectName('label')
        valueLabel.setAlignment(QtCore.Qt.AlignCenter)
        valueLabel.setObjectName(objectName)
        infoBox.addWidget(label)
        infoBox.addWidget(valueLabel)
        return infoBox

class PacketsSniffer(QtGui.QVBoxLayout):
    ''' settings  Transparent Proxy '''
    sendError = QtCore.pyqtSignal(str)
    def __init__(self, main_method, parent = None):
        super(PacketsSniffer, self).__init__(parent)
        self.mainLayout = QtGui.QVBoxLayout()
        self.config = SettingsINI(C.TCPPROXY_INI)
        self.plugins = []
        self.main_method = main_method
        self.bt_SettingsDict = {}
        self.check_PluginDict = {}
        self.search_all_ProxyPlugins()
        #scroll area
        self.scrollwidget = QtGui.QWidget()
        self.scrollwidget.setLayout(self.mainLayout)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollwidget)

        self.tabcontrol = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.page_1 = QtGui.QVBoxLayout(self.tab1)
        self.page_2 = QtGui.QVBoxLayout(self.tab2)
        self.tableLogging  = dockTCPproxy()

        self.tabcontrol.addTab(self.tab1, 'Plugins')
        self.tabcontrol.addTab(self.tab2, 'Logging')

        self.TabPlugins = QtGui.QTableWidget()
        self.TabPlugins.setColumnCount(3)
        self.TabPlugins.setRowCount(len(self.plugins))
        self.TabPlugins.resizeRowsToContents()
        self.TabPlugins.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.TabPlugins.horizontalHeader().setStretchLastSection(True)
        self.TabPlugins.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.TabPlugins.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.TabPlugins.verticalHeader().setVisible(False)
        self.TabPlugins.verticalHeader().setDefaultSectionSize(27)
        self.TabPlugins.setSortingEnabled(True)
        self.THeaders = OrderedDict([('Plugins', []), ('Author', []), ('Description', [])])
        self.TabPlugins.setHorizontalHeaderLabels(list(dict(self.THeaders).keys()))
        self.TabPlugins.horizontalHeader().resizeSection(0, 158)
        self.TabPlugins.horizontalHeader().resizeSection(1, 120)

        self.page_1.addWidget(self.TabPlugins)
        self.page_2.addWidget(self.tableLogging)
        # get all plugins and add into TabWidget
        Headers = []
        for plugin in self.plugins:
            self.bt_SettingsDict[plugin.Name] = QtGui.QPushButton(plugin.Author)
            self.check_PluginDict[plugin.Name] = QtGui.QCheckBox(plugin.Name)
            self.check_PluginDict[plugin.Name].setObjectName(plugin.Name)
            self.check_PluginDict[plugin.Name].clicked.connect(partial(self.setPluginOption, plugin.Name))
            self.THeaders['Plugins'].append(self.check_PluginDict[plugin.Name])
            self.THeaders['Author'].append({'name': plugin.Name})
            self.THeaders['Description'].append(plugin.Description)
        for n, key in enumerate(self.THeaders.keys()):
            Headers.append(key)
            for m, item in enumerate(self.THeaders[key]):
                if type(item) == type(QtGui.QCheckBox()):
                    self.TabPlugins.setCellWidget(m, n, item)
                elif type(item) == type(dict()):
                    self.TabPlugins.setCellWidget(m, n, self.bt_SettingsDict[item['name']])
                else:
                    item = QtGui.QTableWidgetItem(item)
                    self.TabPlugins.setItem(m, n, item)
        self.TabPlugins.setHorizontalHeaderLabels(list(dict(self.THeaders).keys()))

        # check status all checkbox plugins
        for box in self.check_PluginDict.keys():
            self.check_PluginDict[box].setChecked(self.config.get_setting('plugins', box, format=bool))

        self.mainLayout.addWidget(self.tabcontrol)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.scroll)
        self.addLayout(self.layout)

    def setPluginOption(self, name, status):
        ''' get each plugins status'''
        # enable realtime disable and enable plugin
        if self.main_method.FSettings.Settings.get_setting('accesspoint', 'statusAP', format=bool):
            self.main_method.Thread_TCPproxy.disablePlugin(name, status)
        self.config.set_setting('plugins', name, status)

    def search_all_ProxyPlugins(self):
        ''' load all plugins function '''
        plugin_classes = default.PSniffer.__subclasses__()
        for p in plugin_classes:
            if p().Name != 'httpCap':
                self.plugins.append(p())

class ImageCapture(QtGui.QVBoxLayout):
    ''' settings Image capture '''
    sendError = QtCore.pyqtSignal(str)
    def __init__(self,main_method,parent = None):
        super(ImageCapture, self).__init__(parent)
        self.mainLayout = QtGui.QVBoxLayout()
        self.main_method = main_method
        #scroll area
        self.scrollwidget = QtGui.QWidget()
        self.scrollwidget.setLayout(self.mainLayout)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollwidget)
        self.imagesList = []

        self.THUMBNAIL_SIZE = 146
        self.SPACING = 8
        self.IMAGES_PER_ROW = 4
        self.TableImage = QtGui.QTableWidget()
        self.TableImage.setIconSize(QtCore.QSize(146, 146))
        self.TableImage.setColumnCount(self.IMAGES_PER_ROW)
        self.TableImage.setGridStyle(QtCore.Qt.NoPen)

        self.TableImage.verticalHeader().setDefaultSectionSize(self.THUMBNAIL_SIZE + self.SPACING)
        self.TableImage.verticalHeader().hide()
        self.TableImage.horizontalHeader().setDefaultSectionSize(self.THUMBNAIL_SIZE + self.SPACING)
        self.TableImage.horizontalHeader().hide()

        self.TableImage.setMinimumWidth((self.THUMBNAIL_SIZE + self.SPACING) * self.IMAGES_PER_ROW + (self.SPACING * 2))
        self.imageListPath = OrderedDict([('Path',[])])
        self.mainLayout.addWidget(self.TableImage)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.scroll)
        self.addLayout(self.layout)

    def SendImageTableWidgets(self,image):
        self.imageListPath['Path'].append(image)
        rowCount = len(self.imageListPath['Path']) // self.IMAGES_PER_ROW
        if len(self.imageListPath['Path']) % self.IMAGES_PER_ROW: rowCount += 1
        self.TableImage.setRowCount(rowCount)
        row = -1
        for i, picture in enumerate(self.imageListPath['Path']):
            col = i % self.IMAGES_PER_ROW
            if not col: row += 1
            self.addPicture(row, col, picture)

    def addPicture(self, row, col, picturePath):
        item = QtGui.QTableWidgetItem()
        p = QtGui.QPixmap(picturePath)
        if not p.isNull():
            if p.height() > p.width():
                p = p.scaledToWidth(self.THUMBNAIL_SIZE)
            else:
                p = p.scaledToHeight(self.THUMBNAIL_SIZE)
            p = p.copy(0, 0, self.THUMBNAIL_SIZE, self.THUMBNAIL_SIZE)
            item.setIcon(QtGui.QIcon(p))
            self.TableImage.setItem(row, col, item)
            self.TableImage.scrollToBottom()

class Mitmproxy(QtGui.QVBoxLayout):
    ''' settings  Transparent Proxy '''
    sendError = QtCore.pyqtSignal(str)
    def __init__(self, mainWindow):
        QtGui.QVBoxLayout.__init__(self)
        self.mainLayout = QtGui.QVBoxLayout()
        self.config = SettingsINI(C.MITMPROXY_INI)
        self.plugins = []
        self.main_method = mainWindow
        self.bt_SettingsDict = {}
        self.check_PluginDict = {}
        self.search_all_ProxyPlugins()
        #scroll area
        self.scrollwidget = QtGui.QWidget()
        self.scrollwidget.setLayout(self.mainLayout)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollwidget)

        # create for add dock logging
        self.tabcontrol = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.page_1 = QtGui.QVBoxLayout(self.tab1)
        self.page_2 = QtGui.QVBoxLayout(self.tab2)
        self.tableLogging = dockPickleProxy()

        self.tabcontrol.addTab(self.tab1, 'Plugins')
        self.tabcontrol.addTab(self.tab2, 'Logging')

        self.TabPlugins = QtGui.QTableWidget()
        self.TabPlugins.setColumnCount(3)
        self.TabPlugins.setRowCount(len(self.plugins))
        self.TabPlugins.resizeRowsToContents()
        self.TabPlugins.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.TabPlugins.horizontalHeader().setStretchLastSection(True)
        self.TabPlugins.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.TabPlugins.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.TabPlugins.verticalHeader().setVisible(False)
        self.TabPlugins.verticalHeader().setDefaultSectionSize(27)
        self.TabPlugins.setSortingEnabled(True)
        self.THeaders = OrderedDict([('Plugins', []), ('Settings', []), ('Description', [])])
        self.TabPlugins.setHorizontalHeaderLabels(list(dict(self.THeaders).keys()))
        self.TabPlugins.horizontalHeader().resizeSection(0, 158)
        self.TabPlugins.horizontalHeader().resizeSection(1, 80)

        # add on tab
        self.page_1.addWidget(self.TabPlugins)
        self.page_2.addWidget(self.tableLogging)

        # get all plugins and add into TabWidget
        Headers = []
        for plugin in self.plugins:
            if plugin.ConfigParser:
                self.bt_SettingsDict[plugin.Name] = QtGui.QPushButton('Settings')
                self.bt_SettingsDict[plugin.Name].clicked.connect(partial(self.setSettingsPlgins,plugin.Name))
            else:
                self.bt_SettingsDict[plugin.Name] = QtGui.QPushButton('None')
            self.check_PluginDict[plugin.Name] = QtGui.QCheckBox(plugin.Name)
            self.check_PluginDict[plugin.Name].setObjectName(plugin.Name)
            self.check_PluginDict[plugin.Name].clicked.connect(partial(self.setPluginOption,plugin.Name))
            self.THeaders['Plugins'].append(self.check_PluginDict[plugin.Name])
            self.THeaders['Settings'].append({'name': plugin.Name})
            self.THeaders['Description'].append(plugin.Description)
        for n, key in enumerate(self.THeaders.keys()):
            Headers.append(key)
            for m, item in enumerate(self.THeaders[key]):
                if type(item) == type(QtGui.QCheckBox()):
                    self.TabPlugins.setCellWidget(m,n,item)
                elif type(item) == type(dict()):
                    self.TabPlugins.setCellWidget(m,n,self.bt_SettingsDict[item['name']])
                else:
                    item = QtGui.QTableWidgetItem(item)
                    self.TabPlugins.setItem(m, n, item)
        self.TabPlugins.setHorizontalHeaderLabels(list(dict(self.THeaders).keys()))

        # check status all checkbox plugins
        for box in self.check_PluginDict.keys():
            self.check_PluginDict[box].setChecked(self.config.get_setting('plugins',box,format=bool))

        self.mainLayout.addWidget(self.tabcontrol)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.scroll)
        self.addLayout(self.layout)

    def setPluginOption(self, name,status):
        ''' get each plugins status'''
        # enable realtime disable and enable plugin
        if self.main_method.PopUpPlugins.check_mitmproxy.isChecked() and \
            self.main_method.FSettings.Settings.get_setting('accesspoint','statusAP',format=bool):
                self.main_method.Thread_MitmProxy.disablePlugin(name, status)
        self.config.set_setting('plugins',name,status)

    def setSettingsPlgins(self,plugin):
        ''' open settings options for each plugins'''
        key = 'set_{}'.format(plugin)
        self.widget = PickleProxySettings(key,self.config.get_all_childname(key))
        self.widget.show()

    def search_all_ProxyPlugins(self):
        ''' load all plugins function '''
        if load_plugins:
            plugin_classes = plugin.PluginTemplate.__subclasses__()
            for p in plugin_classes:
                self.plugins.append(p())

class PickleMonitor(QtGui.QVBoxLayout):
    ''' Monitor Access Point cleints connections'''
    def __init__(self, FsettingsUI=None, parent = None):
        super(PickleMonitor, self).__init__(parent)
        self.FSettings = FsettingsUI
        self.Home = QtGui.QVBoxLayout()
        self.widget = QtGui.QWidget()
        self.layout = QtGui.QVBoxLayout(self.widget)

        self.GroupMonitor = QtGui.QGroupBox()
        self.MonitorTreeView = QtGui.QTreeView()
        self.MonitorTreeView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.model = QtGui.QStandardItemModel()
        self.setModel()
        self.MonitorTreeView.setUniformRowHeights(True)
        self.MonitorTreeView.setColumnWidth(0, 130)

        self.GroupMonitor.setTitle('Station Monitor AP:')
        self.MonitorLayout = QtGui.QVBoxLayout()
        self.MonitorLayout.addWidget(self.MonitorTreeView)
        self.GroupMonitor.setLayout(self.MonitorLayout)
        self.layout.addWidget(self.GroupMonitor)
        self.Home.addWidget(self.widget)
        self.addLayout(self.Home)

    def setModel(self):
        self.model.setHorizontalHeaderLabels(['Devices','Informations'])
        self.MonitorTreeView.setModel(self.model)

    def expandAll(self):
        return self.MonitorTreeView.expandAll()

    def clearAll(self):
        self.model.clear()
        return self.setModel()

    def addRequests(self,macddress,user,status):
        if status:
            ParentMaster = QtGui.QStandardItem('Connected:: {} at {}'.format(macddress,
            datetime.now().strftime("%H:%M")))
            ParentMaster.setIcon(QtGui.QIcon('icons/connected.png'))
            ParentMaster.setSizeHint(QtCore.QSize(30,30))
            info1 = QtGui.QStandardItem('{}'.format(user['device']))
            info2 = QtGui.QStandardItem('{}'.format(user['IP']))
            info3 = QtGui.QStandardItem('{}'.format(datetime.now().strftime("%Y-%m-%d %H:%M")))
            ParentMaster.appendRow([QtGui.QStandardItem('Device::'),info1])
            ParentMaster.appendRow([QtGui.QStandardItem('IPAddr::'),info2])
            ParentMaster.appendRow([QtGui.QStandardItem('Current date::'),info3])
            self.model.appendRow(ParentMaster)
            self.MonitorTreeView.expandAll()
            return self.MonitorTreeView.setFirstColumnSpanned(ParentMaster.row(),
            self.MonitorTreeView.rootIndex(), True)

        ParentMaster = QtGui.QStandardItem('Disconnected:: {} at {}'.format(macddress,
        datetime.now().strftime("%H:%M")))
        ParentMaster.setIcon(QtGui.QIcon('icons/disconnected.png'))
        ParentMaster.setSizeHint(QtCore.QSize(30,30))
        info1 = QtGui.QStandardItem('{}'.format(user['device']))
        info2 = QtGui.QStandardItem('{}'.format(user['IP']))
        info3 = QtGui.QStandardItem('{}'.format(datetime.now().strftime("%Y-%m-%d %H:%M")))
        ParentMaster.appendRow([QtGui.QStandardItem('Device::'),info1])
        ParentMaster.appendRow([QtGui.QStandardItem('IPAddr::'),info2])
        ParentMaster.appendRow([QtGui.QStandardItem('Current date::'),info3])
        self.model.appendRow(ParentMaster)
        self.MonitorTreeView.setFirstColumnSpanned(ParentMaster.row(),
        self.MonitorTreeView.rootIndex(), True)
        self.MonitorTreeView.expandAll()


class PickleSettings(QtGui.QVBoxLayout):
    ''' settings DHCP options'''
    sendMensage = QtCore.pyqtSignal(str)
    checkDockArea = QtCore.pyqtSignal(dict)
    def __init__(self, parent=None,widgets=None):
        super(PickleSettings, self).__init__(parent)
        self.SettingsAp = widgets['SettingsAP']
        self.Tab_Dock = widgets['Tab_dock']
        self.dockInfo = widgets['DockInfo']
        self.FSettings = widgets['Settings']
        self.NetworkGroup = widgets['Network']
        self.mainLayout = QtGui.QFormLayout()
        self.SettingsDHCP = {}

        #scroll area
        self.scrollwidget = QtGui.QWidget()
        self.scrollwidget.setLayout(self.mainLayout)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollwidget)

        self.GroupDHCP = QtGui.QGroupBox()
        self.GroupArea = QtGui.QGroupBox()
        self.layoutDHCP = QtGui.QFormLayout()
        self.layoutArea = QtGui.QFormLayout()
        self.layoutbuttons = QtGui.QHBoxLayout()
        self.btnDefault = QtGui.QPushButton('Default')
        self.btnSave = QtGui.QPushButton('Apply & Save')
        self.btnSave.setIcon(QtGui.QIcon('icons/export.png'))
        self.btnDefault.setIcon(QtGui.QIcon('icons/settings.png'))
        self.dhcpClassIP = QtGui.QComboBox()
        # dhcp class
        self.classtypes = ['Class-A-Address', 'Class-B-Address', 'Class-C-Address']
        for types in self.classtypes:
            if 'Class-{}-Address'.format(self.FSettings.Settings.get_setting('dhcp', 'classtype')) in types:
                self.classtypes.remove(types),self.classtypes.insert(0, types)
        self.dhcpClassIP.addItems(self.classtypes)

        self.leaseTime_def = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'leasetimeDef'))
        self.leaseTime_Max = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'leasetimeMax'))
        self.netmask = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'netmask'))
        self.range_dhcp = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'range'))
        self.route = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'router'))
        self.subnet = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'subnet'))
        self.broadcast = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'broadcast'))
        self.option = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'option'))
        self.dns = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'dns'))
        self.dhcpClassIP.currentIndexChanged.connect(self.dhcpClassIPClicked)
        self.GroupDHCP.setTitle('DHCP-Settings')
        self.GroupDHCP.setLayout(self.layoutDHCP)
        self.layoutDHCP.addRow('Class Ranges', self.dhcpClassIP)
        self.layoutDHCP.addRow('default-lease-time', self.leaseTime_def)
        self.layoutDHCP.addRow('max-lease-time', self.leaseTime_Max)
        self.layoutDHCP.addRow('subnet', self.subnet)
        self.layoutDHCP.addRow('router', self.route)
        self.layoutDHCP.addRow('netmask', self.netmask)
        self.layoutDHCP.addRow('broadcast-address', self.broadcast)
        self.layoutDHCP.addRow('DNS', self.dns)
        self.layoutDHCP.addRow('option', self.option)
        self.layoutDHCP.addRow('range-dhcp', self.range_dhcp)
        self.GroupDHCP.setFixedWidth(350)

        # layout add
        self.layoutbuttons.addWidget(self.btnSave)
        self.layoutbuttons.addWidget(self.btnDefault)
        self.layoutDHCP.addRow(self.layoutbuttons)

        # Area Group
        self.gridArea = QtGui.QGridLayout()
        self.CB_ActiveMode = QtGui.QCheckBox('::Advanced Mode:: Monitor MITM Attack')
        self.CB_ActiveMode.setHidden(True)
        self.CB_Cread = QtGui.QCheckBox('HTTP-Authentication')
        self.CB_monitorURL = QtGui.QCheckBox('HTTP-Requests')
        self.CB_dhcpd = QtGui.QCheckBox('DHCPD')
        self.CB_mitmproxy = QtGui.QCheckBox('MITM Proxy')
        self.CB_meatglueproxy = QtGui.QCheckBox('MeatGlueDNSProxy')
        self.CB_responder = QtGui.QCheckBox('Responder')
        self.CB_picklePro = QtGui.QCheckBox('Pickle-Proxy')
        self.CB_ActiveMode.setChecked(self.FSettings.Settings.get_setting('dockarea', 'advanced', format=bool))
        self.CB_Cread.setChecked(self.FSettings.Settings.get_setting('dockarea', 'dock_credencials', format=bool))
        self.CB_monitorURL.setChecked(self.FSettings.Settings.get_setting('dockarea', 'dock_urlmonitor', format=bool))
        self.CB_dhcpd.setChecked(self.FSettings.Settings.get_setting('dockarea', 'dock_dhcpd', format=bool))
        self.CB_mitmproxy.setChecked(self.FSettings.Settings.get_setting('dockarea', 'dock_mitmproxy', format=bool))
        self.CB_meatglueproxy.setChecked(self.FSettings.Settings.get_setting('dockarea', 'dock_meatglueproxy', format=bool))
        self.CB_responder.setChecked(self.FSettings.Settings.get_setting('dockarea', 'dock_responder', format=bool))
        self.CB_picklePro.setChecked(self.FSettings.Settings.get_setting('dockarea', 'dock_PickleProxy', format=bool))

        #connect
        self.doCheckAdvanced()
        self.CB_ActiveMode.clicked.connect(self.doCheckAdvanced)
        self.CB_monitorURL.clicked.connect(self.doCheckAdvanced)
        self.CB_Cread.clicked.connect(self.doCheckAdvanced)
        self.CB_dhcpd.clicked.connect(self.doCheckAdvanced)
        self.CB_mitmproxy.clicked.connect(self.doCheckAdvanced)
        self.CB_meatglueproxy.clicked.connect(self.doCheckAdvanced)
        self.CB_responder.clicked.connect(self.doCheckAdvanced)
        self.CB_picklePro.clicked.connect(self.doCheckAdvanced)
        # group
        self.layoutArea.addRow(self.CB_ActiveMode)
        self.gridArea.addWidget(self.CB_monitorURL, 0, 0)
        self.gridArea.addWidget(self.CB_Cread, 0, 1)
        self.gridArea.addWidget(self.CB_responder, 0, 2)
        self.gridArea.addWidget(self.CB_dhcpd, 1, 0)
        self.gridArea.addWidget(self.CB_mitmproxy, 1, 1)
        self.gridArea.addWidget(self.CB_meatglueproxy, 1, 2)
        self.layoutArea.addRow(self.gridArea)
        self.GroupArea.setTitle('Activity Monitor settings')
        self.GroupArea.setLayout(self.layoutArea)

        # connects
        self.btnDefault.clicked.connect(self.setdefaultSettings)
        self.btnSave.clicked.connect(self.savesettingsDHCP)
        self.mainLayout.addRow(self.SettingsAp)
        self.mainLayout.addRow(self.NetworkGroup)
        self.mainLayout.addRow(self.GroupArea)
        self.mainLayout.addRow(self.GroupDHCP)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.scroll)
        self.addLayout(self.layout)


    def dhcpClassIPClicked(self,classIP):
        self.selected = str(self.dhcpClassIP.currentText())
        self.leaseTime_def.setText(self.FSettings.Settings.get_setting(self.selected, 'leasetimeDef'))
        self.leaseTime_Max.setText(self.FSettings.Settings.get_setting(self.selected, 'leasetimeMax'))
        self.netmask.setText(self.FSettings.Settings.get_setting(self.selected, 'netmask'))
        self.range_dhcp.setText(self.FSettings.Settings.get_setting(self.selected, 'range'))
        self.route.setText(self.FSettings.Settings.get_setting(self.selected, 'router'))
        self.subnet.setText(self.FSettings.Settings.get_setting(self.selected, 'subnet'))
        self.broadcast.setText(self.FSettings.Settings.get_setting(self.selected, 'broadcast'))
        self.dns.setText(self.FSettings.Settings.get_setting(self.selected, 'router'))
        self.savesettingsDHCP()

    def AreaWidgetLoader(self,DockInfo):
        if hasattr(self,'dockList'):
            for dock in self.dockList: dock.close()
        self.AllDockArea = {}
        if self.FSettings.Settings.get_setting('dockarea', 'advanced',format=bool):
            self.dockList = []
            for key in DockInfo.keys():
                if DockInfo[key]['active']:
                    self.dock = QtGui.QDockWidget(key)
                    if key == 'HTTP-Authentication':
                        self.AllDockArea[key] = dockCredsMonitor(None,DockInfo[key])
                    elif key == 'HTTP-Requests':
                        self.AllDockArea[key] = dockUrlMonitor(None,DockInfo[key])
                    elif key == 'PickleProxy':
                        self.AllDockArea[key] = dockPickleProxy(None, DockInfo[key])
                    else:
                        self.AllDockArea[key] = dockAreaAPI(None,DockInfo[key])
                    self.dock.setWidget(self.AllDockArea[key])
                    self.dock.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
                    self.dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
                    self.dock.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
                    self.Tab_Dock.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock)
                    self.dockList.insert(0, self.dock)
            if len(self.dockList) > 1:
                for index in range(1 , len(self.dockList) - 1):
                    if self.dockList[index].objectName() != 'HTTP-Requests':
                        self.Tab_Dock.tabifyDockWidget(self.dockList[index],
                            self.dockList[index + 1])
            try:
                self.dockList[0].raise_()
            except IndexError:
                pass
            self.checkDockArea.emit(self.AllDockArea)


    def doCheckAdvanced(self):
        if self.CB_ActiveMode.isChecked():
            self.CB_monitorURL.setEnabled(True)
            self.CB_Cread.setEnabled(True)
            self.CB_dhcpd.setEnabled(True)
            self.CB_mitmproxy.setEnabled(True)
            self.CB_meatglueproxy.setEnabled(True)
            self.CB_responder.setEnabled(True)
            self.CB_picklePro.setEnabled(True)
        else:
            self.CB_monitorURL.setEnabled(False)
            self.CB_Cread.setEnabled(False)
            self.CB_dhcpd.setEnabled(False)
            self.CB_mitmproxy.setEnabled(False)
            self.CB_meatglueproxy.setEnabled(False)
            self.CB_responder.setEnabled(False)
            self.CB_picklePro.setEnabled(False)
        self.FSettings.Settings.set_setting('dockarea', 'dock_credencials', self.CB_Cread.isChecked())
        self.FSettings.Settings.set_setting('dockarea', 'dock_urlmonitor', self.CB_monitorURL.isChecked())
        self.FSettings.Settings.set_setting('dockarea', 'dock_dhcpd', self.CB_dhcpd.isChecked())
        self.FSettings.Settings.set_setting('dockarea', 'dock_mitmproxy', self.CB_mitmproxy.isChecked())
        self.FSettings.Settings.set_setting('dockarea', 'dock_meatglueproxy', self.CB_meatglueproxy.isChecked())
        self.FSettings.Settings.set_setting('dockarea', 'dock_responder', self.CB_responder.isChecked())
        self.FSettings.Settings.set_setting('dockarea', 'dock_PickleProxy', self.CB_picklePro.isChecked())
        self.FSettings.Settings.set_setting('dockarea', 'advanced', self.CB_ActiveMode.isChecked())
        self.dockInfo['HTTP-Requests']['active'] = self.CB_monitorURL.isChecked()
        self.dockInfo['HTTP-Authentication']['active'] = self.CB_Cread.isChecked()
        self.dockInfo['DHCPD']['active'] = self.CB_dhcpd.isChecked()
        self.dockInfo['MITMProxy']['active'] = self.CB_mitmproxy.isChecked()
        self.dockInfo['MeatGlueDNSProxy']['active'] = self.CB_meatglueproxy.isChecked()
        self.dockInfo['Responder']['active'] = self.CB_responder.isChecked()
        if self.CB_ActiveMode.isChecked():
            self.AreaWidgetLoader(self.dockInfo)
            self.checkDockArea.emit(self.AllDockArea)
            if hasattr(self.Tab_Dock, 'form_widget'):
                if hasattr(self.Tab_Dock.form_widget,'Apthreads'):
                    if self.Tab_Dock.form_widget.Apthreads['RougeAP'] != []:
                        for dock in self.Tab_Dock.form_widget.dockAreaList.keys():
                            self.Tab_Dock.form_widget.dockAreaList[dock].RunThread()
        else:
            if hasattr(self,'dockList'):
                for dock in self.dockList:
                    dock.close()


    def setdefaultSettings(self):
        self.dhcpClassIP.setCurrentIndex(self.classtypes.index('Class-A-Address'))
        self.leaseTime_def.setText(self.FSettings.Settings.get_setting('dhcpdefault', 'leasetimeDef'))
        self.leaseTime_Max.setText(self.FSettings.Settings.get_setting('dhcpdefault', 'leasetimeMax'))
        self.netmask.setText(self.FSettings.Settings.get_setting('dhcpdefault', 'netmask'))
        self.range_dhcp.setText(self.FSettings.Settings.get_setting('dhcpdefault', 'range'))
        self.route.setText(self.FSettings.Settings.get_setting('dhcpdefault', 'router'))
        self.subnet.setText(self.FSettings.Settings.get_setting('dhcpdefault', 'subnet'))
        self.broadcast.setText(self.FSettings.Settings.get_setting('dhcpdefault', 'broadcast'))
        self.dns.setText(self.FSettings.Settings.get_setting('dhcpdefault', 'router'))
        self.option.setText("")

    def writeDhcpConf(self):
        dhcpFile = open(str(C.DHCPCONF_PATH), 'w')
        leaseTimeDefault = self.FSettings.Settings.get_setting('dhcp', 'leasetimeDef')
        leaseTimeMax = self.FSettings.Settings.get_setting('dhcp', 'leasetimeMax')
        networkNetmask = self.FSettings.Settings.get_setting('dhcp', 'netmask')
        fullRange = self.FSettings.Settings.get_setting('dhcp', 'range')
        networkRouterAddr = self.FSettings.Settings.get_setting('dhcp', 'router')
        networkAddr = self.FSettings.Settings.get_setting('dhcp', 'subnet')
        networkBroadcastAddr = self.FSettings.Settings.get_setting('dhcp', 'broadcast')
        lowerRange = str(fullRange).split('/')[0]
        upperRange = str(fullRange).split('/')[1]
        dnsAddr = self.FSettings.Settings.get_setting('dhcp', 'dns')
        dhcpOption = self.FSettings.Settings.get_setting('dhcp', 'option')
        confSkeleton = """
default-lease-time %s;
max-lease-time %s;

ddns-update-style none;

authoritative;

subnet %s netmask %s {
  range %s %s;
  option routers %s;
  option domain-name-servers %s;
  %s
}
""" % (leaseTimeDefault, leaseTimeMax, networkAddr, networkNetmask, lowerRange, upperRange, networkRouterAddr, dnsAddr, dhcpOption)
        print('Writting dhcpd.conf with these contents:')
        print(confSkeleton)
        dhcpFile.write(confSkeleton)
        dhcpFile.close()

    def savesettingsDHCP(self):
        self.all_gateway_check = []
        for types in self.classtypes:
            self.all_gateway_check.append(self.FSettings.Settings.get_by_index_key(5, types))
        self.FSettings.Settings.set_setting('dhcp','classtype', str(self.dhcpClassIP.currentText()).split('-')[1])
        self.FSettings.Settings.set_setting('dhcp','leasetimeDef', str(self.leaseTime_def.text()))
        self.FSettings.Settings.set_setting('dhcp','leasetimeMax', str(self.leaseTime_Max.text()))
        self.FSettings.Settings.set_setting('dhcp','netmask', str(self.netmask.text()))
        self.FSettings.Settings.set_setting('dhcp','range', str(self.range_dhcp.text()))
        self.FSettings.Settings.set_setting('dhcp','router', str(self.route.text()))
        self.FSettings.Settings.set_setting('dhcp','subnet', str(self.subnet.text()))
        self.FSettings.Settings.set_setting('dhcp','broadcast', str(self.broadcast.text()))
        self.FSettings.Settings.set_setting('dhcp','dns', str(self.dns.text()))
        self.FSettings.Settings.set_setting('dhcp','option', str(self.option.text()))
        if not str(self.route.text()) in self.all_gateway_check:
            self.FSettings.Settings.set_setting('dhcp', 'classtype', 'Custom')
        self.btnSave.setEnabled(False)
        self.writeDhcpConf()
        #self.sendMensage.emit('settings DHCP saved with success...')
        self.btnSave.setEnabled(True)

    def getPickleSettings(self):
        self.SettingsDHCP['leasetimeDef'] = str(self.leaseTime_def.text())
        self.SettingsDHCP['leasetimeMax'] = str(self.leaseTime_Max.text())
        self.SettingsDHCP['subnet'] = str(self.subnet.text())
        self.SettingsDHCP['router'] = str(self.route.text())
        self.SettingsDHCP['netmask'] = str(self.netmask.text())
        self.SettingsDHCP['broadcast'] = str(self.broadcast.text())
        self.SettingsDHCP['range'] = str(self.range_dhcp.text())
        return self.SettingsDHCP
