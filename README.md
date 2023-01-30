# computer_vision_learning
## Setup
* install `make` and `poetry`
    * run `make setup` in terminal
    * run `make record` to record video to `./video/` folder ()
    * run `make convert` to convert all videos in `./video/` folder to 3D coordinates in `./data/` folder
* or use `pip install`
    * libraries:
        * opencv-python
        * mediapipe
        * pandas
    * create `./video/` and `./data/` folders to store the outputs
    * run commands in `Makefile` without the prefix `poetry run`
* **raspberrypi** only record video works

RaspberryPi 64bit Lite OS
# install Python:3.7.0
sudo apt update
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
sudo tar zxf Python-3.7.0.tgz
cd Python-3.7.0
sudo ./configure
sudo make -j 4
sudo make altinstall
echo "alias python='/usr/local/bin/python3.7'" >> ~/.bashrc
source ~/.bashrc
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
sudo apt install -y ffmpeg python3-opencv git fswebcam
wget https://files.seeedstudio.com/ml/mediapipe/mediapipe-0.8-cp37-cp37m-linux_aarch64.whl
pip3.7 install mediapipe-0.8-cp37-cp37m-linux_aarch64.whl
pip3.7 install protobuf==3.20.*
(TypeError: Descriptors cannot be created directly)
change URL_PREFIX in `~/.local/lib/python3.7/site-packages/mediapipe/python/solutions/download_utils.py` to 'https://storage.googleapis.com/mediapipe-assets/'



## Numerical Data Augmentation
1. **Uniform Random Generation** : This really naive method consists of creating a new instance based on the min and max of the existing ones, the value of each feature is generated randomly with a uniform probability. (The mins and maxs are calculated from the values of the concerned feature of the concerned class each time)
2. **Normal Random Generation** : Same as Uniform but the probability is now a gaussian curve. Which is of course less naive since generated value fit the initial data distribution.
3. **Adding Noise** : This method is a little bit different since it consists of cloning initial values, but each time adding some noise to it. This methods aims to strengthen the models and prevent overfitting.
