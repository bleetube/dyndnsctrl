# dyndnsctrl

Automatically keep a DNS record set to your current IP address using dnscontrol.

## Installation

See development, no package has been published yet.

## Usage

Run `dyndnsctrl` in the same directory that you would run `dnscontrol`.

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
DOMAIN=example.com
UNATTENDED=1
LOG_LEVEL=info # or debug
```

These environmental variables make the script flexible and adaptable for different operational environments and use cases, such as automating DNS updates in response to IP address changes for a specific subdomain.

The optional `DOMAIN` variable will use `dnscontrol --domains` option to limit the update to a specific domain, which is useful if you have more than one domain. It will reduce the amount of api calls that dnscontrol does.

## Systemd

In order to automate the process of updating DNS records with `dnscontrol` whenever your public IP changes, you can utilize systemd to schedule and run a Python script periodically. Here’s how to configure systemd with user services and timers to manage this task:

### Systemd Configuration for DNS Updates

The following steps will guide you through setting up a user service and a timer using systemd. This will ensure that your DNS records are automatically updated on a regular schedule.

#### Step 1: Create the Service File

Create a systemd service file to define how the script should run. This file will specify the script to execute, the type of service, and its working directory.

1. **Create the service file** at `~/.config/systemd/user/dyndnsctrl.service` with the following content:

    ```ini
    [Unit]
    Description=Run dyndnsctrl

    [Service]
    Type=oneshot
    ExecStart=dyndnsctrl
    EnvironmentFile=/path/to/.env
    WorkingDirectory=/home/me/dnscontrol

    [Install]
    WantedBy=multi-user.target
    ```

    - `Type=oneshot` indicates that the service runs the script once and then exits.
    - `ExecStart` should point to the Python executable followed by the path to your script. Modify the path to match where your Python script is located.
    - `WorkingDirectory` is set to the directory containing your DNS control files.

#### Step 2: Create the Timer File

Create a systemd timer file to schedule when the service runs. This timer will activate the service according to a set interval.

1. **Create the timer file** at `~/.config/systemd/user/dyndnsctrl.timer` with the following content:

    ```ini
    [Unit]
    Description=Check our IP address every 15 minutes

    [Timer]
    OnBootSec=15min
    OnUnitActiveSec=15min

    [Install]
    WantedBy=timers.target
    ```

    - `OnBootSec` specifies how long after booting the system the timer should first activate.
    - `OnUnitActiveSec` sets the interval between each activation of the timer.

#### Step 3: Enable and Start the Timer

After creating the service and timer files, you need to tell systemd to start using these new configurations.

1. **Reload systemd to recognize new or changed units**:

    ```shell
    systemctl --user daemon-reload
    ```

2. **Enable and start the timer** to begin scheduling your script:

    ```shell
    systemctl --user enable --now dyndnsctrl.timer
    ```

    - `enable` configures the timer to start automatically at boot.
    - `--now` starts the timer immediately without needing to reboot.

With these configurations in place, your Python script will automatically run every 15 minutes, ensuring that any changes to your public IP address are quickly reflected in your DNS settings. This setup is particularly useful for dynamic IP environments, such as home networks or small offices without static IP addresses. Be sure to replace paths and other details with those specific to your environment.