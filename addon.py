import xbmcaddon
import xbmcgui
import xbmc

# Add following XML to userdata/keymaps/quick-skip.xml
# <?xml version="1.0" encoding="UTF-8"?>
# <keymap>
#   <global>
#     <keyboard>
#       <space>RunAddon(script.quick.skip)</space>
#     </keyboard>
#   </global>
# </keymap>

# See key codes from https://github.com/xbmc/xbmc/blob/master/xbmc/input/Key.h
ACTION_MOVE_LEFT =  1
ACTION_MOVE_RIGHT = 2
ACTION_SELECT_ITEM = 7
ACTION_PREVIOUS_MENU = 10

xbfont_left = 0x00000000
xbfont_right = 0x00000001
xbfont_center_x = 0x00000002
xbfont_center_y = 0x00000004
xbfont_truncated = 0x00000008

SKIP_LEFT = "left"
SKIP_RIGHT = "right"

addon = xbmcaddon.Addon()

class QuickSkipDialog(xbmcgui.WindowDialog):

    def __init__(self):
        self.skipSeconds = 180.0
        self.cumulativeSkipSeconds = 0.0
        self.startTime = None
        self.previousDirection = None
        self.directionChanged = False

        self.addControl(xbmcgui.ControlImage(10, 10, 200, 140, addon.getAddonInfo('path')+'/resources/background.png'))

        self.controlLabel1 = xbmcgui.ControlLabel(x=20, y=20, width=180, height=60, label="", alignment=xbfont_center_y|xbfont_center_x)
        self.addControl(self.controlLabel1)
        self.controlLabel1.setLabel("Jump: 180 sec")

        self.controlLabel2 = xbmcgui.ControlLabel(x=20, y=80, width=180, height=60, label="", alignment=xbfont_center_y|xbfont_center_x)
        self.addControl(self.controlLabel2)
        self.controlLabel2.setLabel("Place: 00:00")


    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.close()
        elif action == ACTION_SELECT_ITEM:
            if not self.directionChanged:
                if int(self.skipSeconds) == 180:
                    self.skipSeconds = 60.0
                    self.controlLabel1.setLabel("Jump: " + str(int(self.skipSeconds)) + " sec")
                elif int(self.skipSeconds) == 60:
                    self.skipSeconds = 10.0
                    self.controlLabel1.setLabel("Jump: " + str(int(self.skipSeconds)) + " sec")
                else:
                    self.close()
            else:
                self.close()
        elif action == ACTION_MOVE_LEFT:
            self.handleSkip(SKIP_LEFT)
        elif action == ACTION_MOVE_RIGHT:
            self.handleSkip(SKIP_RIGHT)
        else:
            pass


    def handleSkip(self, direction):
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

        self.controlLabel1.setLabel("Jump: " + str(int(self.skipSeconds)) + " sec")
        self.controlLabel2.setLabel("Place: " + formatted_place + " sec")

        place_to_seek = self.startTime + self.cumulativeSkipSeconds

        if place_to_seek < 0:
            place_to_seek = 0

        xbmc.Player().seekTime(place_to_seek)


if xbmc.Player().isPlayingVideo():
    dialog = QuickSkipDialog()
    dialog.doModal()
    del dialog
