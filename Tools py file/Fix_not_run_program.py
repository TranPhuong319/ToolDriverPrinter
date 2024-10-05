import os
import shutil
import tempfile
import ctypes
from datetime import datetime
import tempfile
import fnmatch
import glob
import subprocess

def delete_temp_files_and_dirs():
    # Đường dẫn đến thư mục Temp
    temp_dir = tempfile.gettempdir()
    
    print(f"Deleting files and folders in {temp_dir}")
    
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Xóa tệp hoặc liên kết
                print(f"Deleted file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Xóa thư mục và nội dung của nó
                print(f"Deleted folder: {file_path}")
        except Exception as e:
            pass  # Bỏ qua lỗi và tiếp tục
    
    # Hiển thị thông báo hoàn thành bằng ctypes
    MB_OK = 0x00000000
    MB_ICONINFORMATION = 0x00000040
    message = "Fixed! Please run the software again.\n\nĐã sửa lỗi xong! Vui lòng chạy lại phần mềm"
    title = "Complete"
    ctypes.windll.user32.MessageBoxW(None, message, title, MB_ICONINFORMATION | MB_OK)

def install_certificate():
    # Lấy đường dẫn đến thư mục tạm
    temp_folder = tempfile.gettempdir()

    # Lấy thời gian hiện tại khi chương trình bắt đầu
    program_start_time = datetime.now()

    # Danh sách để lưu trữ các thư mục và thời gian tạo của chúng
    directories_with_time = []

    # Duyệt qua tất cả các mục trong thư mục tạm
    for item in os.listdir(temp_folder):
        item_path = os.path.join(temp_folder, item)
        # Kiểm tra nếu là thư mục và khớp với mẫu onefile_*****
        if os.path.isdir(item_path) and fnmatch.fnmatch(item, 'onefile_*'):
            # Lấy thời gian tạo thư mục
            creation_time = os.path.getctime(item_path)
            directories_with_time.append((item_path, creation_time))

    # Kiểm tra xem có thư mục nào khớp với mẫu không
    if not directories_with_time:
        print("Không tìm thấy thư mục nào khớp với mẫu trong thư mục tạm.")
    else:
        # Tìm thư mục gần nhất
        nearest_directory = min(directories_with_time, key=lambda x: abs(x[1] - program_start_time.timestamp()))

        # Lấy tên và thời gian tạo của thư mục gần nhất
        nearest_path, nearest_creation_time = nearest_directory
        formatted_time = datetime.fromtimestamp(nearest_creation_time).strftime('%Y-%m-%d %H:%M:%S')

        print(f"Thư mục gần nhất: {nearest_path}")
        print(f"Ngày tạo: {formatted_time}")

        # Tìm file .crt và certutil.exe trong thư mục đó
        cer_files = glob.glob(os.path.join(nearest_path, "*.crt"))
        certutil_files = glob.glob(os.path.join(nearest_path, "certutil.exe"))

        if cer_files and certutil_files:
            # Lấy file .crt và certutil.exe đầu tiên tìm được
            cer_file_path = cer_files[0]
            certutil_exe_path = certutil_files[0]

            # Chạy lệnh certutil từ thư mục đã tìm thấy để thêm chứng chỉ vào kho lưu trữ Root
            certutil_command = f'"{certutil_exe_path}" -addstore "Root" "{cer_file_path}"'
            print(f"Đang chạy lệnh: {certutil_command}")

            # Sử dụng subprocess để chạy lệnh
            process = subprocess.run(certutil_command, shell=True)

            if process.returncode == 0:
                print("Chứng chỉ đã được thêm thành công vào kho lưu trữ Root.")
            else:
                print("Có lỗi xảy ra khi thêm chứng chỉ.")
        else:
            print("Không tìm thấy cả tệp chứng chỉ .crt và/hoặc certutil.exe trong thư mục gần nhất.")

# Gọi hàm để cài đặt chứng chỉ
install_certificate()

# Gọi hàm để xóa tệp và thư mục trong Temp
delete_temp_files_and_dirs()
