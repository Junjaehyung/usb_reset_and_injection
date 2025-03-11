import os
import shutil
from concurrent.futures import ThreadPoolExecutor

# 드라이브 목록 고정
usb_list = []
print("사용할 USB 포트를 입력해주세요\n>>")
usb_list = input().split(" ")

# 현재 스크립트 위치를 기준으로 상대 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))  # 스크립트 위치 절대경로
source_dir = os.path.join(base_dir, "injection_things")  # injection_things 폴더 경로

# source_dir 확인을 위해 추가한 코드
if not os.path.exists(source_dir):
    print(f"지정된 경로를 찾을 수 없습니다: {source_dir}")
    exit()

i = int(0)
while i < 1:
    def reset_and_copy_files(usb_drive):
        usb_path = f"{usb_drive}:/"

        # USB 드라이브가 존재하는지 확인
        if not os.path.exists(usb_path):
            print(f"{usb_drive} 드라이브가 연결되어 있지 않습니다. 작업을 건너뜁니다.")
            return

        print(f"{usb_drive} 드라이브에서 파일 삭제 중...")
        for root, dirs, files in os.walk(usb_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"파일 삭제 오류: {file_path}, {e}")

        print(f"{usb_drive} 드라이브에 파일 복사 중...")

        try:
            shutil.copytree(source_dir, usb_path, dirs_exist_ok=True)
        except Exception as e:
            print(f"파일 복사 오류: {usb_drive}, {e}")
        
    with ThreadPoolExecutor() as executor:
        executor.map(reset_and_copy_files, usb_list)

    print("모든 작업이 완료되었습니다.\n작업을 중단합니다.")
    print("똑같은 세팅으로 계속 하시겠습니까? (Y or N)\n>>")
    l = input()
    if l == 'N':
        i += 1
