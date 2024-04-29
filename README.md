# dyndnsctrl

## Development

Clone the repo and install dependencies into a local virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate.fish
pip install --upgrade pip
pip install --editable .
dyndnsctrl
```

## Configuration

Optional environmental variables:

```shell
DNSCONFIG_PATH=./dnsconfig.js
SUBDOMAIN=homelab # e.g. homelab.example.com
UNATTENDED=1
LOG_LEVEL=info # or debug
```

## Systemd

Sample configuration

`~/.config/systemd/user/dyndnsctrl.service`:

```ini
[Unit]
Description=Run dyndnsctrl

[Service]
Type=oneshot
ExecStart=dyndnsctrl

[Install]
WantedBy=multi-user.target
```

`~/.config/systemd/user/dyndnsctrl.timer`:

```ini
[Unit]
Description=Check our IP address every 15 minutes

[Timer]
OnBootSec=15min
OnUnitActiveSec=15min

[Install]
WantedBy=timers.target
```

Enabling the user service unit timer:

```shell
systemctl --user daemon-reload
systemctl --user enable --now dyndnsctrl.timer
```
