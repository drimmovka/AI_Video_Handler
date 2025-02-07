# 🤖AI_Video_Handler🤖
The project is a video processing utility.
It identifies the object in the video from the list {SSD drive, Column, Sheet, Sheet with a number}, 
changes the color of this object to a negative and displays information about the time of its appearance in the report.


## Сontent
- [Requirement software](#requirement-software)
- [Software installation](#software-installation)
  - [WSL](#wsl)
  - [Scripts](#scripts)
- [Launching](#launch)
  - [Project structure](project-structure)
  - [Example](#example)
- [Developers](#developers)

<a name="requirement-software"></a>

## Requirement software
- ultralytics
- opencv-python
- torchvision
- numpy

<a name="software-installation"></a>

## Software installation

<a name="wsl"></a>

### WSL

The utility is designed to run on 🐧unix-like🐧 systems. If you have Windows, then you should install WSL (Windows Subsystem for Linux).  
Tutorial:

  1. Windows features

  ![Image alt](https://github.com/KirillMaltsev3341/Images/raw/main/Windows_features.png)
  
  2. Turn on VMP (Virtual Machine Platform)

  ![Image alt](https://github.com/KirillMaltsev3341/Images/raw/main/Turn_on_VMP.png)
  
  3. Make sure that you have enabled virtualization in your BIOS

  4. Get Ubuntu WSL from Microsoft store

  ![Image alt](https://github.com/KirillMaltsev3341/Images/raw/main/WSL_Microsoft_store.png)


<a name="scripts"></a>

### Scripts

Before running the installation script, make sure that you have **git** installed, or install it using the command
```bash
sudo apt-get update
sudo apt-get install git -y
```

Installation script
```bash
sudo -s
git clone https://github.com/KirillMaltsev3341/AI_Video_Handler.git
cd AI_Video_Handler
./install_required_software.sh
```

<a name="launching"></a>

## Launching

<a name="project-structure"></a>

### Project structure

Input files are located in ***input*** directory. Output files will be located in ***output*** directory.
***models*** directory contains models for detecting objects (*objects_640.pt*) and digits (*digits_640.pt*).


<a name="example"></a>

### Example

Initially, a file *Видео для анализа.mov* is already stored in the ***input*** directory (you can put your own file in the ***input*** directory for processing).

To check if the program is working:
```bash
./run.sh --input "Видео для анализа.mov"
```

To find out more information about the launch flags:
```bash
./run.sh --help
```

<a name="developers"></a>

### Developers

  - [Boitsov Vladislav](https://github.com/VBStudi0s)
  - [Luchkin Mark](https://github.com/markluchkin)
  - [Maltsev Kirill](https://github.com/KirillMaltsev3341)
  - [Ryabov	Mikhail](https://github.com/Devilpoper)
  - [Shapovalenko Egor](https://github.com/lastikp0)
