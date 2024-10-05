import os, psutil, sys, subprocess
temp_path = os.getenv('TEMP')
lock_program = os.path.join(temp_path, 'temp.lock')

# Tên của chương trình cần kiểm tra
program_name = "ToolDriverCanon.exe"  # Thay thế bằng tên chương trình thực tế

def is_program_running(program_name):
    """Kiểm tra xem chương trình có đang chạy không."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == program_name:
            return True
    return False

while True:
    # Kiểm tra chương trình có đang chạy không
    if not is_program_running(program_name):
        # Nếu không chạy, xóa file lock
        if os.path.exists(lock_program):
            try:
                result = subprocess.run(
                ['taskkill /f /im SetupDriver.exe /t'],
                ['taskkill /f /im CNABBUND.exe /t'],
                ['taskkill /f /im CNAB4UND.exe /t'],  # '/c' là tham số CMD để thực hiện lệnh và sau đó thoát
                capture_output=True,       # Capture stdout và stderr
                text=True                   # Trả về đầu ra dưới dạng chuỗi thay vì bytes
                )
            except:
                pass
            os.remove(lock_program)
            sys.exit()
        else:
            sys.exit()
    
