// 시대별 정보
const periods = {
    prehistoric: { title: '🦴 선사시대' },
    threekingdoms: { title: '🏺 삼국시대' },
    laterthree: { title: '⚔️ 후삼국' },
    unifiedsilla: { title: '🌟 통일신라' },
    goryeo: { title: '👑 고려' },
    joseon: { title: '📜 조선' },
    modern: { title: '🗽 근현대' }
};

// JSON 데이터 로드 및 초기화
async function init() {
    try {
        const response = await fetch('videos.json');
        const videosData = await response.json();
        
        // 비디오 카드 생성
        createVideoCards(videosData);
        
        // 탭 전환 기능
        initTabs();
        
        // 비디오 팝업 기능
        initVideoModal();
        
    } catch (error) {
        console.error('데이터 로드 실패:', error);
    }
}

// 비디오 카드 생성
function createVideoCards(videosData) {
    Object.keys(videosData).forEach(period => {
        const section = document.getElementById(period);
        if (!section) return;
        
        const videoGrid = section.querySelector('.video-grid');
        videoGrid.innerHTML = '';
        
        videosData[period].forEach(video => {
            const card = document.createElement('div');
            card.className = 'video-card';
            card.innerHTML = `
                <h3>${video.title}</h3>
                <div class="video-wrapper" data-video-id="${video.id}">
                    <img src="https://img.youtube.com/vi/${video.id}/hqdefault.jpg" 
                         alt="${video.title}"
                         onerror="this.onerror=null; this.src='https://via.placeholder.com/480x360/e0e0e0/666666?text=No+Thumbnail';">
                    <div class="play-button"></div>
                </div>
            `;
            videoGrid.appendChild(card);
        });
    });
}

// 탭 전환 기능
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const contentSections = document.querySelectorAll('.content-section');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.dataset.tab;
            
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            contentSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetTab) {
                    section.classList.add('active');
                }
            });
        });
    });
}

// 비디오 팝업 기능
function initVideoModal() {
    const modal = document.getElementById('videoModal');
    const modalIframe = document.getElementById('modalIframe');
    const closeButton = document.querySelector('.close-button');
    
    // 비디오 클릭 이벤트 (이벤트 위임 사용)
    document.addEventListener('click', (e) => {
        const wrapper = e.target.closest('.video-wrapper');
        if (wrapper) {
            const videoId = wrapper.dataset.videoId;
            openModal(videoId);
        }
    });
    
    // 썸네일 에러 처리 제거 (이미 HTML에서 처리)
    
    // 모달 열기
    function openModal(videoId) {
        modalIframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    // 모달 닫기
    function closeModal() {
        modal.classList.remove('active');
        modalIframe.src = '';
        document.body.style.overflow = 'auto';
    }
    
    // 닫기 버튼
    closeButton.addEventListener('click', closeModal);
    
    // 배경 클릭시 닫기
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // ESC 키로 닫기
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
}

// 페이지 로드시 초기화
document.addEventListener('DOMContentLoaded', init);