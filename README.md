# plantApp


## Installation

List boards to get the right USB port \
`arduino-cli board list`

Build software \
`arduino-cli compile --fqbn arduino:avr:uno plantApp`

Upload hex to arduino board \
`arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno plantApp`

## Use Arduino serial in screen terminal

Start serial in ubuntu \
`sudo screen /dev/ttyACM0 9600` 

### Run pumps in serial terminal  

Fertilizer pump number 1 (120 sec.) \
`run_fertilizer_pump13120` 

Fertilizer pump number 2 (3 sec.) <br />
`run_fertilizer_pump12003`

Fertilizer pump number 3 (3 sec.) <br />
`run_fertilizer_pump11003`

Fertilizer pump number 4 (3 sec.) \
`run_fertilizer_pump07003`

Water pump (3 sec.) \
`run_water_pump003` 

Kill serial terminal session \
`ctrl + a, k, y`

## Start app

Activate python virtual environment \
`source venv/bin/activate`

Start plantApp \
`python thingsboard_recv.py`


