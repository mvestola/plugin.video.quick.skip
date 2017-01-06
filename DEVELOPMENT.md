## Useful resources

### Kodi documentation

* http://kodi.wiki/view/Add-on_development
* http://mirrors.kodi.tv/docs/python-docs/
* https://codedocs.xyz/xbmc/xbmc/class_x_b_m_c_addon_1_1xbmcgui_1_1_window_dialog.html
* http://kodi.wiki/view/skip_steps
* http://kodi.wiki/view/Add-on_structure

## Tutorials

* http://www.xbmc4xbox.org.uk/wiki/HOW-TO:Write_Python_Scripts_for_XBMC#add_.28and_remove.29_text_label

### Other add-ons

* https://github.com/zag2me/script.hello.world
* https://github.com/b-jesch/service.sleepy.watchdog
* https://github.com/tamland/xbmc-keymap-editor

## Forum threads

* http://forum.kodi.tv/showthread.php?tid=287443
* http://forum.kodi.tv/showthread.php?tid=263356
* http://forum.kodi.tv/showthread.php?tid=17106

# Testing locally

Update code changes to Kodi:
```
rm -rf ~/.kodi/addons/plugin.video.quick.skip/;cp -r ~/Programming/Python/plugin.video.quick.skip ./
```

Kodi logs:

```
less ~/.kodi//temp/kodi.log
```