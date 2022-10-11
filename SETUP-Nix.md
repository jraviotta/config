# README-Nix.md

- [Install Ubuntu & configure](#install-ubuntu--configure)
  - [Utilities](#utilities)
  - [Snaps](#snaps)
  - [Set zsh to default shell](#set-zsh-to-default-shell)
  - [Create "pbcopy" & "pbpaste"](#create-pbcopy--pbpaste)
  - [Create ssh keys](#create-ssh-keys)
  - [Enable ssh on host](#enable-ssh-on-host)
- [Install ~~config~~](#install-config)
- [Other software & Configuration](#other-software--configuration)
  - [Python](#python)
  - [Google Chrome](#google-chrome)
  - [NoMachine](#nomachine)
  - [Dropbox](#dropbox)
  - [Zotero](#zotero)
  - [VMware Workstation Player](#vmware-workstation-player)
  - [Wine](#wine)
  - [Zoom](#zoom)
- [Old](#old)
  - [Install Psycopg from source code](#install-psycopg-from-source-code)
  - [Lando](#lando)
  - [OneDrive sync](#onedrive-sync)
  - [nbstripout](#nbstripout)
  - [VNC](#vnc)
    - [Fix scaling](#fix-scaling)
    - [Install services](#install-services)
    - [Uninstall services](#uninstall-services)

## Install Ubuntu & configure

- Sign into ubuntu.com, google, microsoft
- Set theme to dark
- Set accessability > text to large

### Utilities

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -q -y \
  zsh \
  curl \
  git-core \
  pandoc \
  virtualbox-qt \
  cockpit
sudo systemctl enable --now cockpit.socket
```

### Snaps

```bash
sudo snap install \
  brave \
  chromium \
  discord \
  docker \
  firefox \
  flameshot \
  libbylinux \
  okular \
  palapeli \
  simple-scan \
  teams \
  tradingview \
 # Special snaps
 sudo snap install --classic -y \
   code \
   deja-dup
```

### Set zsh to default shell

```bash
chsh -s $(which zsh)
```

### Create "pbcopy" & "pbpaste"

```bash
sudo apt install -y -q xclip
echo "alias pbcopy='xclip -selection clipboard'
alias pbpaste='xclip -selection clipboard -o'" >> ~/.zshrc
echo "alias pbcopy='xclip -selection clipboard'
alias pbpaste='xclip -selection clipboard -o'" >> ~/.bashrc

```

### Create ssh keys

```bash
# Create keys
ssh-keygen -f ~/.ssh/<name_of_key>

# Transfer to server
ssh-copy-id -i ~/.ssh/<name_of_key> <user@host>
```

### Enable ssh on host

```bash
sudo apt update
sudo apt install -y -q openssh-server
sudo ufw allow ssh

# TODO sed update
# Enable password login
sudo gedit /etc/ssh/sshd_config
# Update line
# PasswordAuthentication yes

sudo service ssh restart
```

## Install ~~config~~

<!-- TODO standardize across platforms -->
<!-- TODO create install script -->
<!-- TODO Printer https://support.brother.com/g/b/downloadhowto.aspx?c=us&lang=en&prod=mfc9130cw_us&os=128&dlid=dlf006893_000&flang=4&type3=625 -->
```bash
git clone git@github.com:jraviotta/config.git ~/Documents/config
# 
```

## Other software & Configuration

### Python

```bash
# install latest default systems versions
# Python 2.x
# sudo apt install python
sudo apt install -y -q python3
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y -q python3-pip
```

### Google Chrome

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
  sudo dpkg -i google-chrome-stable_current_amd64.deb
```

### NoMachine

See <https://www.nomachine.com/>
Deselect "share the desktop at server startup" from "Server Status">"Status"

```bash
wget https://download.nomachine.com/download/8.0/Linux/nomachine_8.0.168_2_amd64.deb && \
  sudo dpkg -i nomachine_8.0.168_2_amd64.deb
```

### Dropbox

see [install](https://www.dropbox.com/install-linux)

### Zotero

see [install](https://www.zotero.org/support/installation)  
and [plugins](https://www.zotero.org/support/plugins)  

- [Zutilo](https://github.com/wshanks/Zutilo)
- [Zotfile](http://zotfile.com/)

```bash
wget -qO- https://raw.githubusercontent.com/retorquere/zotero-deb/master/install.sh | sudo bash
sudo apt update
sudo apt install zotero
```

### VMware Workstation Player

see <https://linuxize.com/post/how-to-install-vmware-workstation-player-on-ubuntu-20-04/>

```bash
wget --user-agent="Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0" https://www.vmware.com/go/getplayer-linux && \
  chmod +x getplayer-linux && \
  sudo ./getplayer-linux --required --eulas-agreed
```

### Wine

see <https://linuxhint.com/wine_ubuntu_install_configure/>

```bash
sudo apt install -y \
  wine \
  winetricks
```

### Zoom

see <https://support.zoom.us/hc/en-us/articles/204206269-Installing-or-updating-Zoom-on-Linux#h_89c268b4-2a68-4e4c-882f-441e374b87cb>

## Old

### Install Psycopg from source code

See [also](https://www.psycopg.org/docs/install.html)

```bash
export PATH=/usr/lib/postgresql/X.Y/bin/:$PATH
pip install psycopg2
```

### Lando

See <https://docs.lando.dev/getting-started/installation.html>

### OneDrive sync

  [Install](https://github.com/abraunegg/onedrive/blob/master/docs/ubuntu-package-install.md)  
  [Usage](https://github.com/abraunegg/onedrive/blob/master/docs/advanced-usage.md)  
  **Be sure to include trailing slash in config** EG. `sync_dir = "~/OneDrive_PittVax/"

```bash
# install
echo "deb https://download.opensuse.org/repositories/home:/npreining:/debian-ubuntu-onedrive/xUbuntu_20.04/ ./" | sudo tee -a /etc/apt/sources.list
cd ~/Downloads && wget https://download.opensuse.org/repositories/home:/npreining:/debian-ubuntu-onedrive/xUbuntu_20.04/Release.key
sudo apt-key add ./Release.key
sudo apt-get update && sudo apt-get install -y onedrive

# Create OneDrive dirs and onedrive config dirs
declare -a dirs=( ~/OneDrive ~/OneDrive_PittVax ~/OneDrive_SDOH-PACE-UPMC_Data_Center/Data ~/.config/onedrive ~/.config/onedrive_pittvax ~/.config/onedrive_phrl

for val in ${dirs[@]}; do
  if [ ! -e $val ]
    then mkdir $val
  fi
done

# Authenticate the client using the specific configuration file:  
onedrive --confdir="~/.config/onedrive" --synchronize --resync --dry-run
onedrive --confdir="~/.config/onedrive_phrl" --synchronize --resync --dry-run
onedrive --confdir="~/.config/onedrive_pittvax" --synchronize --resync --dry-run


# install & activate services
for SERVICE in onedrive_phrl.service onedrive_pittvax.service onedrive.service jupyter.service
do
if [ ! -e /lib/systemd/system/$SERVICE ]; then 
  sudo cp ~/.bash/services/$SERVICE /lib/systemd/system;
fi
sudo systemctl start $SERVICE # <--- Start now
sudo systemctl enable $SERVICE # <--- Start on boot
systemctl status $SERVICE
done
```

### nbstripout

See [also](https://github.com/kynan/nbstripout)

```bash
# Set up the git filter in your global ~/.gitconfig
nbstripout --install --global
```

#

### VNC

Download and install [vncserver](https://www.realvnc.com/en/connect/download/vnc/)  
Download and install [vncviewer](https://www.realvnc.com/en/connect/download/viewer/)  
Load on startup

```bash
sudo systemctl enable vncserver-x11-serviced.service
sudo systemctl enable vncserver-virtuald.service
```

#### Fix scaling

```bash
sudo apt-get install xvfb xpra x11_server_utils
sudo wget -O /usr/local/bin/run_scaled "https://raw.githubusercontent.com/kaueraal/run_scaled/master/run_scaled"
sudo chmod +x /usr/local/bin/run_scaled
# example
# run_scaled vncviewer

```

#### Install services

See [also](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)

```bash
for SERVICE in <service1.service> <service2.service>
do
if [ ! -e /lib/systemd/system/$SERVICE ]; then 
  sudo cp ~/.bash/services/$SERVICE /lib/systemd/system;
fi
sudo systemctl start $SERVICE # <--- Start now
sudo systemctl enable $SERVICE # <--- Start on boot
systemctl status $SERVICE
done
```

#### Uninstall services

```bash
# find service name
systemctl list-units --type=service | grep onedrive

# Set service name
SERVICE=[myService]

# Execute commands
sudo systemctl stop $SERVICE
sudo systemctl disable $SERVICE
sudo rm /etc/systemd/system/$SERVICE
sudo rm /etc/systemd/system/$SERVICE # and symlinks that might be related
sudo rm /usr/lib/systemd/system/$SERVICE 
sudo rm /usr/lib/systemd/system/$SERVICE # and symlinks that might be related
sudo systemctl daemon-reload
sudo systemctl reset-failed
```
