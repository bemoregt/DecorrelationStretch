import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def enhance_contrast(img):
    # 이미지를 BGR 형식으로 분리
    b, g, r = cv2.split(img)
    
    # 각 채널의 평균 계산
    b_mean = np.mean(b)
    g_mean = np.mean(g)
    r_mean = np.mean(r)
    
    # 평균을 각 채널에서 빼기
    b_new = b - b_mean
    g_new = g - g_mean
    r_new = r - r_mean
    
    # 각 채널의 표준편차 계산
    b_std = np.std(b_new)
    g_std = np.std(g_new)
    r_std = np.std(r_new)
    
    # 최대 표준편차 계산
    new_std = np.max([b_std, g_std, r_std])
    
    # 각 채널 스케일링
    b_scale = np.clip(b_new / new_std * 255, 0, 255).astype(np.uint8)
    g_scale = np.clip(g_new / new_std * 255, 0, 255).astype(np.uint8)
    r_scale = np.clip(r_new / new_std * 255, 0, 255).astype(np.uint8)
    
    # 채널 합치기
    out_img = cv2.merge((b_scale, g_scale, r_scale))
    return out_img

def resize_image(img, width, height):
    """이미지 비율을 유지하면서 지정된 크기 내에 맞게 조정"""
    img_height, img_width = img.shape[:2]
    ratio = min(width / img_width, height / img_height)
    new_width = int(img_width * ratio)
    new_height = int(img_height * ratio)
    return cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

def load_image():
    # 파일 다이얼로그를 통해 이미지 파일 선택
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    
    if file_path:
        # 이미지 읽기
        img = cv2.imread(file_path)
        
        if img is not None:
            # 화면 크기에 맞게 이미지 리사이징
            display_width = 400
            display_height = 400
            
            # 원본 이미지 리사이징 및 표시
            resized_img = resize_image(img, display_width, display_height)
            img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(img_pil)
            original_label.config(image=img_tk)
            original_label.image = img_tk
            
            # 대비 향상 이미지 처리
            enhanced_img = enhance_contrast(img)
            
            # 향상된 이미지 리사이징 및 표시
            resized_enhanced = resize_image(enhanced_img, display_width, display_height)
            enhanced_rgb = cv2.cvtColor(resized_enhanced, cv2.COLOR_BGR2RGB)
            enhanced_pil = Image.fromarray(enhanced_rgb)
            enhanced_tk = ImageTk.PhotoImage(enhanced_pil)
            enhanced_label.config(image=enhanced_tk)
            enhanced_label.image = enhanced_tk
            
            # 파일명만 추출하여 표시
            import os
            filename = os.path.basename(file_path)
            status_label.config(text=f"로드된 이미지: {filename}")
        else:
            status_label.config(text="이미지를 로드할 수 없습니다.")
    else:
        status_label.config(text="이미지가 선택되지 않았습니다.")

# 메인 창 생성
root = tk.Tk()
root.title("이미지 색상 대비 향상")
root.geometry("900x600")  # 창 크기 증가
root.configure(bg="#333333")  # 배경색 설정

# 상단 프레임 (버튼용)
top_frame = tk.Frame(root, bg="#333333")
top_frame.pack(pady=20)

# 이미지 로드 버튼
load_button = tk.Button(
    top_frame, 
    text="Load Image", 
    command=load_image, 
    width=20, 
    height=2,
    bg="#E0E0E0",
    font=("Arial", 12)
)
load_button.pack()

# 중앙 프레임 (이미지 표시용)
center_frame = tk.Frame(root, bg="#333333")
center_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# 원본 이미지 프레임
original_frame = tk.Frame(center_frame, bg="#333333")
original_frame.pack(side=tk.LEFT, padx=10, pady=5, expand=True, fill=tk.BOTH)

original_title = tk.Label(
    original_frame, 
    text="Original Image", 
    bg="#333333", 
    fg="white",
    font=("Arial", 12, "bold")
)
original_title.pack(pady=(0, 10))

original_label = tk.Label(original_frame, bg="#222222")
original_label.pack(expand=True, fill=tk.BOTH)

# 향상된 이미지 프레임
enhanced_frame = tk.Frame(center_frame, bg="#333333")
enhanced_frame.pack(side=tk.RIGHT, padx=10, pady=5, expand=True, fill=tk.BOTH)

enhanced_title = tk.Label(
    enhanced_frame, 
    text="Decorrelation Stretching", 
    bg="#333333", 
    fg="white",
    font=("Arial", 12, "bold")
)
enhanced_title.pack(pady=(0, 10))

enhanced_label = tk.Label(enhanced_frame, bg="#222222")
enhanced_label.pack(expand=True, fill=tk.BOTH)

# 하단 상태 표시줄
status_label = tk.Label(
    root, 
    text="이미지를 로드하려면 '이미지 로드' 버튼을 클릭하세요.", 
    bd=1, 
    relief=tk.SUNKEN, 
    anchor=tk.W,
    bg="#444444",
    fg="white",
    font=("Arial", 10)
)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
