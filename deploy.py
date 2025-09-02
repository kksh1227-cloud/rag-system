#!/usr/bin/env python3
"""
RAG 시스템 자동 배포 스크립트
"""

import os
import subprocess
import webbrowser
import time

def run_command(cmd, cwd=None):
    """명령어 실행"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_remote():
    """Git remote 확인"""
    success, stdout, stderr = run_command("git remote -v")
    return "origin" in stdout if success else False

def deploy_to_railway():
    """Railway 배포 페이지 열기"""
    print("🚂 Railway 배포를 위해 브라우저를 엽니다...")
    webbrowser.open("https://railway.app/new")
    print("Railway 배포 단계:")
    print("1. 'Deploy from GitHub repo' 선택")
    print("2. 저장소 선택")
    print("3. 환경변수 OPENAI_API_KEY 설정")
    print("4. 배포 완료!")

def deploy_to_streamlit():
    """Streamlit Cloud 배포 페이지 열기"""
    print("☁️ Streamlit Cloud 배포를 위해 브라우저를 엽니다...")
    webbrowser.open("https://share.streamlit.io")
    print("Streamlit Cloud 배포 단계:")
    print("1. 'New app' 클릭")
    print("2. Repository 선택")
    print("3. Main file path: streamlit_app.py")
    print("4. 배포 완료!")

def deploy_to_netlify():
    """Netlify Drop 배포"""
    print("🌐 Netlify Drop 배포를 위해 브라우저를 엽니다...")
    webbrowser.open("https://app.netlify.com/drop")
    print("Netlify Drop 배포 단계:")
    print("1. 현재 폴더(rag-system) 전체를 드래그 앤 드롭")
    print("2. 즉시 배포 완료!")
    print("3. 생성된 URL로 접속 가능")

def main():
    print("🚀 RAG 시스템 자동 배포를 시작합니다!")
    print("=" * 50)
    
    # 현재 디렉토리 확인
    if not os.path.exists("requirements.txt"):
        print("❌ RAG 시스템 디렉토리에서 실행해주세요!")
        return
    
    # Git 상태 확인
    if not os.path.exists(".git"):
        print("❌ Git이 초기화되지 않았습니다!")
        return
    
    print("✅ Git 저장소 확인 완료")
    
    # 배포 옵션 선택
    print("\n배포 옵션을 선택하세요:")
    print("1. Netlify Drop (가장 빠름, 즉시 배포)")
    print("2. Railway + Streamlit Cloud (전체 시스템)")
    print("3. 모든 배포 옵션 보기")
    
    try:
        choice = input("선택 (1-3): ").strip()
        
        if choice == "1":
            deploy_to_netlify()
            
        elif choice == "2":
            if not check_git_remote():
                print("\n⚠️ GitHub 저장소가 연결되지 않았습니다.")
                print("다음 단계를 수행해주세요:")
                print("1. GitHub에서 새 저장소 생성")
                print("2. git remote add origin https://github.com/username/repo.git")
                print("3. git push -u origin main")
                
                # GitHub 저장소 생성 페이지 열기
                webbrowser.open("https://github.com/new")
                print("\nGitHub 저장소 생성 페이지를 열었습니다.")
                
                input("\nGitHub에 푸시 완료 후 Enter를 눌러주세요...")
            
            deploy_to_railway()
            time.sleep(2)
            deploy_to_streamlit()
            
        elif choice == "3":
            print("\n🌐 모든 배포 옵션 페이지를 엽니다...")
            deploy_to_netlify()
            time.sleep(1)
            deploy_to_railway() 
            time.sleep(1)
            deploy_to_streamlit()
            
        else:
            print("잘못된 선택입니다.")
            
    except KeyboardInterrupt:
        print("\n\n배포가 취소되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()