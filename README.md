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

