# load in a directory containing images
# display a single frame at a time 
# export a given frame by hitting 's'
# move between frames with the a, d keys

# todo: mark all the various key commands 

import cv2
import os
import sys
import imghdr # for checking if file is a valid image
from shutil import copyfile
import json # for config file 

import Tkinter, tkFileDialog

# for opening the file dialog
root = Tkinter.Tk()
root.withdraw()



display_scalar = 0.75 #how large is the image we see when editing 
current_image_index = 0
load_new_image = True
total_images = 0

output_directory = ""

def update_frame(frame_offset):
	global current_image_index, load_new_image, total_images

	if(total_images	< 1):
		print("Not enough images")
		return
	
	current_image_index	+= frame_offset
	while(current_image_index < 0):
		current_image_index	+= total_images

	current_image_index	= current_image_index % total_images
	load_new_image = True
	print("Current frame: "+str(current_image_index))
	return

# check if we have a config file - if not, make one
# the config file will contain the last directories used for loading and saving 

if os.path.exists("image_sequence_frame_selector_config.json"):
	with open("image_sequence_frame_selector_config.json") as config_file:
		config_file_data = json.load(config_file)
		previous_src_directory = config_file_data["previous_src_directory"]
		previous_dst_directory = config_file_data["previous_dst_directory"]
		config_file.close()
else:
	with open("image_sequence_frame_selector_config.json", "w+") as config_file:
		config_file_data = {}
		previous_src_directory = ""
		previous_dst_directory = ""
		config_file_data["previous_src_directory"] = previous_src_directory
		config_file_data["previous_dst_directory"] = previous_dst_directory
		json.dump(config_file_data, config_file)
		config_file.close()


src_directory = tkFileDialog.askdirectory(initialdir=previous_src_directory)

# save source directory in config file 
with open("image_sequence_frame_selector_config.json", "w") as config_file:
	previous_src_directory = src_directory
	config_file_data["previous_src_directory"] = previous_src_directory
	json.dump(config_file_data, config_file)
	config_file.close()

# make a list of files in our directories 
file_list = []
for root, dirnames, filenames in os.walk(src_directory):
    for filename in filenames:
    	if imghdr.what(os.path.join(root, filename)) is not None:
        	file_list.append((os.path.join(root, filename), filename))
        	print("Appending "+filename)
        	total_images += 1
        else:
        	print(filename + " not recognized as an image")

while(1):
	
	# read in current frame
	if load_new_image:
		file_path, file_name = file_list[current_image_index]
		frame = cv2.imread(file_path)

	if frame is not None:
		load_new_image = False
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
	elif k==115: # if 's', save the frame
		if output_directory == "":
			output_directory = tkFileDialog.askdirectory(initialdir=previous_dst_directory)
		if output_directory != "":
			output_file = os.path.join(output_directory, file_name)
			print("Copying to "+output_file)
			copyfile(file_path, output_file)
			# save destination directory in config file 
			with open("image_sequence_frame_selector_config.json", "w") as config_file:
				previous_dst_directory = output_directory
				config_file_data["previous_dst_directory"] = previous_dst_directory
				json.dump(config_file_data, config_file)
				config_file.close()
	else:
		print(k)

# Closes all the frames
cv2.destroyAllWindows()