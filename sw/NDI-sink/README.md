# NDI sink for Colorlight LED driver mod

This script snds a NDI signal to the LED cube.

It is intended to be used with LED Mapping tools like MadMapper, Resolume or Touchdesigner.

## Dependencies
* nodejs
* a working node gyp setup
* (probably) NDI SDK; Download & install from newtek

## Setup
* `yarn install` or `npm install`

## Usage
* Create a `64*384px` NDI source
* run `node index.js`
* find your source in the list; if it is missing, add the source PC's ip to `extraIPs` at `index.js@29`
* run `node index.js --source <source index>`, e.g. `node index.js --source 0`

## Map content onto it
