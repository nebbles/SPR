# Logbook

## Overview

1. [02 Nov](#2-November-2018-↑)
2. [16 Nov](#16-November-2018-↑)
3. [23 Nov](#23-November-2018-↑)
4. [30 Nov](#30-November-2018-↑)
5. [17-18 Jan](#18-January-2019-↑)
5. [19 Jan](#19-January-2019-↑)

## [22 January 2019 ↑](#overview)

- Continued with (software) preparation for new camera mount.

## [21 January 2019 ↑](#overview)

- Installed new Raspberry Pi casing which is mounted to the frame of the Prusa.
- Connected camera with new 2m cable. Used original position of bottom left corner for the time being.

## [19 January 2019 ↑](#overview)

- Finalised usage of reverse tunnel to remotely access web interface of Prusa octoprint. This is written in the form of a bash script that will be stored in the `misc/` directory. Script is called `serve-web`. See file for more information.
- Made a new cronjob that would start up the reverse tunnel correctly after a Pi reboot: `@reboot /home/pi/bin/serve-web > /home/logs/serve-web.log 2>&1`
- Investigating some additional useful plugins for octoprint that may help with printer management (marks signify package was used):
    - [ ] [Octoprint Anywhere](https://plugins.octoprint.org/plugins/anywhere/)
    - [x] [Exclude Region](https://plugins.octoprint.org/plugins/excluderegion/)
    - [x] [Detailed Progress](https://plugins.octoprint.org/plugins/detailedprogress/)
    - [x] [Print History](https://plugins.octoprint.org/plugins/printhistory/)
    - [x] [Print Time Genius](https://plugins.octoprint.org/plugins/PrintTimeGenius/)
    - [x] [Octolapse](https://plugins.octoprint.org/plugins/octolapse/)
    - [x] [File Manager](https://plugins.octoprint.org/plugins/filemanager/)
    - [ ] [Multiple Upload](https://plugins.octoprint.org/plugins/MultipleUpload/)
    - [ ] [STL Viewer](https://plugins.octoprint.org/plugins/stlviewer/)
    - [ ] [Cancel Object](https://plugins.octoprint.org/plugins/cancelobject/)
    - [x] [Extra Distance](https://plugins.octoprint.org/plugins/extradistance/)
    - [ ] [Fan Speed Control](https://plugins.octoprint.org/plugins/fanslider/)
    - [ ] [Floating Nav Bar](https://plugins.octoprint.org/plugins/floatingnavbar/)
    - [ ] [Gcode Editor](https://plugins.octoprint.org/plugins/GcodeEditor/)
    - [x] [Simple Emergency Stop](https://plugins.octoprint.org/plugins/simpleemergencystop/)
    - [ ] [Better Heater Timeout](https://plugins.octoprint.org/plugins/BetterHeaterTimeout/)
    - [x] [Nav Bar Temp](https://plugins.octoprint.org/plugins/navbartemp/)
    - [ ] [Enclosure](https://plugins.octoprint.org/plugins/enclosure/)
    - [x] [Themeify](https://plugins.octoprint.org/plugins/themeify/)
    - [ ] [Tab Order](https://plugins.octoprint.org/plugins/taborder/)
    - [x] [Printer Statistics](https://plugins.octoprint.org/plugins/stats/)

- [Created](https://nerderati.com/2011/03/17/simplify-your-life-with-an-ssh-config-file/) an SSH config (`nano ~/.ssh/config`) to use an [SSH jump](https://wiki.gentoo.org/wiki/SSH_jump_host) to reach the Pi behind Imperial firewall:

    ```
    Host spr-prusa
            Hostname spr-prusa
            User pi
            ProxyJump serveo.net

    # Equivalent to: ssh -J serveo.net pi@spr-prusa
    ```

    This was done whilst the serveo reverse tunnel was already temporarily established on the Pi side. At this point I had not developed a script to run it automatically: `ssh -R spr-prusa:22:localhost:22 serveo.net`

- Plan to use [SSH keys](https://askubuntu.com/questions/46930/how-can-i-set-up-password-less-ssh-login) for passwordless login on SSH. Followed the following steps:

    ```
    $ ssh-keygen

    ... key is created ...

    $ ssh-copy-id spr-prusa
    ```

    Note that the `-i` flag should be used to specify which identy you want to be copied to the remote host.

- With automatic log-in and a short ssh command set up using a config file to access the Pi remotely, the final step was just to ensure that the SSH reverse tunnel set up previously stays alive. For this a script was set up similar to before and is named `serve-ssh` which can be found in the `misc/` directory. This new script will handle the tunnel responsible for administrative access through port 22 rather than web traffic aimed for port 80 to reach the Octoprint dashboard.

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