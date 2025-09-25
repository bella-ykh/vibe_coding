import pyttsx3
import os

def text_to_speech(input_file, output_file):
    """
    input.txt 파일의 내용을 읽어서 음성으로 변환하고 output.wav 파일로 저장하는 함수
    """
    try:
        # input.txt 파일 읽기
        if not os.path.exists(input_file):
            print(f"오류: {input_file} 파일을 찾을 수 없습니다.")
            return False
        
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
        
        if not text.strip():
            print("오류: input.txt 파일이 비어있습니다.")
            return False
        
        print(f"읽은 텍스트 내용:\n{text}")
        print("\n음성 변환을 시작합니다...")
        
        # TTS 엔진 초기화
        engine = pyttsx3.init()
        
        # 음성 설정 (한국어 지원)
        voices = engine.getProperty('voices')
        
        # 한국어 음성을 찾아서 설정 (가능한 경우)
        for voice in voices:
            if 'korean' in voice.name.lower() or 'korea' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        # 음성 속도 설정 (기본값은 200)
        engine.setProperty('rate', 180)
        
        # 음량 설정 (0.0 ~ 1.0)
        engine.setProperty('volume', 0.8)
        
        # 음성을 파일로 저장
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        
        print(f"음성 변환이 완료되었습니다. 파일이 저장되었습니다: {output_file}")
        return True
        
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")
        return False

def main():
    """
    메인 함수
    """
    input_file = "input.txt"
    output_file = "output.wav"
    
    print("=== 텍스트를 음성으로 변환하는 프로그램 ===")
    print(f"입력 파일: {input_file}")
    print(f"출력 파일: {output_file}")
    print()
    
    # TTS 변환 실행
    success = text_to_speech(input_file, output_file)
    
    if success:
        print("\n프로그램이 성공적으로 완료되었습니다!")
        
        # 파일 크기 확인
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"생성된 음성 파일 크기: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    else:
        print("\n프로그램 실행 중 오류가 발생했습니다.")

if __name__ == "__main__":
    main()
