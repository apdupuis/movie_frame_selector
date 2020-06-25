# load in a movie
# display a single frame at a time 
# export a given frame by hitting 's'
# move between frames with the a, d keys

# todo: mark all the various key commands 

import cv2
import os
import sys
# from shutil import move

import Tkinter, tkFileDialog

# for opening the file dialog
root = Tkinter.Tk()
root.withdraw()

src_file = tkFileDialog.askopenfilename()

display_scalar = 0.75 #how large is the image we see when editing 
current_frame_index = 0
capture_new_frame = True
total_frames = 0
output_file_prefix = ""

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

# read in video
video_capture = cv2.VideoCapture(src_file)

# Check if camera opened successfully
if (video_capture.isOpened()== False):
	print("Error opening video stream or file")

while(video_capture.isOpened()):
	total_frames = video_capture.get(7)

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
		if output_file_prefix == "":
			output_file_prefix = tkFileDialog.asksaveasfilename()
		if output_file_prefix != "":
			output_file = output_file_prefix+"_frame_"+str(int(current_frame_index)).zfill(5)+".png"
			print("Saving to "+output_file)
			cv2.imwrite(output_file, frame)
	else:
		print(k)

# When everything done, release the video capture object
video_capture.release()

# Closes all the frames
cv2.destroyAllWindows()