# StupidArtnet

(Very) Simple Artnet implementation in Python

### Notes

Artnet libraries tend to be complicated and hard to get off the ground. Sources were either too simple and didn't explain the workings or become too complex by fully implementing the protocol. <br />
This is mean as an implementation focusing on DMX over Artnet only.

I am also doing my best to comment the sections where the packets is build. In an effort to help you understand the protocol and be able to extend it for a more case specific use.

Users looking to send a few channels to control a couple of LEDs, projectors or media servers can use this as reference.

Are you running several universes with different fixture types? I would recommend [ArtnetLibs](https://github.com/OpenLightingProject/libartnet) or the [Python Wrapper for Artnet Libs](https://github.com/haum/libartnet)


### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for detailsls
