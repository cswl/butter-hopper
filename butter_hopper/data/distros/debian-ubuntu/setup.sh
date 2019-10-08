# Generate Locale
echo 'LANG="en_US.UTF-8' >  /etc/default/locale
locale-gen en_US.UTF-8

dpkg-reconfigure -f non-interactive tzdata

apt update &&  apt  install language-pack-en && apt upgrade

# install your DE 
xserver-xorg-core xinit x11-xserver-utils

`
`

   56  sudo mkdir ubuntu-latest
   57  ls -al
   58  cd ubuntu-latest/
   59  ls -al
   60  clear
   61  ls -al
   62  sudo btrfs subvol create @
   63  sudo btrfs subvol create home


The run setup.sh script.. which sets your stuff generate locales for en_US.UTF-8 
you need to set your own timezoen tho

// debian
ln -s /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
     
    5  apt install -y   locales 
    7  echo 'LANG="en_US.UTF-8' >  /etc/default/locale
    8  locale-gen en_US.UTF-8
    9  vim /etc/locale.gen 
   10  vi /etc/locale.gen 
   11  locale-gen en_US.UTF-8 
   13  apt update && apt upgrade
   14  dpkg-reconfigure -f non-interactive tzdata
   15  clear
   16  ls
   17  sudo apt install gnome
   18   apt install gnome
   19  history

apt install linux-image-amd64 grub-efi-amd64


---------- UIbuntu
   12  apt install mate-desktop

   25  mv unicode.pf2 fonts/
   26  clear
   27  update-grub 
   33  sudo apt install xserver-xorg-core  x11-xserver-utils sddm

apt install vim psmisc eatmydata

