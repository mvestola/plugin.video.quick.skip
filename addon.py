import xbmcaddon
import xbmcgui
import xbmc
from threading import Timer

# To launch this script, add the file "kodi-quick-skip-keymap.xml" to your kodi user defined keymaps: ~/.kodi/userdata/keymaps/

addon = xbmcaddon.Addon()

# See key codes from https://github.com/xbmc/xbmc/blob/master/xbmc/input/Key.h
ACTION_MOVE_LEFT =  1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_UP = 3
ACTION_PAGE_UP =  5
ACTION_SELECT_ITEM = 7
ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK = 92
ACTION_CHANNEL_UP = 184

xbfont_left = 0x00000000
xbfont_right = 0x00000001
xbfont_center_x = 0x00000002
xbfont_center_y = 0x00000004
xbfont_truncated = 0x00000008

SKIP_LEFT = "left"
SKIP_RIGHT = "right"

AUTO_CLOSE_TIMEOUT_SECONDS = int(addon.getSetting("auto_close_timeout"))
FIRST_SKIP_SECONDS = int(addon.getSetting("first_skip_seconds"))
SECOND_SKIP_SECONDS = int(addon.getSetting("second_skip_seconds"))
THIRD_SKIP_SECONDS = int(addon.getSetting("third_skip_seconds"))

i18n_jump = addon.getLocalizedString(32201)
i18n_place = addon.getLocalizedString(32202)
i18n_sec = addon.getLocalizedString(32203)

timeout = None

class QuickSkipDialog(xbmcgui.WindowDialog):

    def __init__(self):
        self.skipSeconds = float(FIRST_SKIP_SECONDS)
        self.cumulativeSkipSeconds = 0.0
        self.startTime = None
        self.previousDirection = None
        self.directionChanged = False

        self.addControl(xbmcgui.ControlImage(10, 10, 200, 90, addon.getAddonInfo('path')+'/resources/background.png'))

        self.controlLabel1 = xbmcgui.ControlLabel(x=20, y=20, width=180, height=30, label="", alignment=xbfont_center_y|xbfont_center_x)
        self.addControl(self.controlLabel1)
        self.controlLabel1.setLabel(i18n_jump + ": " + str(FIRST_SKIP_SECONDS) + " " + i18n_sec)

        self.controlLabel2 = xbmcgui.ControlLabel(x=20, y=60, width=180, height=30, label="", alignment=xbfont_center_y|xbfont_center_x)
        self.addControl(self.controlLabel2)
        self.controlLabel2.setLabel(i18n_place + ": +00:00:00")

    def restartTimeoutTimer(self):
        global timeout
        timeout.cancel()
        timeout = Timer(AUTO_CLOSE_TIMEOUT_SECONDS, self.close)
        timeout.start()

    def closeDialogByUserInput(self):
        global timeout
        timeout.cancel()
        del timeout
        self.close()

    def onAction(self, action):
        action_id = action.getId()
        if action_id == ACTION_SELECT_ITEM or action_id == ACTION_MOVE_UP or action_id == ACTION_PAGE_UP or action_id == ACTION_CHANNEL_UP:
            if not self.directionChanged:
                if int(self.skipSeconds) == FIRST_SKIP_SECONDS:
                    self.restartTimeoutTimer()
                    self.skipSeconds = float(SECOND_SKIP_SECONDS)
                    self.controlLabel1.setLabel(i18n_jump + ": " + str(SECOND_SKIP_SECONDS) + " " + i18n_sec)
                elif int(self.skipSeconds) == SECOND_SKIP_SECONDS:
                    self.restartTimeoutTimer()
                    self.skipSeconds = float(THIRD_SKIP_SECONDS)
                    self.controlLabel1.setLabel(i18n_jump + ": " + str(THIRD_SKIP_SECONDS) + " " + i18n_sec)
                else:
                    self.closeDialogByUserInput()
            else:
                self.closeDialogByUserInput()
        elif action_id == ACTION_MOVE_LEFT:
            self.handleSkip(SKIP_LEFT)
        elif action_id == ACTION_MOVE_RIGHT:
            self.handleSkip(SKIP_RIGHT)
        else:
            self.closeDialogByUserInput()


    def handleSkip(self, direction):
        self.restartTimeoutTimer()

        if self.previousDirection is not None and self.previousDirection != direction:
            self.directionChanged = True

        if not self.directionChanged and self.startTime is None:
            self.startTime = xbmc.Player().getTime()

        if self.directionChanged:
            self.skipSeconds = self.skipSeconds / 2

        if abs(self.skipSeconds) < 2.0:
            self.skipSeconds = 2.0

        if direction == SKIP_LEFT:
            self.skipSeconds = -abs(self.skipSeconds)
        else:
            self.skipSeconds = abs(self.skipSeconds)

        self.cumulativeSkipSeconds = self.cumulativeSkipSeconds + self.skipSeconds
        self.previousDirection = direction

        m, s = divmod(abs(self.cumulativeSkipSeconds), 60)
        h, m = divmod(m, 60)
        formatted_place = "%02d:%02d:%02d" % (h, m, s)

        if self.cumulativeSkipSeconds < 0.0:
            formatted_place = "-" + formatted_place
        else:
            formatted_place = "+" + formatted_place

        self.controlLabel1.setLabel(i18n_jump + ": " + str(int(self.skipSeconds)) + " " + i18n_sec)
        self.controlLabel2.setLabel(i18n_place + ": " + formatted_place)

        place_to_seek = self.startTime + self.cumulativeSkipSeconds

        if place_to_seek < 0:
            place_to_seek = 0

        xbmc.Player().seekTime(place_to_seek)


if xbmc.Player().isPlayingVideo():
    dialog = QuickSkipDialog()
    timeout = Timer(AUTO_CLOSE_TIMEOUT_SECONDS, dialog.close)
    timeout.start()
    dialog.doModal()
    del dialog
