# computer_vision_learning

Pose Estimation Model: https://google.github.io/mediapipe/solutions/pose.html

*autoencoder-decoder to do binary classification for stable and non-stable event.*

*segment-anything*
## TODO
- GUI
  - [ ] Add menu helper
  - [ ] Add current label indicator
  - [ ] Add Auto-Refresh
  - [ ] Add playback speed controls


## Usage
* `make test` to test different configurations specify in `src/test.py`
* `make record` to record video to `video/` folder 
  * change MAX_TIME, FPS for record time or frame per second in `src/convert.py`
* `make label` to show all videos in `video/` folder (max=10) with GUI, click 'label' then 'convert' to label each video.
  * something like this
  * <img width="500" alt="Screen Shot 2023-03-04 at 2 20 56 PM" src="https://user-images.githubusercontent.com/44049919/222931197-10e69854-2bf4-4a1f-be65-d483c9677016.png">

* `make model <file_name_in_nn_folder>`
  * `make model LSTM` to run `LSTM.py` and save model to `model/` 
  * specify `<name>.mp4.csv` files in `LSTM.py` to train
* `make predict` to test model
  * specify MODEL_NAME to load in `src/predict.py`
  * might need to retrain model on different machine to get the working `keras_metadata.pb` file
  
## Visitor Count
![Visitor Count](https://profile-counter.glitch.me/huangruoqi/count.svg)


## Setup
* **Windows** *(recommended)*
  <!-- * Enable long path for windows in powershell
    * https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=powershell
    ```
    New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
    ```
  * run in powershell to install `poetry`
    ```
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python
    ``` -->
  * use `pip install`
      * libraries:
          * opencv-python
          * mediapipe
          * pandas
          * pygame
          * and other modules defined in pyproject.toml
  * download `make` utils 
    * https://sourceforge.net/projects/gnuwin32/files/make/3.81/make-3.81.exe/download?use_mirror=gigenet&download=
  * run `make setup` in terminal

* **MacOS** (intel chip only)
   * use `pip install`
       * libraries:
           * opencv-python
           * mediapipe
           * pandas
           * pygame
           * and other modules defined in pyproject.toml
       * create `video/` and `data/` folders to store the outputs
       * run commands in `Makefile`

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
