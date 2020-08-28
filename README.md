# Hand Signs Recognition

## Table Of Contents

 1. [Introduction](#introduction)

 2. [Build Status](#build-status)

 3. [Requirement](#requirement)

 4. [Installation](#installation)

 5. [Usage](#usage)

 6. [Contribute](#contribute)

## Introduction

Hand Signs Recognition contains a tool to captures data from the machine's camera and model trained by the data. The model can guesses the shape of hand with more than 92% accuracy. 

![Alt Text](Hnet-image.gif)

## Build Status

[![Build Status](https://travis-ci.com/travis-ci/travis-web.svg?branch=master)](https://travis-ci.com/travis-ci/travis-web)

## Requirement

This project requires some python libraries which can be installed via pip3

1. Numpy

2. Pillow

3. TensorFlow

4. OpenCV

## Installation

```
pip3 install numpy
```

```
pip3 install pillow
```

```
pip3 install tensorflow
```

```
pip3 install opencv-python
```

## Usage

1. Clone the folder from GitHub repository

2. cd hand-signs-recognition

3. Take training data and testing data

    - Add categories which you want to train the model in image_taking.py (there are 5 examples in the file)

    - You can change the argument for each category *TakeImage('data/training/',<name_of_category>,size_of_image,number_of_image,duration_between_image)*

    - *python3 image_taking.py*

    - When the camera is on, the program starts take image. You can press 'p' key to pause, or 'c' key to continue taking images. The program will stop when it exceed the number of images

4. Train the model with the taken data

5. Run the demonstration

## Contribute  

1. Fork it

2. Create your feature branch

3. Commit your changes

4. Push to the branch

5. Create a new Pull Request
