from picamera2 import Picamera2
import cv2
import threading
import time
from app.core.models import model_detection


def draw_detection(frame_bgr, result):
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        cls = int(box.cls[0])
        label = model_detection.names[cls]

        # Draw bounding box
        cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Draw label
        text = f"{label}: {confidence:.2f}"
        cv2.putText(
            frame_bgr,
            text,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2,
        )


class CameraService:
    def __init__(self):
        self.picam2 = Picamera2()
        self.lock = threading.Lock()
        self.frame_jpeg = None
        self.running = True

        config = self.picam2.create_video_configuration(
            main={"format": "XRGB8888", "size": (640, 480)}
        )
        self.picam2.configure(config)
        self.picam2.start()
        time.sleep(2)

        self.thread = threading.Thread(
            target=self._capture_loop, daemon=True
        )
        self.thread.start()

    def _capture_loop(self):
        while self.running:
            try:
                frame = self.picam2.capture_array()
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                # --- Detection only ---
                results = model_detection.predict(
                    source=frame_bgr,
                    verbose=False
                )

                for r in results:
                    draw_detection(frame_bgr, r)

                ret, buffer = cv2.imencode(".jpg", frame_bgr)
                if not ret:
                    continue

                with self.lock:
                    self.frame_jpeg = buffer.tobytes()

            except Exception as e:
                print("Camera loop error:", e)
                time.sleep(0.1)

    def get_frame(self):
        with self.lock:
            return self.frame_jpeg

    def stop(self):
        self.running = False
        self.picam2.stop()