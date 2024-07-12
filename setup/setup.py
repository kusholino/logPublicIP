import argparse
import getpass
import subprocess

# Parse command line arguments for proxy
parser = argparse.ArgumentParser(description='Setup script for logPublicIP service with optional proxy.')
parser.add_argument('--proxy', help='Specify a proxy in the format http://your_proxy:port', default='')
args = parser.parse_args()

# Automatically get the current username
username = getpass.getuser()
repo_name = 'logPublicIP'
script_name = 'logIP.py'

# Define the path where the script will reside after cloning
script_path = f'/home/{username}/{repo_name}/{script_name}'

# Service file content
service_content = f'''
[Unit]
Description=Log Public IP Address on IP Change sends email notification
After=network.target

[Service]
Type=simple
ExecStart=python3 {script_path}
User={username}
Restart=on-failure
SyslogIdentifier=logIP
RestartSec=5
TimeoutStartSec=infinity

[Install]
WantedBy=multi-user.target
'''

# Specify the filename for the service file
filename = f'{repo_name}.service'

try: 
    # Write the content to the service file
    with open(filename, 'w') as file:
        file.write(service_content.strip())
    print(f'SETUP: Service file {filename} has been created ... OK')

    subprocess.run(['mv', f'/home/{username}/{repo_name}/{filename}', '/etc/systemd/system/'], check=True)

    print('SETUP: Moved the service file to /etc/systemd/system/ ... OK')

    subprocess.run(['systemctl', 'daemon-reload'], check=True)

    print('SETUP: Reloaded the daemon ... OK')

    # Enable the service (optional, if you want it to start at boot)
    subprocess.run(['systemctl', 'enable', filename], check=True)

    print('SETUP: Enabled the service ... OK')

    # Start the service
    subprocess.run(['systemctl', 'start', filename], check=True)

    print('SETUP: Started the service ... OK')

    # Install the requirements using the proxy if specified
    if args.proxy:
        env = {'http_proxy': args.proxy, 'https_proxy': args.proxy}
        subprocess.run(['pip3', 'install', '-r', 'requirements.txt', '--proxy', args.proxy], cwd=f'/home/{username}/{repo_name}/setup/', env=env, check=True)
        print(f'SETUP: Installed the required packages using the proxy {args.proxy} ... OK')
    else:
        subprocess.run(['pip3', 'install', '-r', 'requirements.txt'], cwd=f'/home/{username}/{repo_name}/setup/', check=True)
        print('SETUP: Installed the required packages ... OK')
    
except subprocess.CalledProcessError as e:
    print(f'SETUP: Subprocess error occurred: {e}')

except Exception as e:
    print(f'SETUP: An error occurred: {e}')

finally:
    print('SETUP: Setup completed ... OK')