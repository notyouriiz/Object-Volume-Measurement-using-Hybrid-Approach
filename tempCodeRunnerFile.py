import cv2
import numpy as np

class DetectorObj:
    def __init__(self):
        pass

    def detect_objects(self, frame):
        """
        Detects large objects using adaptive thresholding and contour extraction.
        Uses an inverse threshold to handle bright objects on dark backgrounds.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY_INV, 19, 5
        )

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        objects_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 2000]
        return objects_contours


def main():
    # --- Initialize ArUco (DICT_4X4_50) ---
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    aruco_params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    marker_id_expected = 0  # your marker ID
    marker_size_cm = 5    # printed marker side size (adjust to your real value)

    pixel_cm_ratio = None
    detector_obj = DetectorObj()

    # --- Start camera ---
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Camera read failed.")
            break

        img = frame.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- Detect ArUco marker ---
        corners, ids, _ = detector.detectMarkers(gray)

        marker_status = "No marker"
        if ids is not None:
            for i, marker_id in enumerate(ids.flatten()):
                if marker_id == marker_id_expected:
                    cv2.polylines(img, [np.intp(corners[i][0])], True, (255, 0, 0), 2)
                    marker_status = f"Marker OK (ID {marker_id})"

                    # Calculate marker perimeter and derive cm/pixel
                    side_px = np.mean([
                        np.linalg.norm(corners[i][0][0] - corners[i][0][1]),
                        np.linalg.norm(corners[i][0][1] - corners[i][0][2]),
                        np.linalg.norm(corners[i][0][2] - corners[i][0][3]),
                        np.linalg.norm(corners[i][0][3] - corners[i][0][0]),
                    ])
                    pixel_cm_ratio = side_px / marker_size_cm
                    break
        else:
            marker_status = "Marker not detected"

        # --- Detect objects ---
        contours = detector_obj.detect_objects(img)
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            (x, y), (w, h), _ = rect

            if pixel_cm_ratio:
                object_width = w / pixel_cm_ratio
                object_height = h / pixel_cm_ratio
            else:
                object_width, object_height = 0, 0

            box = cv2.boxPoints(rect)
            box = np.intp(box)
            cv2.polylines(img, [box], True, (0, 255, 0), 2)

            cv2.putText(img, f"W: {object_width:.2f} cm", (int(x - 100), int(y - 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100), 2)
            cv2.putText(img, f"H: {object_height:.2f} cm", (int(x - 100), int(y + 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100), 2)

        cv2.putText(img, marker_status, (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

        cv2.imshow("Object Measurement (4x4_50)", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
