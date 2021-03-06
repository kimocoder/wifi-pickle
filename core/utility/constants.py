import os

"""
Description:
    This program is a module for wifi-pickle.py file which includes functionality
    declare constants .

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

dir_of_executable = os.path.dirname(__file__)
dir_path          = os.getcwd()
# window constants
GEOMETRYH = 1024
GEOMETRYW = 768

MENU_STYLE = 'QListWidget::item {border-style: solid; border-width:3px; ' \
             'border-color:#3A3939;}QListWidget::item:selected {border-style:' \
             ' solid; color:#FFFFFF;  background-color: #3A3939; border-width:2px; border-radius: 2px; border: 3px solid #5d198e;}QListWidget ' \
             '{background-color: #302F2F; border-radius 2px; border-width:3px;border-color:#201F1F;} QListWidget:item:hover'\
'{color: #6d2f99;border-radius: 2px; }'
GTKTHEME = 'Plastique'

NOTIFYSTYLE = "; ".join((
    "color: #302F2F",
    'background-color: #996633',
    "border-color: #996633",
    "border: 2px solid #996633",
    "padding: 5px"))


#settings DHCP
DHCPLEASES_PATH = '/var/lib/dhcp/dhcpd.leases'
DHCPCONF_PATH   = 'core/config/dhcpd/dhcpd.conf'

# settings HOSTAPD
HOSTAPDCONF_PATH    = 'core/config/hostapd/hostapd.conf'
HOSTAPDCONF_PATH2   = 'core/config/hostapd/hostapd+.conf'
ALGORITMS = ('TKIP','CCMP','TKIP + CCMP')

#system configs
NETWORKMANAGER = '/etc/NetworkManager/NetworkManager.conf'
IPFORWARD      = '/proc/sys/net/ipv4/ip_forward'

#logging
LOG_MITMPROXY = 'logs/AccessPoint/pickle-proxy.log'
LOG_URLCAPTURE   = 'logs/AccessPoint/urls.log'
LOG_CREDSCAPTURE = 'logs/AccessPoint/credentials.log'
LOG_TCPPROXY     = 'logs/AccessPoint/tcp-proxy.log'
LOG_RESPONDER    = 'logs/AccessPoint/responder.log'
LOG_SSLSTRIP     = 'logs/AccessPoint/injectionPage.log'
LOG_DNSSPOOF     = 'logs/AccessPoint/dnsspoof.log'
LOG_PHISHING     = 'logs/Phishing/requests.log'
LOG_DHCP         = 'logs/AccessPoint/dhcp.log'
LOG_HOSTAPD      = 'logs/AccessPoint/hostapd.log'


#APP SETTINGS
CONFIG_INI      = 'core/config/app/config.ini'
TCPPROXY_INI    = 'core/config/app/tcpproxy.ini'
MITMPROXY_INI   = 'core/config/app/proxy.ini'
TEMPLATES       = 'templates/fakeupdate/Windows_Update/Settins_WinUpdate.html'
TEMPLATE_PH     = 'templates/phishing/custom/index.html'
TEMPLATE_CLONE  = 'templates/phishing/web_server/index.html'
EXTRACT_TEMP    = 'cd templates/ && tar -xf fakeupdate.tar.gz'
LCOMMITS        = 'https://raw.githubusercontent.com/P0cL4bs/WiFi-Pickle/master/Core/config/commits/Lcommits.cfg'
SOURCE_URL      = 'https://github.com/P0cL4bs/WiFi-Pickle.git'

#settings template
TEMP_CUSTOM = dir_path+'/templates/phishing/custom'
TEMP_Win    = dir_path+'/templates/fakeupdate/Windows_Update'
TEMP_Java   = dir_path+'/templates/fakeupdate/Java_Update'

#plugins path
RESPONDER_EXEC  = 'plugins/external/Responder/Responder.py'
DNS2PROXY_EXEC  = 'plugins/external/dns2proxy/dns2proxy.py'
BDFPROXY_EXEC   = 'plugins/external/BDFProxy-ng/bdf_proxy.py'

#colors
YELLOW = '\033[33m'
RED = '\033[91m'
ENDC = '\033[0m'
