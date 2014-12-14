raspberry-led-garland
=====================

systemd service
---------------

Copy to the `raspberry-led-garland` directory to the `/opt/raspberry-led-garland` or create symlink like this command:
```
sudo ln -s /home/jheka/raspberry-led-garland /opt/raspberry-led-garland
```

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
