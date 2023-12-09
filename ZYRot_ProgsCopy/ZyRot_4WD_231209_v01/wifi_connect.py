SSID = "HogPC"
PWD = "43215678"

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PWD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    

#do_connect()

    