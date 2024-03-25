`indicatortest` exercises a range of indicator functionality on `Debian`, `Ubuntu`, `Fedora`, `openSUSE`, `Manjaro`  and theoretically, any platform which supports the `appindicator` library. Other indicators in this series are:
- `indicatorfortune`
- `indicatorlunar`
- `indicatoronthisday`
- `indicatorppadownloadstatistics`
- `indicatorpunycode`
- `indicatorscriptrunner`
- `indicatorstardate`
- `indicatortide`
- `indicatorvirtualbox`

Installation
------------
<details><summary><b>Debian 11 / 12</b></summary>

1. Install operating system packages:

    ```
    sudo apt-get -y install calendar fortune-mod fortunes gir1.2-ayatanaappindicator3-0.1 gir1.2-gtk-3.0 libcairo2-dev libgirepository1.0-dev pkg-config python3-dev python3-gi python3-gi-cairo python3-notify2 python3-venv wmctrl
    ```

2. Install the `GNOME Shell` `AppIndicator and KStatusNotifierItem Support` [extension](https://extensions.gnome.org/extension/615/appindicator-support).

3. Create a `Python` virtual environment, activate and install the indicator package:
    ```
    python3 -m venv $HOME/.local/venv_indicatortest && \
    . $HOME/.local/venv_indicatortest/bin/activate && \
    python3 -m pip install --upgrade pip indicatortest && \
    deactivate
    ```
4. Copy icon, run script and desktop file to `$HOME/.local`:
    ```
    mkdir -p $HOME/.local/share/icons/hicolor/scalable/apps && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/icons/*.svg $HOME/.local/share/icons/hicolor/scalable/apps && \
    mkdir -p $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.sh $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.py.desktop $HOME/.local/share/applications
    ```

</details>

<details><summary><b>Fedora 38 / 39</b></summary>

1. Install operating system packages:

    ```
    sudo dnf -y install cairo-devel cairo-gobject-devel calendar fortune-mod gnome-extensions-app gnome-shell-extension-appindicator gobject-introspection-devel libappindicator-gtk3 pkgconf-pkg-config python3-devel python3-gobject python3-notify2 wmctrl
    ```

2. Create a `Python` virtual environment, activate and install the indicator package:
    ```
    python3 -m venv $HOME/.local/venv_indicatortest && \
    . $HOME/.local/venv_indicatortest/bin/activate && \
    python3 -m pip install --upgrade pip indicatortest && \
    deactivate
    ```
3. Copy icon, run script and desktop file to `$HOME/.local`:
    ```
    mkdir -p $HOME/.local/share/icons/hicolor/scalable/apps && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/icons/*.svg $HOME/.local/share/icons/hicolor/scalable/apps && \
    mkdir -p $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.sh $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.py.desktop $HOME/.local/share/applications
    ```

</details>

<details><summary><b>Manjaro 22.1</b></summary>

1. Install operating system packages:

    ```
    sudo pacman -S --noconfirm cairo fortune-mod gobject-introspection gtk3 libayatana-appindicator pkgconf wmctrl
    ```

2. Create a `Python` virtual environment, activate and install the indicator package:
    ```
    python3 -m venv $HOME/.local/venv_indicatortest && \
    . $HOME/.local/venv_indicatortest/bin/activate && \
    python3 -m pip install --upgrade pip indicatortest && \
    deactivate
    ```
3. Copy icon, run script and desktop file to `$HOME/.local`:
    ```
    mkdir -p $HOME/.local/share/icons/hicolor/scalable/apps && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/icons/*.svg $HOME/.local/share/icons/hicolor/scalable/apps && \
    mkdir -p $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.sh $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.py.desktop $HOME/.local/share/applications
    ```

</details>

<details><summary><b>openSUSE Tumbleweed</b></summary>

1. Install operating system packages:

    ```
    sudo zypper install -y cairo-devel fortune gcc gobject-introspection-devel pkg-config python3-devel typelib-1_0-AyatanaAppIndicator3-0_1
    ```

2. Install the `GNOME Shell` `AppIndicator and KStatusNotifierItem Support` [extension](https://extensions.gnome.org/extension/615/appindicator-support).

3. Create a `Python` virtual environment, activate and install the indicator package:
    ```
    python3 -m venv $HOME/.local/venv_indicatortest && \
    . $HOME/.local/venv_indicatortest/bin/activate && \
    python3 -m pip install --upgrade pip indicatortest && \
    deactivate
    ```
4. Copy icon, run script and desktop file to `$HOME/.local`:
    ```
    mkdir -p $HOME/.local/share/icons/hicolor/scalable/apps && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/icons/*.svg $HOME/.local/share/icons/hicolor/scalable/apps && \
    mkdir -p $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.sh $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.py.desktop $HOME/.local/share/applications
    ```

</details>

<details><summary><b>Ubuntu 20.04</b></summary>

1. Install operating system packages:

    ```
    sudo apt-get -y install fortune-mod fortunes gir1.2-ayatanaappindicator3-0.1 gir1.2-gtk-3.0 gnome-shell-extension-appindicator libcairo2-dev libgirepository1.0-dev pkg-config python3-dev python3-gi python3-gi-cairo python3-notify2 python3-venv wmctrl
    ```

2. Create a `Python` virtual environment, activate and install the indicator package:
    ```
    python3 -m venv $HOME/.local/venv_indicatortest && \
    . $HOME/.local/venv_indicatortest/bin/activate && \
    python3 -m pip install --upgrade pip indicatortest && \
    deactivate
    ```
3. Copy icon, run script and desktop file to `$HOME/.local`:
    ```
    mkdir -p $HOME/.local/share/icons/hicolor/scalable/apps && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/icons/*.svg $HOME/.local/share/icons/hicolor/scalable/apps && \
    mkdir -p $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.sh $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.py.desktop $HOME/.local/share/applications
    ```

</details>

<details><summary><b>Ubuntu 22.04</b></summary>

1. Install operating system packages:

    ```
    sudo apt-get -y install calendar fortune-mod fortunes gir1.2-ayatanaappindicator3-0.1 gir1.2-gtk-3.0 gnome-shell-extension-appindicator libcairo2-dev libgirepository1.0-dev pkg-config python3-dev python3-gi python3-gi-cairo python3-notify2 python3-venv wmctrl
    ```

2. Create a `Python` virtual environment, activate and install the indicator package:
    ```
    python3 -m venv $HOME/.local/venv_indicatortest && \
    . $HOME/.local/venv_indicatortest/bin/activate && \
    python3 -m pip install --upgrade pip indicatortest && \
    deactivate
    ```
3. Copy icon, run script and desktop file to `$HOME/.local`:
    ```
    mkdir -p $HOME/.local/share/icons/hicolor/scalable/apps && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/icons/*.svg $HOME/.local/share/icons/hicolor/scalable/apps && \
    mkdir -p $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.sh $HOME/.local/bin && \
    cp $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest/platform/linux/indicatortest.py.desktop $HOME/.local/share/applications
    ```

</details>

Usage
-----
To run `indicatortest`, press the `Super`/`Windows` key to open the `Show Applications` overlay (or similar), type `test` into the search bar and the icon should be present for you to click.  If the icon does not appear, or appears as generic, you may have to log out and log back in (or restart).

Distributions Tested
--------------------
Distributions/versions with full functionality:
- `Debian 11 / 12 GNOME on Xorg`
- `Fedora 38 / 39 GNOME on Xorg`
- `Kubuntu 20.04 / 22.04`
- `Ubuntu 20.04`
- `Ubuntu 22.04 on Xorg`
- `Ubuntu Budgie 22.04`
- `Ubuntu Unity 20.04 / 22.04`
- `Xubuntu 20.04 / 22.04`

Distributions/versions with limited functionality:
- `Debian 11 / 12 GNOME` No clipboard; no `wmctrl`.
- `Fedora 38 / 39 GNOME` No clipboard; no `wmctrl`.
- `Kubuntu 20.04 / 22.04` No mouse wheel scroll; tooltip in lieu of label.
- `Linux Mint 21 Cinnamon` Tooltip in lieu of label.
- `Lubuntu 20.04 / 22.04` No label; tooltip is not dynamic; icon is not dynamic.
- `Manjaro 22.1 GNOME` No `calendar`.
- `openSUSE Tumbleweed` No clipboard; no `wmctrl`; no `calendar`.
- `openSUSE Tumbleweed GNOME on Xorg` No `calendar`.
- `Ubuntu 22.04` No clipboard; no `wmctrl`.
- `Ubuntu Budgie 20.04` No mouse middle click.
- `Ubuntu MATE 20.04` Dynamic icon is truncated, but fine whilst being clicked.
- `Ubuntu MATE 22.04` Dynamic icon for NEW MOON is truncated.
- `Xubuntu 20.04 / 22.04` No mouse wheel scroll; tooltip in lieu of label.

Removal
-------
<details><summary><b>Debian 11 / 12</b></summary>

1. Remove operating system packages:

    ```
    sudo apt-get -y remove calendar fortune-mod fortunes gir1.2-ayatanaappindicator3-0.1 gir1.2-gtk-3.0 libcairo2-dev libgirepository1.0-dev pkg-config python3-dev python3-gi python3-gi-cairo python3-notify2 python3-venv wmctrl
    ```

2. Remove `Python` virtual environment and files from `$HOME/.local`:
    ```
    rm -r $HOME/.local/venv_indicatortest && \
    rm $HOME/.local/share/icons/hicolor/scalable/apps/indicatortest*.svg && \
    rm $HOME/.local/bin/indicatortest.sh && \
    rm $HOME/.local/share/applications/indicatortest.py.desktop
    ```

</details>

<details><summary><b>Fedora 38 / 39</b></summary>

1. Remove operating system packages:

    ```
    sudo dnf -y remove cairo-devel cairo-gobject-devel calendar fortune-mod gnome-extensions-app gnome-shell-extension-appindicator gobject-introspection-devel libappindicator-gtk3 pkgconf-pkg-config python3-devel python3-gobject python3-notify2 wmctrl
    ```

2. Remove `Python` virtual environment and files from `$HOME/.local`:
    ```
    rm -r $HOME/.local/venv_indicatortest && \
    rm $HOME/.local/share/icons/hicolor/scalable/apps/indicatortest*.svg && \
    rm $HOME/.local/bin/indicatortest.sh && \
    rm $HOME/.local/share/applications/indicatortest.py.desktop
    ```

</details>

<details><summary><b>Manjaro 22.1</b></summary>

1. Remove operating system packages:

    ```
    sudo pacman -R --noconfirm cairo fortune-mod gobject-introspection gtk3 libayatana-appindicator pkgconf wmctrl
    ```

2. Remove `Python` virtual environment and files from `$HOME/.local`:
    ```
    rm -r $HOME/.local/venv_indicatortest && \
    rm $HOME/.local/share/icons/hicolor/scalable/apps/indicatortest*.svg && \
    rm $HOME/.local/bin/indicatortest.sh && \
    rm $HOME/.local/share/applications/indicatortest.py.desktop
    ```

</details>

<details><summary><b>openSUSE Tumbleweed</b></summary>

1. Remove operating system packages:

    ```
    sudo zypper remove -y cairo-devel fortune gcc gobject-introspection-devel pkg-config python3-devel typelib-1_0-AyatanaAppIndicator3-0_1
    ```

2. Remove `Python` virtual environment and files from `$HOME/.local`:
    ```
    rm -r $HOME/.local/venv_indicatortest && \
    rm $HOME/.local/share/icons/hicolor/scalable/apps/indicatortest*.svg && \
    rm $HOME/.local/bin/indicatortest.sh && \
    rm $HOME/.local/share/applications/indicatortest.py.desktop
    ```

</details>

<details><summary><b>Ubuntu 20.04</b></summary>

1. Remove operating system packages:

    ```
    sudo apt-get -y remove fortune-mod fortunes gir1.2-ayatanaappindicator3-0.1 gir1.2-gtk-3.0 gnome-shell-extension-appindicator libcairo2-dev libgirepository1.0-dev pkg-config python3-dev python3-gi python3-gi-cairo python3-notify2 python3-venv wmctrl
    ```

2. Remove `Python` virtual environment and files from `$HOME/.local`:
    ```
    rm -r $HOME/.local/venv_indicatortest && \
    rm $HOME/.local/share/icons/hicolor/scalable/apps/indicatortest*.svg && \
    rm $HOME/.local/bin/indicatortest.sh && \
    rm $HOME/.local/share/applications/indicatortest.py.desktop
    ```

</details>

<details><summary><b>Ubuntu 22.04</b></summary>

1. Remove operating system packages:

    ```
    sudo apt-get -y remove calendar fortune-mod fortunes gir1.2-ayatanaappindicator3-0.1 gir1.2-gtk-3.0 gnome-shell-extension-appindicator libcairo2-dev libgirepository1.0-dev pkg-config python3-dev python3-gi python3-gi-cairo python3-notify2 python3-venv wmctrl
    ```

2. Remove `Python` virtual environment and files from `$HOME/.local`:
    ```
    rm -r $HOME/.local/venv_indicatortest && \
    rm $HOME/.local/share/icons/hicolor/scalable/apps/indicatortest*.svg && \
    rm $HOME/.local/bin/indicatortest.sh && \
    rm $HOME/.local/share/applications/indicatortest.py.desktop
    ```

</details>

License
-------
This project in its entirety is licensed under the terms of the GNU General Public License v3.0 license.

Copyright 2016-2024 Bernard Giannetti.
