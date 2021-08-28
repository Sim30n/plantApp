# print board list to get the right port
arduino-cli board list

# compile software
arduino-cli compile --fqbn arduino:avr:uno plantApp

# upload hex to arduino board
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno plantApp

# start serial in ubuntu
sudo screen /dev/ttyACM0 9600

# kill serial terminal session
ctrl + a, k, y

# activate virtual environment for python
source venv/bin/activate

# run pumps
run_fertilizer_pump13003
run_fertilizer_pump12003
run_fertilizer_pump11003
run_fertilizer_pump07003
run_water_pump003