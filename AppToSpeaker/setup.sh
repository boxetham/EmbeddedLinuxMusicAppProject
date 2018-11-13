#!/bin/bash

# put bluetooth in discoverable mode
echo -e 'discoverable yes\npairable yes\nquit' | bluetoothctl
