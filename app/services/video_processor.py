import cv2
import threading
import time
import numpy as np
from picamera2 import Picamera2

from app.core.models import model_detection
from app.services.relay_control import RelayService


class CameraService:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(
            self.picam2.create_preview_configuration(
                main={"size": (640, 480)}  # Reduce resolution for speed
            )
        )
        self.picam2.start()

        self.lock = threading.Lock()
        self.frame_jpeg = None
        self.helmet_detected = False
        self.running = True

        self.relay_service = RelayService()

        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            try:
                frame = self.picam2.capture_array()
                if frame is None:
                    continue

                # Convert only if needed
                if frame.shape[2] == 4:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                # Smaller frame for inference (huge speed improvement)
                inference_frame = cv2.resize(frame, (416, 416))

                helmet_detected = False

                results = model_detection(inference_frame, verbose=False)

                h_original, w_original = frame.shape[:2]
                h_inf, w_inf = inference_frame.shape[:2]

                scale_x = w_original / w_inf
                scale_y = h_original / h_inf

                for result in results:
                    boxes = result.boxes
                    if boxes is None:
                        continue

                    for box in boxes:
                        conf = float(box.conf[0])
                        if conf < 0.5:
                            continue

                        cls_id = int(box.cls[0])
                        class_name = result.names[cls_id]

                        # Get bounding box (xyxy format)
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

                        # Scale coordinates back to original frame size
                        x1 = int(x1 * scale_x)
                        y1 = int(y1 * scale_y)
                        x2 = int(x2 * scale_x)
                        y2 = int(y2 * scale_y)

                        # Choose color
                        color = (0, 255, 0) if class_name.lower() == "helmet" else (0, 0, 255)

                        # Draw rectangle
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                        # Draw label
                        label = f"{class_name} {conf:.2f}"
                        cv2.putText(frame, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, color, 2)

                        if class_name.lower() == "helmet":
                        # if class_name.lower() == "bike_rider":
                            helmet_detected = True

                # for result in results:
                #     boxes = result.boxes
                #     if boxes is None:
                #         continue

                #     for box in boxes:
                #         conf = float(box.conf[0])
                #         if conf < 0.5:
                #             continue

                #         cls_id = int(box.cls[0])
                #         class_name = result.names[cls_id]

                #         if class_name.lower() == "helmet":
                #             helmet_detected = True
                #             break  # Stop checking once found

                #     if helmet_detected:
                #         break

                # Relay control (clean and direct)
                if helmet_detected:
                    self.relay_service.turn_on()
                else:
                    self.relay_service.turn_off()

                # Encode for streaming
                ret, jpeg = cv2.imencode(".jpg", frame)
                if not ret:
                    continue

                with self.lock:
                    self.frame_jpeg = jpeg.tobytes()
                    self.helmet_detected = helmet_detected

            except Exception as e:
                print(f"Camera update error: {e}")

    def get_frame(self):
        with self.lock:
            return self.frame_jpeg

    def get_helmet_status(self):
        with self.lock:
            return self.helmet_detected

    def stop(self):
        self.running = False
        self.thread.join()
        self.picam2.stop()
        self.relay_service.cleanup()
        
        
        
# import cv2
# import threading
# import time
# import numpy as np
# from ultralytics import YOLO
# from picamera2 import Picamera2

# from app.core.models import model_detection

# from app.services.relay_control import RelayService

# class CameraService:
#     def __init__(self):
        
#         self.picam2 = Picamera2()
#         self.picam2.configure(self.picam2.create_preview_configuration())
#         self.picam2.start()
        
#         self.lock = threading.Lock()
#         self.frame_jpeg = None
#         self.helmet_detected = False
#         self.running = True
#         self.bypass_mode = None
#         self.relay_service = RelayService()
        
#         self.thread = threading.Thread(target=self.update, daemon=True)
#         self.thread.start()
        
    
#     def update(self):
#         while self.running:
#             try:
#                 # Capture frame from PiCamera2
#                 frame = self.picam2.capture_array()

#                 if frame is None:
#                     continue

#                 if len(frame.shape) == 3:
#                     if frame.shape[2] == 4:
#                         frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
#                     else:
#                         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

#                 helmet_detected = False

#                 # Run YOLO inference
#                 results = model_detection(frame, verbose=False)

#                 for result in results:
#                     boxes = result.boxes
#                     if boxes is None:
#                         continue

#                     for box in boxes:
                        
#                         cls_id = int(box.cls[0])
#                         conf = float(box.conf[0])
#                         class_name = result.names[cls_id]

#                         if conf > 0.5:
#                             if class_name.lower() == "helmet":
#                                 helmet_detected = True

#                             x1, y1, x2, y2 = map(int, box.xyxy[0])

#                             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                             cv2.putText(
#                                 frame,
#                                 f"{class_name} {conf:.2f}",
#                                 (x1, y1 - 10),
#                                 cv2.FONT_HERSHEY_SIMPLEX,
#                                 0.6,
#                                 (0, 255, 0),
#                                 2,
#                             )

#                 # Relay control (if not bypassed)
#                 if self.bypass_mode == "always_on":
#                     self.relay_service.turn_on()
#                 elif self.bypass_mode == "always_off":
#                     self.relay_service.turn_off()
#                 else:
#                     if helmet_detected:
#                         self.relay_service.turn_on()
#                     else:
#                         self.relay_service.turn_off()

#                 # Encode frame to JPEG for streaming
#                 ret, jpeg = cv2.imencode(".jpg", frame)
#                 if not ret:
#                     continue

#                 with self.lock:
#                     self.frame_jpeg = jpeg.tobytes()
#                     self.helmet_detected = helmet_detected

#             except Exception as e:
#                 print(f"Camera update error: {e}")

#             time.sleep(0.03)  
    
#     def bypass_relay_always_on(self):
#         with self.lock:
#             self.bypass_mode = "always_on"

#     def bypass_relay_always_off(self):
#         with self.lock:
#             self.bypass_mode = "always_off"

#     def disable_bypass(self):
#         with self.lock:
#             self.bypass_mode = None

#     def get_frame(self):
#         with self.lock:
#             return self.frame_jpeg
 
#     def get_helmet_status(self):
#         with self.lock:
#             return self.helmet_detected

#     def stop(self):
#         self.running = False
#         self.thread.join()
#         self.picam2.stop()
#         self.relay_service.cleanup()

