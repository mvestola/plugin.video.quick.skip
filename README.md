# QuickSkip for Kodi 

<img src="icon.png" alt="QuickSkip logo"/>

## Introduction

This addon for Kodi (former XBMC) allows you to fast skip commercials with a few button presses. All you need to to is to press the up arrow and then click right/left. Similar functionality was provided in Topfield PVR set top boxes as an TAP addon (SkipIt).

Typical usage is this:
1. You are playing a recorded TV show and commercials are starting. You want to skip to place where the commercials have ended and the TV show continues.
1. Press `up` key to show the add-on dialog.
1. Press `right` to skip 180 seconds forward.
1. You see that commercials are still running. Press `right` key again to skip 180 seconds forward.
1. You see that commercials are not running anymore so you skipped too far. Press `left` key to skip 180 / 2 = 90 seconds backwards.
1. You see that commercials are still not running so you have to skip a little bit more backwards. Press `left` key again to skip 90 / 2 = 45 seconds backwards.
1. You see that commercials are now running so you have to skip a little bit more forward. Press `right` key to skip 45 / 2 = 22 seconds forward.
1. You see that the commercial break is just ending and the TV show continues. Don't press anything and the add-on dialog will disappear in a few seconds.

Usage might sound complicated at first but it is very powerful, intuitive and fast way to skip commercials. You can skip commercials in just a few seconds by pressing `right` and `left` keys to the direction where the commercial break is ending and TV show continues.

## Installation to Kodi

1. Download this repository as [zip file](https://github.com/mvestola/plugin.video.quick.skip/archive/master.zip).
1. Copy the zip file to the computer you are running Kodi.
1. Install the plugin from the zip file using the Kodi addon manager
1. Define the key that will launch the add-on. You have two options to do this:
   1. Use [Keymap editor add-on](http://kodi.wiki/view/Add-on:Keymap_Editor) to configure the key. Select `Programs...Keymap Editor...Edit...Fullscreen Video...Add-ons...Launch QuickSkip` and Input the `up` key. Finally save Keymap Editor settings.
   1. Make SSH to kodi and create user defined keymap file to `~/.kodi/userdata/keymaps/quick-skip-keymap.xml` with contents same as in file [/resources/data/quick-skip-keymap.xml](/resources/data/quick-skip-keymap.xml).

## Usage in Kodi

1. Open some video file and play it in fullscreen mode
1. Click `up` key from your keyboard or remote control: a dialog window should appear to the top left corner
1. Use `left` and `right` arrow keys from your keyboard or remote control to skip to direction you want
1. You can press `OK` key to change the time to skip from 180 sec -> 60 sec -> 10 sec.
1. Close the dialog with `Esc` from your keyboard or `back` from your remote control. Or just wait for a few seconds and the dialog will automatically close.
