# compile software
arduino-cli compile --fqbn arduino:avr:uno plantApp

# upload hex to arduino board
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno plantApp