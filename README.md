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
    * `sudo apt update`
    * `sudo apt upgrade`
    * `sudo apt install ffmpeg python3-opencv python3-pip git fswebcam`
    * `git clone https://github.com/huangruoqi/computer_vision_learning.git`
    * `cd computer_vision_learning`
    * *mediapipe*: https://github.com/superuser789/MediaPipe-on-RaspberryPi#readme


## Numerical Data Augmentation
1. **Uniform Random Generation** : This really naive method consists of creating a new instance based on the min and max of the existing ones, the value of each feature is generated randomly with a uniform probability. (The mins and maxs are calculated from the values of the concerned feature of the concerned class each time)
2. **Normal Random Generation** : Same as Uniform but the probability is now a gaussian curve. Which is of course less naive since generated value fit the initial data distribution.
3. **Adding Noise** : This method is a little bit different since it consists of cloning initial values, but each time adding some noise to it. This methods aims to strengthen the models and prevent overfitting.
