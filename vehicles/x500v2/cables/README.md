# Cable documentation

We're using [WireViz}(https://github.com/wireviz/WireViz) a YAML protocol and renderer for describing connectors.

This directory contains the raw YAML describing each of the connectors on the drone, as well as an SVG and PNG rendering of each.

It's possible to install WireViz locally, but as long as you have an Internet connetion it's probably easier to use an online converter. We're using [WireViz.app](https://www.wireviz.app/).

Lots of documentation on how to use it. For the most part the PNG/SVG renders should be sufficiently clear to fabricate and use the appropriate connectors.


### POWER on Pixhawk to the APM Power Module
![](PNG/power1-to-power-module.png)

### PPM/SBUS RC on Pixhawk to the right socket on the RC receiver
![PPM/SBUS RC to RC Receiver Right](PNG/ppm-sbus-rc-to-rc-receiver-right.png)

### TELEM1 on Pixhawk to the left socket on the RC receiver
![TELEM1 to RC Receiver left](PNG/telem1-to-rc-receiver-left.png)

SAFETY on Pixhawk to the Safety Switch
![SAFETY to Safety Switch](PNG/safety-to-safety-switch.png)

IO/PWM OUT on Pixhawk to PWM MODULE B-CUBE PWM IN
![IO/PWM OUT to PWM MODULE B-CUBE PWM IN](PNG/io-pwm-out-to-pwm-module-b-cube-pwm-in.png)

### TELEM3 on Pixhawk to the Camera Subsystem
![TELEM3 to Camera](PNG/telem3-to-camera.png)
