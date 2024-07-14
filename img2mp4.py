
import re
import glob
import cv2
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

class Img2MP4:
    def __init__(self, img_folder, output_folder, fps=30, batch_size=100, concatenate=False):
        self.img_folder = img_folder
        self.output_folder = output_folder
        self.fps = fps
        self.batch_size = batch_size
        self.concatenate = concatenate

    def atoi(self, text):
        return int(text) if text.isdigit() else text

    def natural_keys(self, text):
        return [self.atoi(c) for c in re.split(r'(\d+)', text)]

    def create_directories(self):
        try:
            os.makedirs(self.img_folder)
            print(f"{self.img_folder}を作成しました。")
            print(f"{self.img_folder}に画像を保存してください。")
        except:
            pass
        try:
            os.makedirs(self.output_folder)
            print(f"{self.output_folder}を作成しました。")
        except:
            pass

    def read_and_sort_images(self):
        imgs = glob.glob(f"{self.img_folder}/*.jpg")
        imgs = sorted(imgs, key=self.natural_keys)
        return imgs

    def create_video(self, imgs):
        if not imgs:
            print("画像が見つかりませんでした。")
            return

        filename = os.path.basename(imgs[0]).split(".")[0]
        total_batches = len(imgs) // self.batch_size + (1 if len(imgs) % self.batch_size != 0 else 0)
        video_files = []

        for batch in range(total_batches):
            start_index = batch * self.batch_size
            end_index = start_index + self.batch_size
            batch_imgs = imgs[start_index:end_index]

            if not batch_imgs:
                continue

            key = f"{filename}_batch_{batch}"
            mp4_name = f"{self.output_folder}/{key}.mp4"
            video_files.append(mp4_name)

            first_img = cv2.imread(batch_imgs[0])
            height, width, layers = first_img.shape
            size = (width, height)

            out = cv2.VideoWriter(mp4_name, cv2.VideoWriter_fourcc(*'MP4V'), self.fps, size)
            for img_file in batch_imgs:
                img = cv2.imread(img_file)
                out.write(img)
            out.release()
            print(f"{key}.mp4 を作成しました")

        if self.concatenate and video_files:
            self.concatenate_videos(video_files, f"{self.output_folder}/{filename}_final.mp4")

    def concatenate_videos(self, video_files, output_path):
        clips = [VideoFileClip(f) for f in video_files]
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_path, codec="libx264")
        print(f"最終動画ファイル {output_path} を作成しました")

    def run(self):
        self.create_directories()
        imgs = self.read_and_sort_images()
        self.create_video(imgs)