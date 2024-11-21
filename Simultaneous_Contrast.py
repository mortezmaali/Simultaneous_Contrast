import cv2
import numpy as np

# Define video properties
width, height = 800, 600
video_duration = 5  # seconds per color combination
fps = 30
frame_count = int(video_duration * fps)

# Define square patch properties
patch_size = 80  # Larger square patches
patch_color = (0, 255, 255)  # Yellow in BGR

# Define background color combinations (left side, right side)
background_combinations = [
    ((255, 0, 0), (0, 255, 0)),       # Left: Blue, Right: Green
    ((0, 0, 255), (255, 0, 0)),       # Left: Red, Right: Blue
    ((0, 255, 0), (0, 0, 0)),         # Left: Green, Right: Black
    ((255, 255, 255), (0, 0, 0)),     # Left: White, Right: Black
    ((255, 0, 255), (255, 255, 0)),   # Left: Magenta, Right: Cyan
    ((128, 128, 128), (255, 255, 255)), # Left: Gray, Right: White
    ((128, 128, 128), (0, 0, 0))      # Left: Gray, Right: Black
]

# Create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('split_color_square_patches_video.mp4', fourcc, fps, (width, height))

# Define text properties
text = "Same colors can appear different\n depending on the background"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.2
font_thickness = 2
edge_thickness = font_thickness + 2  # Slightly thicker for the white edge
text_position = (50, 50)  # Position for text

cv2.namedWindow('Split Color Patches Video', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Split Color Patches Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

for left_color, right_color in background_combinations:
    # Generate frames for the current background combination
    for _ in range(frame_count):
        # Create the left and right backgrounds
        left_side = np.full((height, width // 2, 3), left_color, dtype=np.uint8)
        right_side = np.full((height, width // 2, 3), right_color, dtype=np.uint8)
        
        # Combine the two sides into one frame
        frame = np.hstack((left_side, right_side))
        
        # Draw the left yellow square in the center of the left section
        left_center_x = width // 4
        left_center_y = height // 2
        cv2.rectangle(frame, 
                      (left_center_x - patch_size // 2, left_center_y - patch_size // 2), 
                      (left_center_x + patch_size // 2, left_center_y + patch_size // 2), 
                      patch_color, -1)
        
        # Draw the right yellow square in the center of the right section
        right_center_x = 3 * width // 4
        right_center_y = height // 2
        cv2.rectangle(frame, 
                      (right_center_x - patch_size // 2, right_center_y - patch_size // 2), 
                      (right_center_x + patch_size // 2, right_center_y + patch_size // 2), 
                      patch_color, -1)
        
        # Add the text to the frame with a white edge
        y_offset = text_position[1]
        for line in text.split('\n'):
            # Draw white outline
            cv2.putText(frame, line, (text_position[0], y_offset), font, font_scale, (255, 255, 255), edge_thickness, cv2.LINE_AA)
            # Draw black text on top
            cv2.putText(frame, line, (text_position[0], y_offset), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)
            y_offset += 40  # Adjust spacing between lines
        
        # Write frame to video
        out.write(frame)

        # Show the frame
        cv2.imshow('Split Color Patches Video', frame)
        cv2.waitKey(int(1000 / fps))

# Release video writer and close any OpenCV windows
out.release()
cv2.destroyAllWindows()

print("Video created successfully!")
