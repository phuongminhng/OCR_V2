import csv
import cv2
from os import listdir
from os.path import isfile, join
import easyocr
from tool.config import Config
import argparse
from run import Pipeline
import matplotlib.pyplot as plt
import numpy as np
import time
import pytesseract
import fastwer



config = './tool/config/configs.yaml'

config = Config(config)

parser = argparse.ArgumentParser("vnOcrToolboxWithVietOcr")
parser.add_argument("--input")
parser.add_argument("--output", default="./results")
parser.add_argument("--debug", action="store_true")
parser.add_argument("--do_retrieve", action="store_true")
parser.add_argument("--find_best_rotation", action="store_true")
args = parser.parse_args()
img = cv2.imread("/home/tuanna/Desktop/OCR/data/images/GPKD_gcndkdoanhnghiepcongtycophan_3.jpg")
pipeline = Pipeline(args, config)
pipeline.getBox(img)

