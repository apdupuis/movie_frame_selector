# load in a movie
# display a single frame at a time 
# export a given frame by hitting 's'
# move between frames with the a, d keys

# todo: mark all the various key commands 

import cv2
import os
import sys
import json # for config file 

import Tkinter, tkFileDialog

# for opening the file dialog
root = Tkinter.Tk()
root.withdraw()

display_scalar = 0.75 #how large is the image we see when editing 
current_frame_index = 0
capture_new_frame = True
total_frames = 0

output_file_prefix = ""
previous_src_file = ""
previous_dst_file = ""

def update_frame(frame_offset):
	global current_frame_index, capture_new_frame, total_frames

	if(total_frames	< 1):
		print("Not enough frames")
		return
	
	current_frame_index	+= frame_offset
	while(current_frame_index < 0):
		current_frame_index	+= total_frames

	current_frame_index	= current_frame_index % total_frames
	capture_new_frame = True
	print("Current frame: "+str(current_frame_index))
	return

def open_movie():
	global previous_src_file, total_frames, capture_new_frame, output_file_prefix, current_frame_index, video_capture
	# prompt for file
	src_file = tkFileDialog.askopenfilename(initialfile=previous_src_file)
	# save the new filename in the config
	with open("movie_frame_selector_config.json", "w") as config_file:
		previous_src_file = src_file
		config_file_data["previous_src_file"] = previous_src_file
		json.dump(config_file_data, config_file)
		config_file.close()
	video_capture = cv2.VideoCapture(src_file)

	# Check if camera opened successfully
	if (video_capture.isOpened()== False):
		print("Error opening video stream or file")
	else:
		total_frames = video_capture.get(7)
		capture_new_frame = True
		current_frame_index = 0
		# prompt for the option of a new filename next time we save
		output_file_prefix = ""

# check if we have a config file - if not, make one
# the config file will contain the last directories used for loading and saving 

if os.path.exists("movie_frame_selector_config.json"):
	with open("movie_frame_selector_config.json") as config_file:
		config_file_data = json.load(config_file)
		previous_src_file = config_file_data["previous_src_file"]
		previous_dst_file = config_file_data["previous_dst_file"]
		config_file.close()
else:
	with open("movie_frame_selector_config.json", "w+") as config_file:
		config_file_data = {}
		config_file_data["previous_src_file"] = previous_src_file
		config_file_data["previous_dst_file"] = previous_dst_file
		json.dump(config_file_data, config_file)
		config_file.close()

# read in video
open_movie()

while(video_capture.isOpened()):
	
	# read in current frame
	# note - we might actually need it to be current_frame_index - 1, if it in face 
	# reads the NEXT frame
	if capture_new_frame:
		video_capture.set(1, current_frame_index)
		ret, frame = video_capture.read()

	if ret == True:
		if capture_new_frame:
			capture_new_frame = False
			cv2.imshow('Frame display', frame)
	else:
		print("Failed to get frame")

	k = cv2.waitKey(33)
	if k==-1:  # normally -1 returned,so don't print it
		continue
	elif k==27:	# Esc key to stop
		# sys.exit()
		break
	elif k==122: # if 'z', go back 100 frames
		update_frame(-100)
	elif k==113: # if 'q', go back 10 frames
		update_frame(-10)
	elif k==97: # if 'a', go to the previous frame
		update_frame(-1)
	elif k==100: # if 'd', to the next frame
		update_frame(1)
	elif k==101: # if 'e', advance 10 frames
		update_frame(10)
	elif k==99: # if 'c', advance 100 frames
		update_frame(100)
	elif k==111: # if 'o', prompt to open a new file
		open_movie()
	elif k==115: # if 's', save the frame
		if output_file_prefix == "":
			output_file_prefix = tkFileDialog.asksaveasfilename(initialfile=previous_dst_file)
		if output_file_prefix != "":
			output_file = output_file_prefix+"_frame_"+str(int(current_frame_index)).zfill(5)+".png"
			print("Saving to "+output_file)
			cv2.imwrite(output_file, frame)
			with open("movie_frame_selector_config.json", "w") as config_file:
				previous_dst_file = output_file_prefix
				config_file_data["previous_dst_file"] = previous_dst_file
				json.dump(config_file_data, config_file)
				config_file.close()

	else:
		print(k)

# When everything done, release the video capture object
video_capture.release()

# Closes all the frames
cv2.destroyAllWindows()