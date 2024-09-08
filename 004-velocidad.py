import cv2
import numpy as np
import os
import time
import math
from datetime import datetime, timedelta

# Create render directory if it doesn't exist
render_dir = "render"
if not os.path.exists(render_dir):
    os.makedirs(render_dir)

# Get current epoch time for filename
epoch_time = int(time.time())
filename = f"{render_dir}/{epoch_time}.mp4"

# Video settings
width = 1920
height = 1080
fps = 60
duration = 60  # in seconds
total_frames = fps * duration

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

# Starfield settings
num_stars = 1000
stars = []

class Star:
    def __init__(self):
        self.angle = np.random.rand() * 2 * np.pi
        self.distance = np.random.rand() * 1000
        self.speed = self.distance / 100  # Keep the original speed logic

# Start time
start_time = time.time()

# Main loop to generate each frame
for frame in range(total_frames):
    # Create a black canvas
    frame_img = np.zeros((height, width, 3), dtype=np.uint8)

    # Gradually add new stars continuously
    if len(stars) < num_stars:
        stars.append(Star())

    for star in stars:
        star.distance += star.speed
        if star.distance > 1000:
            star.distance = 0.1
            star.angle = np.random.rand() * 2 * np.pi  # Recalculate angle for a new trajectory
        
        x = int(width/2 + star.distance * math.cos(star.angle))
        y = int(height/2 + star.distance * math.sin(star.angle))
        
        x2 = int(width/2 + star.distance * 1.1 * math.cos(star.angle + 0.01))
        y2 = int(height/2 + star.distance * 1.1 * math.sin(star.angle + 0.01))

        if 0 <= x < width and 0 <= y < height and 0 <= x2 < width and 0 <= y2 < height:
            cv2.line(frame_img, (x, y), (x2, y2), (255, 255, 255), 1)
    
    # Add some fading effect
    frame_img = cv2.addWeighted(frame_img, 0.9, frame_img, 0.1, 0)

    # Write the frame to the video file
    out.write(frame_img)

    # Statistics every 60 frames
    if (frame + 1) % 60 == 0:
        elapsed_time = time.time() - start_time
        time_passed = str(timedelta(seconds=int(elapsed_time)))
        frames_remaining = total_frames - (frame + 1)
        estimated_time_remaining = elapsed_time / (frame + 1) * frames_remaining
        time_remaining = str(timedelta(seconds=int(estimated_time_remaining)))
        estimated_finish_time = datetime.now() + timedelta(seconds=estimated_time_remaining)
        percent_complete = (frame + 1) / total_frames * 100

        print(f"Frame: {frame + 1}/{total_frames}")
        print(f"Time Passed: {time_passed}")
        print(f"Time Remaining: {time_remaining}")
        print(f"Estimated Finish Time: {estimated_finish_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Percentage Complete: {percent_complete:.2f}%")
        print("-" * 50)

# Release the video writer
out.release()

print(f"Video saved as {filename}")
