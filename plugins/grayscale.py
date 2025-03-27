import cv2

class GrayscalePlugin:
    def apply_effect(self, frame):
        """グレースケール変換 (BGR -> GRAY)"""
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)