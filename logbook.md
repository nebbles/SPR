# Logbook

## Overview

1. [02 Nov](#2-November-2018)
2. [16 Nov](#16-November-2018)
3. [23 Nov](#23-November-2018)
4. [30 Nov](#30-November-2018)
5. [17-19 Jan](#19-January-2019)

## [19 January 2019 ↑](#overview)

- Finalised usage of reverse tunnel to remotely access web interface of Prusa octoprint. This is written in the form of a bash script that will be stored in the `misc/` directory. Script is called `serve-web`. See file for more information.
- Made a new cronjob that would start up the reverse tunnel correctly after a Pi reboot: `@reboot /home/pi/bin/serve-web > /home/logs/serve-web.log 2>&1`
- Plan to use [SSH keys](https://askubuntu.com/questions/46930/how-can-i-set-up-password-less-ssh-login) for passwordless login on SSH.
- Prepared for new script that will serve SSH tunnel for remote administration. This will forward port 22 instead of the web port (80) as before.
- Investigating some additional useful plugins for octoprint that may help with printer management (marks signify package was used):
    - [ ] [Octoprint Anywhere](https://plugins.octoprint.org/plugins/anywhere/)
    - [ ] [Exclude Region](https://plugins.octoprint.org/plugins/excluderegion/)
    - [ ] [Detailed Progress](https://plugins.octoprint.org/plugins/detailedprogress/)
    - [ ] [Print History](https://plugins.octoprint.org/plugins/printhistory/)
    - [ ] [Print Time Genius](https://plugins.octoprint.org/plugins/PrintTimeGenius/)
    - [ ] [Octolapse](https://plugins.octoprint.org/plugins/octolapse/)
    - [ ] [File Manager](https://plugins.octoprint.org/plugins/filemanager/)
    - [ ] [Multiple Upload](https://plugins.octoprint.org/plugins/MultipleUpload/)
    - [ ] [STL Viewer](https://plugins.octoprint.org/plugins/stlviewer/)
    - [ ] [Cancel Object](https://plugins.octoprint.org/plugins/cancelobject/)
    - [ ] [Extra Distance](https://plugins.octoprint.org/plugins/extradistance/)
    - [ ] [Fan Speed Control](https://plugins.octoprint.org/plugins/fanslider/)
    - [ ] [Floating Nav Bar](https://plugins.octoprint.org/plugins/floatingnavbar/)
    - [ ] [Gcode Editor](https://plugins.octoprint.org/plugins/GcodeEditor/)
    - [ ] [Simple Emergency Stop](https://plugins.octoprint.org/plugins/simpleemergencystop/)
    - [ ] [Better Heater Timeout](https://plugins.octoprint.org/plugins/BetterHeaterTimeout/)
    - [ ] [Nav Bar Temp](https://plugins.octoprint.org/plugins/navbartemp/)
    - [ ] [Enclosure](https://plugins.octoprint.org/plugins/enclosure/)
    - [x] [Themeify](https://plugins.octoprint.org/plugins/themeify/)
    - [ ] [Tab Order](https://plugins.octoprint.org/plugins/taborder/)
    - [ ] [Printer Statistics](https://plugins.octoprint.org/plugins/stats/)

## [18 January 2019 ↑](#overview)

- Started manufacturing a new camera mount that will be fixed relative to z axis of hotend.
- Further research on reverse tunnelling to assist with remote monitoring.

## [17 January 2019 ↑](#overview)

- Rebuilt SD with Octoprint on and reinstalled remot3.it (weaved) as a backup to remote connection. Note that my effective `wpa_supplicant.conf` for Imperial wifi is stored in the `misc/` directory of this project.
- 3D printed a camera mount for the Pi camera. Fixed it to lower right corner of bed. Unfortuantely I think there is risk of this being too low an angle; camera being fixed relative to the bed is useful however.
- Manufactured a case for Pi to secure to the Prusa. This requries a longer flex cable from Pi to camera however.
- Ordered two longer camera flex cables for Prusa Pi and ultimately the Wanhao Pi once set up.
- Wanhao printer set up an calibrated (no accompanying Pi yet). Some test prints run on it.
- The intial aim is to have Octoprint set up for both printers and taking time lapse photos. The quality and control of these images from the octoprint interface has to be established. This may mean that more granualr control is needed through an alternative, or custom, plugin to the octoprint platform.
- Initial research conducted into how to use reverse tunnelling to bypass Imperial firewalls and remotely monitor the printers.

## [30 November 2018 ↑](#overview)

- Found a simple protective frame for the Pi. Started printing it.
- Identified an appropriate flex cable. for the camera. About to look into a camera mount design.
- Checked to see if there was any way to stream a preview of the video stream over SSH. 
- Want to avoid VNC due to clunky workflow.
- Looking into streaming to a remote web browser instead
- Want to set up stream via python rather than bash
- Found a python based video stream server for camera https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/

## [23 November 2018 ↑](#overview)

- New printer, Prusa MK2 (lent by Prof. P Cheung) is up and running – calibration took most of the day but now is acting well.
- Basic control of the printer with Python over a serial connection has been proven but not yet tested extensively.
- Next up:
  - will be trying to see if I can stream a whole gcode file to the printer in realtime
  - will look into gcode injection which will be needed for taking photographs (getting print head out the way)

## [16 November 2018 ↑](#overview)

- Spent day trying to get BQ Hephestos 2 calibrated and operating properly. Mostly failed. Had particular issues trying to get the hot end extrude consistently.
- Plan to source alternative backup printer if the issue continues.

## [2 November 2018 ↑](#overview)

- Initial search into 3D print errors (document on Drive). Further categorisation of errors still to come and analysis of which are able to visual detection and which can be potentially corrected in realtime through Gcode control is yet to be set.
- A brief shopping list has been put together to understand what is needed to get some primitive control and testing up and running. Focus will be on a single point of camera to start with.
- Control will be over serial using Python if possible. This will allow for more granular control. Some existing source code and methodologies have been found online through preliminary research and will be verified once the hardware is up and running.