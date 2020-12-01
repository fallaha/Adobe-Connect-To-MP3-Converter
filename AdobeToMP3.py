# (c) Ali Fallah
# 1 Dec 2020

import findstreamAdded
import pathlib
import os
import datetime
import sys, getopt, time, subprocess, shlex
import tempfile
import zipfile

if len(sys.argv) != 2:
    print("USAGE: python AdobeToMP3.py D:\\path\\to\\directory\\example.zip")
    exit(0)
if not os.path.isfile(sys.argv[1]) or not sys.argv[1].endswith(".zip"):
    print("ERROR: %s is not a correct file"%sys.argv[1])
    exit(0)

zipfilename = os.path.basename(sys.argv[1]).split(".")[0]
# Extract Zip file in Temp directory
temp_dir = tempfile.TemporaryDirectory()
lesson_path = temp_dir.name
with zipfile.ZipFile(sys.argv[1],'r') as zip_ref:
        zip_ref.extractall(lesson_path)

zipfilename = os.path.basename(sys.argv[1]).split(".")[0]
# Extract Zip file in Temp directory
temp_dir = tempfile.TemporaryDirectory()
lesson_path = temp_dir.name
with zipfile.ZipFile(sys.argv[1],'r') as zip_ref:
        zip_ref.extractall(lesson_path)

mainstream_file_path = os.path.join(lesson_path,"mainstream.xml")

flv_objs = findstreamAdded.findStreamAddedInYourDestination(mainstream_file_path,"findStreamAddedInYourDestination")
total_time = int(findstreamAdded.findStreamAddedInYourDestination(mainstream_file_path,"totalTime"))
command = ["-itsoffset %i -i %s.flv" %(int(item["startTime"])//1000,os.path.join(lesson_path,item['name'][1:])) for item in flv_objs]

output_name = zipfilename+".mp3"

ffmpeg_cmd = """ffmpeg -y \
 {0}\
 -filter_complex "amix=inputs={1}:duration=longest [aout]" -map [aout] -acodec mp3 \
 -async 1 -t {2} {3}""".format(" ".join(command),str(len(flv_objs)),total_time//1000,output_name)

if os.name == "nt": ffmpeg_cmd = ffmpeg_cmd.replace('\\','\\\\')
args = shlex.split(ffmpeg_cmd)
p = subprocess.Popen(args).wait()

if not p:
    print("Convert Successfully Finished")
else:
    print(ffmpeg_cmd)
    print("an error occured in conversion")
