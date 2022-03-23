#
#      Copyright (C) 2014 Tommy Winther, msj33, TermeHansen
#
#  https://github.com/xbmc-danish-addons/plugin.video.drnu
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import pickle
import os
import sys
import re
import datetime

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

from resources.lib import tvapi
from resources.lib import tvgui

if sys.version_info.major == 2:
    # python 2
    import urlparse
    from xbmc import translatePath
    compat_str = unicode
else:
    import urllib.parse as urlparse
    from xbmcvfs import translatePath
    compat_str = str


addon = xbmcaddon.Addon()
get_setting = addon.getSetting
addon_path = addon.getAddonInfo('path')
addon_name = addon.getAddonInfo('name')


def tr(id):
    if isinstance(id, list):
        return '\n'.join([addon.getLocalizedString(item) for item in id])
    return addon.getLocalizedString(id)


def bool_setting(name):
    return  get_setting(name) == 'true'


def make_notice(object):
    xbmc.log(str(object), xbmc.LOGDEBUG )


class DrDkTvAddon(object):
    def __init__(self, plugin_url, plugin_handle):
        self._plugin_url = plugin_url
        self._plugin_handle = plugin_handle

        self.cache_path = translatePath(addon.getAddonInfo('profile'))
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

        self.favorites_path = os.path.join(self.cache_path, 'favorites.pickle')
        self.recent_path = os.path.join(self.cache_path, 'recent.pickle')
        self.fanart_image = os.path.join(addon_path, 'resources', 'fanart.jpg')

        self.api = tvapi.Api(self.cache_path)
        self.favorites = list()
        self.recentlyWatched = list()

        self.menuItems = list()
        runScript = "RunAddon(plugin.video.drnu,?show=areaselector&random={:d})".format(self._plugin_handle)
        self.menuItems.append((tr(30511), runScript))

        # Area Selector
        self.area_item = xbmcgui.ListItem(tr(30101), offscreen=True)
        self.area_item.setArt({'fanart': self.fanart_image, 'icon': os.path.join(addon_path, 'resources', 'icons', 'all.png')})



    def showAZ(self):
        # All Program Series
        iconImage = os.path.join(addon_path, 'resources', 'icons', 'all.png')
        items = list()
        for programIndex in self.api.getProgramIndexes():
            item = xbmcgui.ListItem(programIndex['Title'], offscreen=True)
            item.setArt({'fanart': self.fanart_image, 'icon': iconImage})
            item.addContextMenuItems(self.menuItems, False)

            url = self._plugin_url + '?listProgramSeriesByLetter=' + programIndex['_Param']
            items.append((url, item, True))
        xbmcplugin.addDirectoryItems(self._plugin_handle, items)
        xbmcplugin.endOfDirectory(self._plugin_handle)


    def listSeries(self, items, addToFavorites=True, add_area_selector=False):
        if not items:
            xbmcplugin.endOfDirectory(self._plugin_handle, succeeded=False)
            if not addToFavorites:
                xbmcgui.Dialog().ok(addon_name, tr([30013, 30018, 30019]))
            else:
                xbmcgui.Dialog().ok(addon_name, tr(30013))
        else:
            directoryItems = list()
            if add_area_selector:
                directoryItems.append((self._plugin_url + '?show=areaselector', self.area_item, True))
            for item in items:
                menuItems = list(self.menuItems)

                title = item['SeriesTitle'].replace('&', '%26').replace(',', '%2C')
                if item['SeriesTitle'] in self.favorites:
                    runScript = compat_str("RunPlugin(plugin://plugin.video.drnu/?delfavorite={})").format(title)
                    menuItems.append((tr(30201), runScript))
                else:
                    runScript = compat_str("RunPlugin(plugin://plugin.video.drnu/?addfavorite={})").format(title)
                    menuItems.append((tr(30200), runScript))


                listItem = xbmcgui.ListItem(item['SeriesTitle'], offscreen=True)
                fanart_h = int(get_setting('fanart.size'))
                fanart_w = int(fanart_h*16/9)
                listItem.setArt({'thumb': self.api.redirectImageUrl(item['PrimaryImageUri'], 640, 360),
                          	 'icon': self.api.redirectImageUrl(item['PrimaryImageUri'], 75, 42),
                          	 'fanart': self.api.redirectImageUrl(item['PrimaryImageUri'], fanart_w, fanart_h)})
                listItem.addContextMenuItems(menuItems, False)

                url = self._plugin_url + '?listVideos=' + item['SeriesSlug']
                directoryItems.append((url, listItem, True))

            xbmcplugin.addDirectoryItems(self._plugin_handle, directoryItems)
            xbmcplugin.endOfDirectory(self._plugin_handle)

    def listEpisodes(self, items, addSortMethods=True):
        directoryItems = list()
        for item in items:
            if 'PrimaryAsset' not in item or 'Uri' not in item['PrimaryAsset'] or not item['PrimaryAsset']['Uri']:
                continue

            infoLabels = {
                'title': item['Title']
            }
            if 'Description' in item:
                infoLabels['plot'] = item['Description']
            if 'PrimaryBroadcastStartTime' in item and item['PrimaryBroadcastStartTime'] is not None:
                broadcastTime = self.parseDate(item['PrimaryBroadcastStartTime'])
                if broadcastTime:
                    infoLabels['date'] = broadcastTime.strftime('%d.%m.%Y')
                    infoLabels['aired'] = broadcastTime.strftime('%Y-%m-%d')
                    infoLabels['year'] = int(broadcastTime.strftime('%Y'))

            listItem = xbmcgui.ListItem(item['Title'], offscreen=True)
            fanart_h = int(get_setting('fanart.size'))
            fanart_w = int(fanart_h*16/9)
            listItem.setArt({'thumb': self.api.redirectImageUrl(item['PrimaryImageUri'], 640, 360),
                             'icon': self.api.redirectImageUrl(item['PrimaryImageUri'], 75, 42),
                             'fanart': self.api.redirectImageUrl(item['PrimaryImageUri'], fanart_w, fanart_h)})
            listItem.setInfo('video', infoLabels)
            url = self._plugin_url + '?playVideo=' + item['Slug']
            listItem.setProperty('IsPlayable', 'true')
            listItem.addContextMenuItems(self.menuItems, False)
            directoryItems.append((url, listItem))

        xbmcplugin.addDirectoryItems(self._plugin_handle, directoryItems)
        if addSortMethods:
            xbmcplugin.addSortMethod(self._plugin_handle, xbmcplugin.SORT_METHOD_DATE)
            xbmcplugin.addSortMethod(self._plugin_handle, xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(self._plugin_handle)

    def playVideo(self, slug):
        api_item = self.api.getEpisode(slug)
        kids_channel = False
        if 'PrimaryBroadcast' in api_item:
            kids_channel = api_item['PrimaryBroadcast']['ChannelSlug'] in ['dr-ramasjang', 'dr-ultra']
        if not 'PrimaryAsset' in api_item:
            self.displayError(tr(30904))
            return
        video = self.api.getVideoUrl(api_item['PrimaryAsset']['Uri'])
        item = xbmcgui.ListItem(path=video['Uri'], offscreen=True)
        item.setArt({'thumb': api_item['PrimaryImageUri']})

        if not all([bool_setting('disable.kids.subtitles') and kids_channel]):
            if video['SubtitlesUri']:
                if bool_setting('enable.subtitles'):
                    item.setSubtitles(video['SubtitlesUri'][::-1])
                else:
                    item.setSubtitles(video['SubtitlesUri'])
        xbmcplugin.setResolvedUrl(self._plugin_handle, video['Uri'] is not None, item)


    def parseDate(self, dateString):
        if dateString is not None:
            try:
                m = re.search('(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)', dateString)
                year = int(m.group(1))
                month = int(m.group(2))
                day = int(m.group(3))
                hours = int(m.group(4))
                minutes = int(m.group(5))
                seconds = int(m.group(6))
                return datetime.datetime(year, month, day, hours, minutes, seconds)
            except ValueError:
                return None
        else:
            return None


    def displayError(self, message='n/a'):
        xbmcgui.Dialog().ok(message, '\n'.join([tr(30900), tr(30901), message]))


    def route(self, query):
        try:
            PARAMS = dict(urlparse.parse_qsl(query[1:]))
            if 'show' in PARAMS:
                self.showAZ()
            elif 'listThemeSeries' in PARAMS:
                self.listSeries(self.api.getEpisodes(PARAMS['listThemeSeries']))

            elif 'listProgramSeriesByLetter' in PARAMS:
                self.listSeries(self.api.getSeries(PARAMS['listProgramSeriesByLetter']))

            elif 'listVideos' in PARAMS:
                self.listEpisodes(self.api.getEpisodes(PARAMS['listVideos']))

            elif 'playVideo' in PARAMS:
                self.playVideo(PARAMS['playVideo'])

            else:
                self.showAZ()

        except tvapi.ApiException as ex:
            self.displayError(str(ex))

        except Exception:
            pass
