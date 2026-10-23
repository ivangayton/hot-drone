# Pixhawk setup and parameters

## Flashing setup
- Connect the new (or to-be-reflashed) Pixhawk6C to a computer running QGroundControl. Hit the configure button. Click the Firmware tab. 
- The device should be already selected via its serial port in the dropdown, otherwise select it. Hit the Flash button. It'll instruct you to unplug the Pixhawk and plug it back in to get it into flashing mode.
- Select the Chibios OS (normally the default already) and the Pixhawk6C-bdshot (Holybro) option. 
- Once the Pixhawk is flashed, QGroundControl should announce that "Configuration tasks remain before this vehicle is ready to fly. Open the red-marked components on the left to finish setup."
- Start with the Frame, which should be a Quad X. 
- Go to Parameters, push the Tools button on the upper right, choose Load from file for review, and select the x500v2.params file from this repo. Press Open. It'll complain that there are missing parameters which have been skipped; that's ok because they're fine as the defaults. Everything we need to overwrite is in the .params file.

TODO: remove unnecessary stuff from params file

NOTE: the serial ports on the Pixhawk6C Pro we have don't match the Holybro documentation or the standards expected by MavLink and QGroundControl.

- Telem1 maps to Serial1 in the Ardupilot params
- Telem2 maps to Serial2 in the Ardupilot params
- Telem3 maps to Serial5 in the Ardupilot params

NOTE: in PX4 the mapping is different, as are the parameter names. If and when we want to get any of this stuff working with PX4, we'll need to investigate the serial mapping among many other things.

### 2026-10-16 Further Ken and Ivan setup
The KB2040 coordinator for the camera module is flashed&mdash;for the moment&mdash;with a [mock setup implementing a "fake" camera component](https://github.com/mrkensan/tri-cam-kb2040/) to exercise the interaction between the flight controller, ground station, and camera subsystem (that interaction won't change when we add the RPis with the actual cameras, we'll just add the actual photo captures etc). This interaction happens in MavLink, so the flight controller parameters need to be set correctly. If they aren't, the camera controls do not appear in the QGroundControl UI, and (rather more importantly) the flight controller won't be able to instruct the camera to start capturing photos.

The KB2040 identifies itself over a serial connection to the Telem3 port on the Pixhawk as a MavLink camera component with ID 100 (kinda standard for MavLink cameras) running at 57600 baud. Therefore the Ardupilot parameter SERIAL5_BAUD must be 57600 and the SERIAL5_PROTOCOL must be MAVLink2.

The CAM1_TYPE parameter should be set to MavLinkCamV2.

In QGroundControl (Android or PC), the "Fly" view should contain a camera control in the upper right hand portion of the screen. There's a trigger button and a settings gear icon; the settings can be for single or time-lapse photography (we'll want this set to time-lapse with a 1-second interval). If that camera control widget doesn't appear, it means that the flight controller has not been able to discover a camera peripheral. The QGroundControl MAVLink Inspector view gives an overview of MavLink protocol serial traffic; if all is well the camera subsystem will be visible with component ID 100, emitting a hearbeat at 1 hz and (when triggered) CAMERA_CAPTURE_STATUS, CAMERA_IMAGE_CAPTURED (also nominally at 1 hz if it's been triggered appropriately), and COMMAND_ACK (you can filter the view in the Inspector to only show messages from component 100 i.e. our camera subsystem). 

