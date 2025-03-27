import cv2

class BlurPlugin:
    def apply_effect(self, frame):
        """ガウシアンブラー (カラー画像対応)"""
        return cv2.GaussianBlur(frame, (25, 25), 0)