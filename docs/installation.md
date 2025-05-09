# Installation

Gourmand is currently available in the form of Flatpak, AppImage, and Python wheel.  
For wheels and Flatpak installations, you will need an internet connection.  
The AppImage can be copied from one computer to another.  

## AppImage

The AppImage is available from the [release page](https://github.com/GourmandRecipeManager/gourmand/releases/).
Download it and mark it as executable:

```sh
chmod +x ./Gourmand-1.0.0-x86_64.AppImage
```

It can then be executed by double-clicking on it or launching it from a terminal:

```sh
./Gourmand-1.0.0-x86_64.AppImage
```

## Flatpak

The Flatpak contains the full environment, but depends on other flatpak
packages, which will be installed automatically.

Install Flatpak if it's not on your system already:

```sh
sudo apt-get install flatpak
```

As Gourmand is still under active development, the flatpak is not available from
Flathub, and instead must be [downloaded and installed manually](https://github.com/GourmandRecipeManager/gourmand/releases/).

In a terminal, execute the following:

```sh
flatpak remote-add --if-not-exists --user flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install gourmand-1.0.0.flatpak
```

You will be prompted with a message regarding the runtime:

```sh
Required runtime for io.github.GourmandRecipeManager.Gourmand/x86_64/master (runtime/org.gnome.Platform/x86_64/3.40) found in remote flathub)
Do you want to install it? [Y/n]
```

Select `y`, and a list of dependencies will be displayed. Say `y` to install
them all.

At the end, you will be greeted with an `Installation complete.` message.

You can now launch the Flatpak either from your application menu, or from the
command line so:

```sh
flatpak run io.github.GourmandRecipeManager.Gourmand
```

It can be uninstalled so:

```sh
flatpak remove io.github.GourmandRecipeManager.Gourmand
```

## Python Wheel

You can get the wheel from PyPI. Some dependencies must be installed manually and/or
require more work, especially for *pygobject* when using virtual environments.

The following section is outdated and requires an overhaul for recent Ubuntu versions.
Feel free to submit a corresponding PR if you tracked down how to install everything
into a dedicated virtual environment.

### Ubuntu 20.04, Linux Mint 20

Install the following packages from `apt`:

```sh
sudo apt-get update

sudo apt-get install --no-install-recommends python3-gi python3-gi-cairo gir1.2-gtk-3.0 libgirepository1.0-dev libcairo2-dev enchant python3-bs4 python3-ebooklib python3-keyring python3-lxml python3-pil python3-cairo python3-enchant python3-gi python3-gst-1.0 python3-gtkspellcheck python3-requests python3-reportlab python3-selenium python3-setuptools python3-sqlalchemy python3-pip python3-toml gir1.2-poppler-0.18
```

Finally, install Gourmand:

```sh
sudo pip3 install gourmand-1.0.0-py3-none-any.whl
```

You can now launch Gourmand from a terminal:

```sh
$ gourmand
First time? Setting you up with yummy recipes.
```

## Windows 10

Running Gourmand on Windows is still experimental at this stage: the application can run fine, and even exports to PDF. However, there are a couple of issues, and the installation is cumbersome.

Download and install [MSYS2](https://www.msys2.org/)
Within the MSYS2 terminal, synchronize your software sources:

```sh
pacman -Syu
```

Then install parts of the dependencies:

```sh
pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3-gobject mingw-w64-x86_64-python-pillow mingw-w64-x86_64-python-sqlalchemy mingw-w64-x86_64-gstreamer mingw-w64-x86_64-poppler mingw-w64-x86_64-python-reportlab
```

Install the package from PyPI:

```sh
python3 -m pip install gourmand
```

Then launch it:

```sh
python3 -m gourmand
```
