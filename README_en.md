# Houdini Icon Browser

This script lists the icons that are included by default in Houdini and allows you to search, get names, edit, and export them.

![HoudiniIconBrowser](https://user-images.githubusercontent.com/50489494/208280012-6bde2aa1-8e6d-42c7-83f9-a198c98a5129.png)

## Install

Download the ZIP file from **Code > Download ZIP**.

Copy the `python_panels` and `scripts` folders from the extracted folder to the Houdini folder in your Documents or where the environment variable `HOUDINI_PATH` passes.

![DownloadFile](https://user-images.githubusercontent.com/50489494/208280543-060010e5-b6c5-45c0-8b3d-1367da2d1cf9.png)

## How to start the script

Start Houdini, right-click on the panel tab, and select Icon Browser from the panel list.

![IconBrowserRun](https://user-images.githubusercontent.com/50489494/208281466-30245413-5256-490b-aa19-11bc38b7c6b8.gif)

## Features

### Double click

![IconBrowserCopyName](https://user-images.githubusercontent.com/50489494/208280386-4b2c8819-86e5-4a6e-a547-c044d34a2c2e.png)

Copy the name of the icon to the clipboard.<br>
Paste the copied icon name into the icon setting field of the HDA or shelf tool to set the icon.

### Context menu

![IconBrowserContextMenu](https://user-images.githubusercontent.com/50489494/208280156-e54a67a7-c492-4327-b403-792b7381b7d9.png)

- **Copy Name**<br>
    Same as double-clicking, copy the name of the icon to the clipboard.
- **Open Icon File**<br>
    Open the icon file with the software that is tied to the svg file editing.
- **Save Icon File**<br>
    Copy the icon file to another folder.<br>
    When executed, a dialog box will open to select a destination folder.

### Filtering

![IconBrowserFilter](https://user-images.githubusercontent.com/50489494/208280215-09973416-51bd-457e-bf08-96db5c05ce28.png)

You can filter by category using the pull-down menu.
By entering text in the search bar, only icons with that text in the icon name will be displayed.

### Icon size adjustment

![IconBrowserIconSize](https://user-images.githubusercontent.com/50489494/208280288-9aed45fa-5bdf-424d-86f3-3276558e1236.png)

The size of the icon can be changed by changing the slider in the lower right corner, the plus and minus buttons, and the numeric input box.<br>
The default is 64px and can be changed from 16px to 64px.

### Change view mode

<img src="https://user-images.githubusercontent.com/50489494/208280329-c41863f8-8c6c-4d3e-8e3d-913dc0cabbfa.png" width=49.5%> <img src="https://user-images.githubusercontent.com/50489494/208280334-9bbde091-b7c1-41c1-aadb-49496f75563d.png" width=49.5%>
The buttons in the lower right corner allow you to change between list mode and icon mode.
