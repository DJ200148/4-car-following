from ultralytics import YOLO
from ultralytics.solutions import object_counter
import cv2
import time

# Initialize model
model = YOLO("yolov8n.pt").to('cuda')  # Use 'cuda' for GPU
path = 'docs\\videos\\2024-03-10-[19-00]-capture - Trim.mp4'
cap = cv2.VideoCapture(path)
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

region_points = [(20, 400), (1080, 404), (1080, 360), (20, 360)]

video_writer = cv2.VideoWriter("object_counting_output.avi",
                       cv2.VideoWriter_fourcc(*'mp4v'),
                       fps,
                       (w, h))

counter = object_counter.ObjectCounter()
counter.set_args(view_img=True,
                 reg_pts=region_points,
                 classes_names=model.names,
                 draw_tracks=True)

frame_count = 0
total_start_time = time.time()
latencies = []
detect_times = []
count_times = []

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        break
    frame_start_time = time.time()

    # Detection and Tracking
    detect_start_time = time.time()
    tracks = model.track(im0, persist=True, show=False)
    detect_end_time = time.time()

    # Counting
    count_start_time = time.time()
    im0 = counter.start_counting(im0, tracks)
    count_end_time = time.time()

    video_writer.write(im0)
    frame_end_time = time.time()

    # Record latencies
    detect_latency = detect_end_time - detect_start_time
    count_latency = count_end_time - count_start_time
    total_latency = frame_end_time - frame_start_time

    detect_times.append(detect_latency)
    count_times.append(count_latency)
    latencies.append(total_latency)

    frame_count += 1

cap.release()
video_writer.release()
cv2.destroyAllWindows()

total_end_time = time.time()

# Calculate metrics
total_time = total_end_time - total_start_time
average_detect_time = sum(detect_times) / len(detect_times)
average_count_time = sum(count_times) / len(count_times)
average_latency = sum(latencies) / len(latencies)
throughput = frame_count / total_time  # Frames per second
device = next(model.parameters()).device

print(f"Model is running on: {device}")
print(f"Total Frames: {frame_count}")
print(f"Total Time: {total_time:.2f} seconds")
print(f"Average Detection Time: {average_detect_time:.4f} seconds per frame")
print(f"Average Counting Time: {average_count_time:.4f} seconds per frame")
print(f"Average Latency (Total): {average_latency:.4f} seconds per frame")
print(f"Throughput: {throughput:.2f} frames per second")
