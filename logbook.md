# Logbook

1. [02 Nov](#2-November-2018)
2. [16 Nov](#16-November-2018)
3. [23 Nov](#23-November-2018)
4. [30 Nov](#30-November-2018)

## 2 November 2018

- Initial search into 3D print errors (document on Drive). Further categorisation of errors still to come and analysis of which are able to visual detection and which can be potentially corrected in realtime through Gcode control is yet to be set.
- A brief shopping list has been put together to understand what is needed to get some primitive control and testing up and running. Focus will be on a single point of camera to start with.
- Control will be over serial using Python if possible. This will allow for more granular control. Some existing source code and methodologies have been found online through preliminary research and will be verified once the hardware is up and running.

## 16 November 2018

- Spent day trying to get BQ Hephestos 2 calibrated and operating properly. Mostly failed. Had particular issues trying to get the hot end extrude consistently.
- Plan to source alternative backup printer if the issue continues.

## 23 November 2018

- New printer, Prusa MK2 (lent by Prof. P Cheung) is up and running – calibration took most of the day but now is acting well.
- Basic control of the printer with Python over a serial connection has been proven but not yet tested extensively.
- Next up:
  - will be trying to see if I can stream a whole gcode file to the printer in realtime
  - will look into gcode injection which will be needed for taking photographs (getting print head out the way)

## 30 November 2018

- Found a simple protective frame for the Pi. Started printing it.
- Identified an appropriate flex cable. for the camera. About to look into a camera mount design.
- Checked to see if there was any way to stream a preview of the video stream over SSH. 
- Want to avoid VNC due to clunky workflow.
- Looking into streaming to a remote web browser instead
- Want to set up stream via python rather than bash
- Found a python based video stream server for camera https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/