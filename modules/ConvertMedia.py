import subprocess as sp
import os


def executeConversion(sourceName, outputName, directory, destination, post_conversion_destination):
    sp.run("HandBrakeCLI -f av_mp4 -e x264 -q 20 -B 160 -i "+directory+sourceName+" -o "+destination+outputName+".mp4", shell=True)
    outputName = outputName+".mp4"
    os.rename(destination+outputName, post_conversion_destination+outputName)
    os.remove(directory+sourceName)