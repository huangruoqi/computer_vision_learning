# computer_vision_learning
Pose Estimation Model: https://google.github.io/mediapipe/solutions/pose.html
## TODO
- Mediapipe hand tracking test
- Data collection
  - 爬虫
  - Simple GUI for labeling behaviors in video range
- Tensorflow 
- Behavior classification
- Performance


## Setup
* **Windows**
  * Enable long path for windows in powershell
    * https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=powershell
    ```
    New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
    ```
  * run in powershell to install `poetry`
    ```
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python
    ```
  * download `make` utils 
    * https://sourceforge.net/projects/gnuwin32/files/make/3.81/make-3.81.exe/download?use_mirror=gigenet&download=
  * run `make setup` in terminal
  * run `make record` to record video to `./video/` folder 
    * change MAX_TIME, FPS for record time or frame per second in `./code/video_to_3d_positions.py`
  * run `make convert` to convert all videos in `./video/` folder to 3D coordinates in `./data/` folder
* **MacOS** *(not tested)*
   * use `pip install`
       * libraries:
           * opencv-python
           * mediapipe
           * pandas
           * pygame
       * create `./video/` and `./data/` folders to store the outputs
       * run commands in `Makefile` without the prefix `poetry run`
* **RaspberryPi 64bit Lite OS** 
   * run the following commands
   ```
      sudo apt install git
      git clone https://github.com/huangruoqi/computer_vision_learning.git
      cd computer_vision_learning
      mv Makefile4raspi Makefile
      make setup
   ```
   or install dependencies manually
   ```
      sudo apt update
      # build dependencies
      sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev \
      libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev \
      libexpat1-dev liblzma-dev zlib1g-dev libffi-dev

      # Python:3.7.0
      wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
      sudo tar zxf Python-3.7.0.tgz
      cd Python-3.7.0
      sudo ./configure
      sudo make -j 4
      sudo make altinstall
      echo "alias python='/usr/local/bin/python3.7'" >> ~/.bashrc
      source ~/.bashrc

      # pip with Python3.7
      wget https://bootstrap.pypa.io/get-pip.py
      python get-pip.py

      # opencv, ffmpeg, mediapipe
      sudo apt install -y ffmpeg python3-opencv fswebcam
      wget https://files.seeedstudio.com/ml/mediapipe/mediapipe-0.8-cp37-cp37m-linux_aarch64.whl
      pip3.7 install mediapipe-0.8-cp37-cp37m-linux_aarch64.whl

      # [fix] TypeError: Descriptors cannot be created directly
      pip3.7 install protobuf==3.20.*

      # other libs
      pip3.7 install pandas pygame
   ``` 
   and change URL_PREFIX in `~/.local/lib/python3.7/site-packages/mediapipe/python/solutions/download_utils.py` to 'https://storage.googleapis.com/mediapipe-assets/'
