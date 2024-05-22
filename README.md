# 🤖AI_Video_Handler🤖
Проект представляет собой утилиту для обработки видео. 
Она определяет объект на видео из списка {SSD накопитель, Колонка, Лист, Лист с цифрой}.
Изменяет цвет данного объекта на негатив и выводит в отчёт информациюо о времени его появления.


## Сontent
- [Requirement software](#requirement-software)
- [Software installation](#software-installation)
- [Launching](#launching)
  - [Project structure](project-structure)
  - [Example](#example)
- [Developers](#developers)

<a name="requirement-software"></a>

## Requirement software
- ultralytics
- cv2
- csv
- numpy
- torch

<a name="software-installation"></a>

## Software installation

Before you run the *./install_required_software.sh*, make sure that you have pip3 installed or install it with the command
```bash
sudo apt-get install python3-pip -y
```

Then run
```bash
git https://github.com/KirillMaltsev3341/AI_Video_Handler.git
cd AI_Video_Handler
./install_required_software.sh
```

<a name="launching"></a>

## Launching

<a name="project-structure"></a>

### Project structure

Input files are located in ***input*** directory. Output files will be located in ***output*** directory.
***models*** directory contains models for detecting objects (***digits_640.pt***) and digits (***objects_640.pt***).


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

  - [Boitsov Vladislav](#https://github.com/VladislavBoytsovfrom3341Clan)
  - [Luchkin Mark](#https://github.com/markluchkin)
  - [Maltsev Kirill](#https://github.com/KirillMaltsev3341)
  - [Ryabov	Mikhail](#https://github.com/Devilpoper)
  - [Shapovalenko Egor](#https://github.com/lastikp0)