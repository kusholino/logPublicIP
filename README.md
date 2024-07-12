# logPublicIP

## Overview
Fetches the current public IP address and compares it to the old IP address. If the IP changed a e-mail notification will be sent with the timestamp and the new IP address. Same information will be written into a log file.

## Features
- Automatically detects changes in the public IP address.
- Writes IP address into log file with the current timestamp.
- Offers the option to send a notification e-mail on IP change.
- Uses a configuration file to set the parameters for the service.
- Offers option to install dependencies using proxy

## Setup
To install this service follow the steps below:

1. Clone the Repository

    `git clone https://github.com/kusholino/logPublicIP`

2. Install Dependencies and setup the service and Start the Service. This must be run with root permissions

    `cd logPublicIP`

    Without a proxy:
    
    `python3 setup.py`

    With a proxy:
    
    `python3 setup.py --proxy http://ip:port`

## Config File
To enable e-mail notifications set the value of send_mail in the config file to True.

 `send_mail = True`



## Information
Keep in mind, i used a smtp server that doesnt support tls and is only reachable within my private network.

To start the service:

`systemctl start logPublicIP.service`
