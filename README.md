# plantApp


## Installation

List boards to get the right USB port <br />
`arduino-cli board list`

Build software <br />
`arduino-cli compile --fqbn arduino:avr:uno plantApp`

Upload hex to arduino board <br />
`arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno plantApp`

## Use Arduino serial in screen terminal

Start serial in ubuntu <br />
`sudo screen /dev/ttyACM0 9600` 

### Run pumps in serial terminal  

Fertilizer pump number 1 (120 sec.) <br />
`run_fertilizer_pump13120` 

Fertilizer pump number 2 (3 sec.) <br />
`run_fertilizer_pump12003`

Fertilizer pump number 3 (3 sec.) <br />
`run_fertilizer_pump11003`

Fertilizer pump number 4 (3 sec.) <br />
`run_fertilizer_pump07003`

Water pump (3 sec.) <br />
`run_water_pump003` 

Kill serial terminal session <br />
`ctrl + a, k, y`

## Start app

Creat virtual environment <br />
`python3 -m venv venv`

Activate python virtual environment <br />
`source venv/bin/activate`

Install requirements <br />
`pip3 install -r requirements.txt`

Start plantApp <br />
`python3 thingsboard_recv.py`


