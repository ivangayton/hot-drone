# GNSS Dataloggging for PPK Positioning

Since the Global Navigation Satellite System (GNSS, often confused with GPS which is the proper name of the US GNSS system) chip we are using is a u-blox ZED-F9P dual-frequency receiver, we can peform Post-Processing Kinematic (PPK) correction to improve the geolocation of the photographs. This involves recording the raw GNSS satellite data streams and later combining them (post-processing) with similar streams from a base station to correct the positions. 

We've added a tiny serial datalogger to record the raw GNSS readings, the [Sparkfun Open Log DEV-13712](https://www.sparkfun.com/sparkfun-openlog.html). There's a [hookup guide for it here](https://learn.sparkfun.com/tutorials/openlog-hookup-guide). 

Without kinematic correction, the positional accuracy of the GNSS on the drone is around 2-4 m. With correction it's theoretically closer to 5 cm. In reality it's usually more like 20 cm on drones, mostly because it's quite difficult to get exact synchronization between the exact moment of photo/line/pixel capture—from a platform moving at 10 m/s, wobbling, and not necessarily maintaining a constant speed—and the position reading from the GNSS chip (I know that some people think this is an easy problem, by all means come fix it, bro!). Still, even 20 cm accuracy is massively better than 2-4 m accuracy for image processing and georeferencing purposes!

_NOTE: it's also possible to use the F9P for Real-Time Kinematic (RTK) correction, allowing the drone to have ~5-20 cm positional accuracy in, well, real time! This is great because it eliminates some post-processing steps that can be a hassle, and can also help for precise landings (for the moment we don't have the optical flow stuff that allows many commercial drones to land within centimeters of their takeoff point despite having low GNSS accuracy). This probably requires an additional dedicated radio receiver to receive the correction data stream, so we haven't gotten to this yet._


