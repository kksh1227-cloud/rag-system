import requests
import json
import webbrowser
import time

def create_github_repo():
    """GitHub API를 사용하여 저장소 생성"""
    
    # GitHub 개인 액세스 토큰이 필요합니다
    print("🔑 GitHub 저장소를 생성하려면 개인 액세스 토큰이 필요합니다.")
    print("📋 다음 단계를 따라주세요:")
    print()
    print("1. GitHub Settings 페이지를 엽니다...")
    webbrowser.open("https://github.com/settings/tokens/new")
    time.sleep(2)
    
    print("2. 토큰 생성:")
    print("   - Note: 'RAG System Deployment'")
    print("   - Expiration: 30 days")
    print("   - Scopes: 'repo' 체크")
    print("   - Generate token 클릭")
    print()
    
    token = input("생성된 토큰을 입력하세요 (ghp_로 시작): ").strip()
    
    if not token.startswith('ghp_'):
        print("❌ 올바른 토큰 형식이 아닙니다.")
        return False
    
    # GitHub API로 저장소 생성
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': 'rag-system',
        'description': 'LLM + RAG System - Document-based Q&A with FastAPI and Streamlit',
        'private': False,
        'has_issues': True,
        'has_projects': False,
        'has_wiki': False
    }
    
    try:
        response = requests.post(
            'https://api.github.com/user/repos',
            headers=headers,
            json=data
        )
        
        if response.status_code == 201:
            repo_data = response.json()
            clone_url = repo_data['clone_url']
            html_url = repo_data['html_url']
            
            print(f"✅ 저장소가 성공적으로 생성되었습니다!")
            print(f"📋 저장소 URL: {html_url}")
            print(f"🔗 Clone URL: {clone_url}")
            
            # Git remote 추가 및 푸시
            import subprocess
            
            print("\n📤 코드를 GitHub에 푸시하는 중...")
            
            commands = [
                f"git remote add origin {clone_url}",
                "git push -u origin main"
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {cmd}")
                else:
                    print(f"❌ {cmd} - {result.stderr}")
            
            print(f"\n🎉 GitHub 저장소 생성 및 코드 업로드 완료!")
            print(f"🌐 저장소 확인: {html_url}")
            
            return html_url
            
        else:
            print(f"❌ 저장소 생성 실패: {response.status_code}")
            print(f"오류 메시지: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def simple_method():
    """간단한 수동 방법"""
    print("🚀 간단한 방법으로 진행합니다!")
    print()
    print("1. GitHub 저장소 생성 페이지를 엽니다...")
    webbrowser.open("https://github.com/new")
    time.sleep(1)
    
    print("2. 다음 정보를 입력하세요:")
    print("   - Repository name: rag-system")  
    print("   - Description: LLM + RAG System")
    print("   - Public 선택")
    print("   - Create repository 클릭")
    print()
    
    input("저장소 생성 완료 후 Enter를 눌러주세요...")
    
    username = input("GitHub 사용자명을 입력하세요: ").strip()
    
    if username:
        repo_url = f"https://github.com/{username}/rag-system.git"
        
        print(f"\n📤 코드를 GitHub에 푸시합니다...")
        
        import subprocess
        
        commands = [
            f"git remote add origin {repo_url}",
            "git push -u origin main"
        ]
        
        for cmd in commands:
            print(f"실행 중: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ 성공")
            else:
                print(f"❌ 실패: {result.stderr}")
                if "already exists" in result.stderr:
                    print("이미 remote가 존재합니다. git push만 실행합니다.")
                    subprocess.run("git push -u origin main", shell=True)
        
        return f"https://github.com/{username}/rag-system"
    
    return False

if __name__ == "__main__":
    print("🐙 GitHub 저장소 생성 방법을 선택하세요:")
    print("1. 자동 생성 (GitHub 토큰 필요)")
    print("2. 수동 생성 (권장)")
    
    choice = input("선택 (1 또는 2): ").strip()
    
    if choice == "1":
        repo_url = create_github_repo()
    else:
        repo_url = simple_method()
    
    if repo_url:
        print(f"\n🎉 다음 단계: Streamlit Cloud 배포")
        print(f"🔗 저장소 URL: {repo_url}")
        
        # Streamlit Cloud 페이지 열기
        time.sleep(2)
        print("\n☁️ Streamlit Cloud 페이지를 엽니다...")
        webbrowser.open("https://share.streamlit.io")
    else:
        print("\n❌ 저장소 생성에 실패했습니다.")