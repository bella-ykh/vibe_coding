#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hello World 프로그램
이 프로그램은 간단한 인사말을 출력합니다.
"""

def print_rainbow_text(text):
    """텍스트를 무지개 색상으로 출력하는 함수"""
    colors = [
        '\033[91m',  # 빨간색
        '\033[93m',  # 노란색
        '\033[92m',  # 초록색
        '\033[96m',  # 청록색
        '\033[94m',  # 파란색
        '\033[95m',  # 보라색
    ]
    reset = '\033[0m'  # 색상 리셋
    
    colored_text = ""
    for i, char in enumerate(text):
        if char != ' ':  # 공백이 아닌 경우에만 색상 적용
            color = colors[i % len(colors)]
            colored_text += f"{color}{char}{reset}"
        else:
            colored_text += char
    
    return colored_text

def main():
    """메인 함수"""
    # 무지개 색상으로 Hello, World! 출력
    rainbow_hello = print_rainbow_text("Hello, World!")
    print(rainbow_hello)
    
    # 사용자 이름을 받아서 개인화된 인사
    name = input("이름을 입력해주세요: ")
    rainbow_name = print_rainbow_text(f"Hello, {name}! Welcome!")
    print(rainbow_name)

if __name__ == "__main__":
    main()
