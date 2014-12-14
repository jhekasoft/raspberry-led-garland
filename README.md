Raspberry Pi LED garland
========================

Installation
------------

You must have installed `python3`, `libbcm2835` library (Arch Linux) and `RPi.GPIO` Python library.

Copy `raspberry-led-garland` directory to the `/opt/raspberry-led-garland` or create symlink like this:
```
sudo ln -s /home/jheka/raspberry-led-garland /opt/raspberry-led-garland
```

Running
-------
```
sudo python3 /opt/raspberry-led-garland/garland.py
```

systemd service
---------------

You must have `/opt/raspberry-led-garland` directiory (see Installation).

Copy file `systemd/garland.service` to the `/etc/systemd/system/` directory (Arch Linux).

Then run for autostart:
```
sudo systemctl enable garland.service
```

Run service:
```
sudo systemctl start garland.service
```

Stop service:
```
sudo systemctl stop garland.service
```
