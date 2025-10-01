import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def get_kospi_index():
    """
    네이버 금융에서 코스피 지수를 가져오는 함수
    """
    try:
        # 네이버 금융 메인 페이지 URL
        url = "https://finance.naver.com/"
        
        # User-Agent 헤더 설정 (봇 차단 방지)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 웹페이지 요청
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 에러 체크
        
        # HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 코스피 지수 정보 찾기
        kospi_info = {}
        
        # 방법 1: 특정 클래스나 ID로 찾기
        kospi_elements = soup.find_all(['span', 'div', 'td'], string=re.compile(r'코스피'))
        
        # 방법 2: 지수 관련 텍스트가 포함된 요소 찾기
        index_elements = soup.find_all(string=re.compile(r'3,?\d{3}\.\d{2}'))
        
        # 방법 3: 더 구체적인 패턴으로 코스피 데이터 찾기
        kospi_pattern = re.compile(r'코스피.*?(\d{1,3}(?:,\d{3})*\.\d{2}).*?([+-]?\d+\.\d{2})')
        
        # 페이지 전체 텍스트에서 코스피 정보 검색
        page_text = soup.get_text()
        kospi_matches = kospi_pattern.findall(page_text)
        
        if kospi_matches:
            for match in kospi_matches:
                index_value = match[0].replace(',', '')
                change_value = match[1]
                kospi_info['index'] = float(index_value)
                kospi_info['change'] = float(change_value)
                break
        
        # 방법 4: 테이블이나 특정 구조에서 찾기
        if not kospi_info:
            # 시세 관련 테이블이나 div 찾기
            market_elements = soup.find_all(['table', 'div'], class_=re.compile(r'(market|index|sise)', re.I))
            
            for element in market_elements:
                text = element.get_text()
                if '코스피' in text:
                    # 숫자 패턴 찾기
                    numbers = re.findall(r'(\d{1,3}(?:,\d{3})*\.\d{2})', text)
                    if numbers:
                        kospi_info['index'] = float(numbers[0].replace(',', ''))
                        # 변화량 찾기
                        changes = re.findall(r'([+-]?\d+\.\d{2})', text)
                        if changes:
                            kospi_info['change'] = float(changes[0])
                        break
        
        return kospi_info
        
    except requests.RequestException as e:
        print(f"웹페이지 요청 중 오류 발생: {e}")
        return None
    except Exception as e:
        print(f"데이터 파싱 중 오류 발생: {e}")
        return None

def format_kospi_info(kospi_info):
    """
    코스피 정보를 보기 좋게 포맷팅하는 함수
    """
    if not kospi_info:
        return "코스피 지수 정보를 가져올 수 없습니다."
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    index = kospi_info.get('index', 'N/A')
    change = kospi_info.get('change', 'N/A')
    
    # 변화량에 따른 상승/하락 표시
    if isinstance(change, (int, float)):
        if change > 0:
            change_str = f"+{change:.2f} (상승)"
        elif change < 0:
            change_str = f"{change:.2f} (하락)"
        else:
            change_str = "0.00 (보합)"
    else:
        change_str = str(change)
    
    result = f"""
=== 코스피 지수 정보 ===
조회 시간: {current_time}
현재 지수: {index:,.2f}
전일 대비: {change_str}
{'=' * 25}
    """
    
    return result.strip()

def main():
    """
    메인 실행 함수
    """
    print("네이버 금융에서 코스피 지수를 가져오는 중...")
    
    kospi_info = get_kospi_index() 
    result = format_kospi_info(kospi_info)
    
    print(result)
    
    # 추가 정보 출력
    if kospi_info:
        print("\n※ 데이터 출처: 네이버 금융 (https://finance.naver.com/)")
        print("※ 실시간 데이터는 네이버 금융 사이트를 참조하세요.")

if __name__ == "__main__":
    main()
