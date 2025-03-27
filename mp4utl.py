import os
import cv2
import sys
from typing import Dict, List

class VideoProcessor:
    def __init__(self):
        self.plugins = self._load_plugins()
        
    def _load_plugins(self) -> Dict[str, object]:
        """プラグインをロード"""
        plugins = {}
        plugin_dir = "plugins"
        
        if not os.path.exists(plugin_dir):
            return plugins
            
        sys.path.insert(0, os.path.abspath(plugin_dir))
        
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                try:
                    module = __import__(module_name)
                    for name, obj in vars(module).items():
                        if name.endswith("Plugin") and hasattr(obj, 'apply_effect'):
                            plugins[module_name] = obj()
                            print(f"Loaded plugin: {module_name} ({name})")
                except Exception as e:
                    print(f"Error loading {module_name}: {str(e)}")
                    
        return plugins
    
    def process_video(self, input_path: str, output_path: str, effects: List[str]):
        """動画処理のメイン関数"""
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ValueError(f"入力ファイルを開けません: {input_path}")
        
        # 動画プロパティ取得
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 出力設定 (H.264コーデック推奨)
        fourcc = cv2.VideoWriter_fourcc(*'avc1')  # 'mp4v'でも可
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)
        
        if not out.isOpened():
            raise ValueError(f"出力ファイルを作成できません: {output_path}")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            processed = frame.copy()
            
            # エフェクト適用
            for effect in effects:
                if effect in self.plugins:
                    try:
                        processed = self.plugins[effect].apply_effect(processed)
                        
                        # グレースケール処理後のカラー変換
                        if len(processed.shape) == 2:  # モノクロの場合
                            processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
                            
                    except Exception as e:
                        print(f"エフェクト {effect} 適用エラー: {str(e)}")
                        processed = frame
            
            # フレーム書き込み
            out.write(processed)
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        # 出力ファイルサイズ確認
        output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB単位
        print(f"出力完了: {output_path} (サイズ: {output_size:.2f}MB)")

def main():
    print("=== mp4utl - MP4動画処理ツール ===")
    
    if len(sys.argv) < 4:
        print("使用方法: python mp4utl.py 入力.mp4 出力.mp4 エフェクト1 [エフェクト2...]")
        return
    
    processor = VideoProcessor()
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    effects = sys.argv[3:]
    
    print(f"処理中: {input_path}")
    print(f"適用エフェクト: {', '.join(effects)}")
    
    try:
        processor.process_video(input_path, output_path, effects)
        print("正常に処理が完了しました")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()
