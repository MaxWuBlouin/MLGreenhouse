import devices

devices.connect_devices()
print(devices.send_message("OUTLET", "test"))
print(devices.send_message("WRONG", "message"))