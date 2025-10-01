import os
import glob
from PIL import Image
import sys

# rembg는 선택적으로 import (처음 실행 시 모델 다운로드 시간이 오래 걸림)
try:
    from rembg import remove
    REMBG_AVAILABLE = True
    print("✓ rembg 라이브러리를 사용합니다.")
except ImportError:
    REMBG_AVAILABLE = False
    print("⚠ rembg 라이브러리를 사용할 수 없습니다. 기본 배경 제거 방법을 사용합니다.")

def create_output_folder():
    """output 폴더가 없으면 생성"""
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"'{output_dir}' 폴더를 생성했습니다.")
    return output_dir

def get_image_files():
    """images 폴더에서 모든 이미지 파일을 가져옴"""
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.webp', '*.tiff']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join("images", ext)))
        image_files.extend(glob.glob(os.path.join("images", ext.upper())))
    
    return image_files

def simple_background_removal(input_path, output_path):
    """간단한 배경 제거 (흰색 배경을 투명하게)"""
    try:
        # 이미지 열기
        img = Image.open(input_path)
        
        # RGBA 모드로 변환
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 데이터 가져오기
        data = img.getdata()
        
        # 새로운 데이터 생성 (흰색 배경을 투명하게)
        new_data = []
        for item in data:
            # 흰색에 가까운 픽셀을 투명하게 처리
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((255, 255, 255, 0))  # 투명
            else:
                new_data.append(item)
        
        # 새로운 이미지 생성
        img.putdata(new_data)
        
        # PNG로 저장
        img.save(output_path, 'PNG')
        return True
        
    except Exception as e:
        print(f"✗ {os.path.basename(input_path)} 기본 처리 중 오류: {str(e)}")
        return False

def remove_background_and_save(input_path, output_path):
    """이미지의 배경을 제거하고 PNG로 저장"""
    try:
        if REMBG_AVAILABLE:
            # rembg 사용
            with open(input_path, 'rb') as input_file:
                input_data = input_file.read()
            
            # 배경 제거
            output_data = remove(input_data)
            
            # PNG로 저장
            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)
        else:
            # 기본 배경 제거 방법 사용
            return simple_background_removal(input_path, output_path)
        
        print(f"✓ {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
        return True
        
    except Exception as e:
        print(f"✗ {os.path.basename(input_path)} 처리 중 오류: {str(e)}")
        # rembg 실패 시 기본 방법 시도
        if REMBG_AVAILABLE:
            print(f"  → 기본 방법으로 재시도...")
            return simple_background_removal(input_path, output_path)
        return False

def main():
    print("=== 이미지 배경 제거 및 PNG 변환 프로그램 ===")
    print()
    
    try:
        # images 폴더 존재 확인
        print("1. images 폴더 확인 중...")
        if not os.path.exists("images"):
            print("❌ 'images' 폴더를 찾을 수 없습니다.")
            return
        print("✓ images 폴더를 찾았습니다.")
        
        # output 폴더 생성
        print("2. output 폴더 생성 중...")
        output_dir = create_output_folder()
        
        # 이미지 파일 목록 가져오기
        print("3. 이미지 파일 검색 중...")
        image_files = get_image_files()
        
        if not image_files:
            print("❌ images 폴더에서 이미지 파일을 찾을 수 없습니다.")
            return
        
        print(f"📁 {len(image_files)}개의 이미지 파일을 찾았습니다:")
        for img in image_files:
            print(f"  - {os.path.basename(img)}")
        print()
        
        # 각 이미지 처리
        success_count = 0
        total_count = len(image_files)
        
        for i, input_path in enumerate(image_files, 1):
            print(f"[{i}/{total_count}] 처리 중...")
            
            # 출력 파일명 생성 (원본 파일명 + .png)
            filename = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_dir, f"{filename}.png")
            
            # 배경 제거 및 저장
            if remove_background_and_save(input_path, output_path):
                success_count += 1
        
        print()
        print("=== 처리 완료 ===")
        print(f"✅ 성공: {success_count}/{total_count}개 파일")
        print(f"📁 출력 폴더: {os.path.abspath(output_dir)}")
        
        if success_count < total_count:
            print(f"❌ 실패: {total_count - success_count}개 파일")
            
    except Exception as e:
        print(f"❌ 프로그램 실행 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
