# Mount a Windows Shared Folder on Ubuntu

## Step 1: Install `cifs-utils`

First, you need to install the `cifs-utils` package, which provides support for mounting and managing CIFS (SMB) network file systems.

```bash
sudo apt update
sudo apt install cifs-utils
```

## Step 1: Create a Mount Point
Choose or create a directory where you want to mount the shared folder. For example:

```bash
sudo mkdir -p /mnt/shared
```

## Step 3: Mount the Shared Folder
Use the mount command to mount the shared folder. You'll need the network path to the shared folder and, if required, the credentials (username and password).

```bash
sudo mount -t cifs //server_name/shared_folder /mnt/shared -o username=your_username,password=your_password
```
Replace server_name with the name or IP address of your Windows machine, shared_folder with the name of the shared folder, and your_username and your_password with the appropriate credentials.

## Step 5: Test the Mount
To verify that the shared folder is mounted correctly, you can list the contents of the mount point:

```bash
ls /mnt/shared
```

## Step 6: Boot Services
### Mount Shared Service
1. Create the service file

```bash
sudo nano /etc/systemd/system/mount-shared.service
```

2. Add the configuration
```bash
[Unit]
Description=Mount Shared Drive
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/mount -t cifs //192.168.10.190/F1_Drop_Main /mnt/shared -o credentials=/etc/samba/creds --verbose
ExecStop=/usr/bin/umount /mnt/shared
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

3. Create Credentials File
```bash
sudo nano /etc/samba/creds
```

4. Add the following with your username and password:
```bash
username=<username>
password=<password>
```

5. Secure the file
```bash
sudo chmod 600 /etc/samba/creds
```

6. Reload the daemon

```bash
sudo systemctl daemon-reload
```

7. Enable the service

```bash
sudo systemctl enable mount-shared.service
```

8. Start the service

```bash
sudo systemctl start mount-shared.service
```

9. Check the status
```bash
systemctl status mount-shared.service
```

10. Verify the mount point
```bash
df -h /mnt/shared
```



### Print Controller Service
1. Create the service file

```bash
sudo nano /etc/systemd/system/mount-shared.service
```

2. Add the configuration
```bash
[Unit]
Description=Run Docker Compose for AR Print Controller
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
RemainAfterExit=yes
WorkingDirectory=/home/kicks-kiosk/ar-print-controller
ExecStartPre=/usr/local/bin/docker-compose down -v
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down -v
Restart=always
RestartSec=2s

[Install]
WantedBy=multi-user.target
```

3. Reload the daemon

```bash
sudo systemctl daemon-reload
```

4. Enable the service

```bash
sudo systemctl enable ar-print-controller.service
```

5. Start the service

```bash
sudo systemctl start ar-print-controller.service
```

6. Check the status
```bash
sudo systemctl status ar-print-controller.service
```
