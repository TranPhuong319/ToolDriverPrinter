#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Easy Printer Driver Install/Uninstall Tool
    Copyright ©️ 2023-2025 TranPhuong319.
    Version 1.0.2.
    Compile by Nuitka.
    License: Apache License.
    More infomation, visit https://github.com/TranPhuong319/ToolDriverPrinter.git
"""
import json ; import os ; import subprocess ; import sys ; import wx.adv ; import configparser
import glob; import tempfile; from datetime import datetime; import re ; import webbrowser 
import wx ; import msvcrt ; import locale ; import threading; import time; import winsound 
from plyer import notification; import fnmatch ; import winreg ; import psutil # Nhập thư viện cần thiết

# Thay đổi thư mục làm việc thành thư mục chứa tệp chạy
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# Lấy thời gian hiện tại
current_time = time.time()

# Lấy thư mục tạm
temp_dir = os.getenv('TEMP')

# Tìm tất cả thư mục có định dạng 'onefile_XXXX_...' trong thư mục tạm
onefile_dirs = glob.glob(os.path.join(temp_dir, 'onefile_*'))

# Kiểm tra xem có thư mục nào khớp với định dạng không và tìm thư mục gần nhất
latest_onefile_dir = None
latest_creation_time = 0
missingfiletext = "TDP-MissingFiles.log"
ProcessRunning = ""
pathnameInstall = ""

def Check_Files():        
    """Kiểm tra xem file tồn tại không nếu không thì báo lỗi và thoát chương trình"""
    # Danh sách các biến tập tin cần kiểm tra
    files_to_check = [
        file_icon,
        file_setup_driver_vi_6300,
        file_Uninstall_driver_vi_6300,
        file_setup_driver_en_6300,
        file_Uninstall_driver_en_6300,
        file_setup_driver_vi_2900,
        file_Uninstall_driver_vi_2900,
        file_setup_driver_en_2900,
        file_Uninstall_driver_en_2900,
        file_en,
        file_vi,
        icon_install,
        icon_change_language,
        icon_exit,
        icon_terminal,
        icon_info,
        icon_uninstall,
        icon_restart,
    ]

    # Kiểm tra sự tồn tại của các tập tin
    missing_files = [f for f in files_to_check if not os.path.isfile(f)]
    for missing_file in missing_files:
        if missing_files:
            class MissingFileError(wx.Dialog):
                def __init__(self, parent, message, timeout=7):
                    super(MissingFileError, self).__init__(parent, title=f"Closing in {timeout} seconds", size=(410, 255))
                    
                    self.timeout = timeout
                    self.remaining_time = timeout
                    
                    # Thiết lập giao diện
                    panel = wx.Panel(self)
                    vbox = wx.BoxSizer(wx.VERTICAL)

                    # Thêm một sizer để chứa biểu tượng và tin nhắn
                    hbox = wx.BoxSizer(wx.HORIZONTAL)

                    # Thêm biểu tượng lỗi
                    icon = wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_FRAME_ICON, (32, 32))
                    icon_bitmap = wx.StaticBitmap(panel, bitmap=icon)
                    hbox.Add(icon_bitmap, flag=wx.ALIGN_TOP | wx.RIGHT, border=10)

                    # Tin nhắn
                    message_label = wx.StaticText(panel, label=message, style=wx.ST_NO_AUTORESIZE)
                    hbox.Add(message_label, proportion=1, flag=wx.EXPAND)

                    vbox.Add(hbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
                    
                    # Nút OK có khoảng cách 5px với viền hộp thoại
                    ok_button = wx.Button(panel, label='OK')
                    ok_button.Bind(wx.EVT_BUTTON, self.on_close)
                    vbox.Add(ok_button, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)
                    
                    panel.SetSizer(vbox)
                    
                    # Thiết lập Timer
                    self.timer = wx.Timer(self)
                    self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

                def ShowModal(self):
                    # Phát âm thanh với luồng riêng biệt
                    sound_thread = threading.Thread(target=self.play_sound)
                    sound_thread.start()
                    self.timer.Start(1000)  # Mỗi giây cập nhật 1 lần
                    result = super(MissingFileError, self).ShowModal()
                    return result

                def play_sound(self):
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                def on_timer(self, event):
                    self.remaining_time -= 1
                    if self.remaining_time > -1:
                        self.SetTitle(f"Closing in {self.remaining_time} seconds")
                    else:
                        self.timer.Stop()
                        self.Close()

                def on_close(self, event):
                    self.timer.Stop()
                    self.Close()
                    sys.exit(0)

            # Tạo ứng dụng wxPython
            MissingFile = wx.App(False)

            # Tạo hộp thoại tự động đóng
            message = ("The program cannot be run because it is missing files that are important for operation! Exiting...\n\n"
                    "Chương trình không thể chạy được vì thiếu các tệp quan trọng để hoạt động! Đang thoát...\n\n"
                    "Bạn có thể xem các tệp thiếu bằng cách mở tệp tên là 'MissingFiles.log'.\n\n"
                    "You can view the missing files by opening the file named 'MissingFiles.log'.")
            
            now = datetime.now()
            datetime_str = now.strftime("%d/%m/%Y %H:%M:%S")
            with open (missingfiletext, 'a', encoding='utf-8') as file:
                file.write("\n"+str(datetime_str)+"          Missing files: \n")
                for missing_file in missing_files:
                    file.write(str(datetime_str)+ "          " + f"{missing_file}\n")

            # Hiển thị hộp thoại tự động đóng với tiêu đề cập nhật thời gian và biểu tượng lỗi
            dlg = MissingFileError(None, message=f"{message}")
            # Hiện dialog
            dlg.ShowModal()

            # Kết thúc ứng dụng
            dlg.Destroy()
            MissingFile.MainLoop()
            sys.exit(0)


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

        if cer_files:
            # Lấy file .crt và certutil.exe đầu tiên tìm được
            cer_file_path = cer_files[0]

            # Chạy lệnh certutil từ thư mục đã tìm thấy để thêm chứng chỉ vào kho lưu trữ Root
            certutil_command = f'cmd /c certutil -addstore "Root" "{cer_file_path}"'
            print(f"Đang chạy lệnh: {certutil_command}")

            # Sử dụng subprocess để chạy lệnh
            process = subprocess.run(certutil_command, shell=True)

            if process.returncode == 0:
                print("Chứng chỉ đã được thêm thành công vào kho lưu trữ Root.")
            else:
                print("Có lỗi xảy ra khi thêm chứng chỉ.")
        else:
            print("Không tìm thấy cả tệp chứng chỉ .crt và/hoặc certutil.exe trong thư mục gần nhất.")


# Khai báo các biến, library
file_icon = os.path.join('Icon', 'IconProgram.ico')
file_en = os.path.join('Languages', 'en.lng')
file_vi = os.path.join('Languages', 'vi.lng')
file_setup_driver_vi_6300 = os.path.join('LBP6300dn_R150_V110_W64_vi_VN_1', 'SetupDriver.exe')
file_Uninstall_driver_vi_6300 = os.path.join('LBP6300dn_R150_V110_W64_vi_VN_1', 'MISC', 'CNABBUND.exe')
file_setup_driver_en_6300 = os.path.join('LBP6300dn_R150_V110_W64_uk_EN_1', 'SetupDriver.exe')
file_Uninstall_driver_en_6300 = os.path.join('LBP6300dn_R150_V110_W64_uk_EN_1', 'MISC', 'CNABBUND.exe')
file_setup_driver_vi_2900 = os.path.join('LBP2900_R150_V330_W64_vi_VN_2', 'x64', 'SetupDriver.exe')
file_Uninstall_driver_vi_2900 = os.path.join('LBP2900_R150_V330_W64_vi_VN_2', 'x64', 'MISC', 'CNAB4UND.exe')
file_setup_driver_en_2900 = os.path.join('LBP2900_R150_V330_W64_uk_EN_2', 'x64', 'SetupDriver.exe')
file_Uninstall_driver_en_2900 = os.path.join('LBP2900_R150_V330_W64_uk_EN_2', 'x64', 'MISC', 'CNAB4UND.exe')
icon_install = os.path.join('Icon', 'install.png')
icon_change_language = os.path.join('Icon', 'change_language.png')
icon_exit = os.path.join('Icon', 'exit.png')
icon_terminal = os.path.join('Icon', 'terminal.png')
icon_info = os.path.join('Icon', 'info.png')
icon_uninstall = os.path.join('Icon', 'uninstall.png')
icon_vi = os.path.join('Icon', 'vi.png')
icon_us = os.path.join('Icon', 'us.png')
icon_restart = os.path.join('Icon', 'restart.png')
license_vi = os.path.join('License', 'LICENSE-vi')
license_en = os.path.join('License', 'LICENSE-en')
ProcessToCheck = None
# Định nghĩa các biến tập tin
file_ini_language = 'TDP-Config.json'
path_driver_select = 'TDP-PathDriver.json'
temp_path = os.getenv('TEMP')
lock_program = os.path.join(temp_path, 'Program.LCK')
driver_names = ["Canon LBP2900", "Canon LBP6300"]
DisableAllButton = False
DisableRestartButton = False
LockFile=True
bug_url = "https://github.com/TranPhuong319/ToolDriverPrinter/issues"
__version__ = '1.0.2'
# Đường dẫn đến thư mục hiện tại
src_base_path = os.getcwd()
deleteValueInstall = False
deleteValueUninstall = False
install_certificate()
Check_Files()

# Lấy đường dẫn đến thư mục temp
temp_folder_path = os.getenv('TEMP')

nameProcessInfo = [
    "Install",
    "Uninstall"
]

def WriteAceptedLicenseTerms():
    key_path = r"SOFTWARE\TDP"  # Đường dẫn khóa
    value_name = "AcceptLicenseTerms"  # Tên giá trị
    value_data = "Accepted"  # Dữ liệu giá trị
    value_type = winreg.REG_SZ  # Loại giá trị (chuỗi)

    try:
        # Tạo hoặc mở khóa Registry
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            # Đặt giá trị cho khóa
            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
    except PermissionError:
        print("Không đủ quyền để ghi vào Registry. Hãy chạy script với quyền quản trị.")


class AnotherProgramRunning(wx.Dialog):
    def __init__(self, parent, message, timeout=5):
        super().__init__(parent, title=f"Closing in {timeout} seconds", size=(410, 210))
                
        self.timeout = timeout
        self.remaining_time = timeout
        
        # Thiết lập giao diện
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Thêm một sizer để chứa biểu tượng và tin nhắn
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Thêm biểu tượng lỗi
        icon = wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_FRAME_ICON, (32, 32))
        icon_bitmap = wx.StaticBitmap(panel, bitmap=icon)
        hbox.Add(icon_bitmap, flag=wx.ALIGN_TOP | wx.RIGHT, border=10)

        # Tin nhắn
        message_label = wx.StaticText(panel, label=message, style=wx.ST_NO_AUTORESIZE)
        hbox.Add(message_label, proportion=1, flag=wx.EXPAND)

        vbox.Add(hbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        
        # Nút OK có khoảng cách 5px với viền hộp thoại
        ok_button = wx.Button(panel, label='OK')
        ok_button.Bind(wx.EVT_BUTTON, self.on_close)
        vbox.Add(ok_button, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)  # Thêm khoảng cách 5px

        panel.SetSizer(vbox)
        
        # Thiết lập Timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

    def ShowModal(self):
        # Start playing the sound in a separate thread
        sound_thread = threading.Thread(target=self.play_sound)
        sound_thread.start()
        self.timer.Start(1000)  # Mỗi giây cập nhật 1 lần
        result = super().ShowModal()
        return result

    def play_sound(self):
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                
    def on_timer(self, event):
        self.remaining_time -= 1
        if self.remaining_time > -1:
            self.SetTitle(f"Closing in {self.remaining_time} seconds")
        else:
            self.timer.Stop()
            self.Close()

    def on_close(self, event):
        self.timer.Stop()
        self.Close()

if os.path.exists(lock_program):
    try:
        os.remove(lock_program)  # Thử xóa file lock
        print(f"Xoá File lock {lock_program} thành công")
    except PermissionError:
        # Tạo ứng dụng wxPython
        AnotherAppRunning = wx.App(False)

        # Tạo hộp thoại tự động đóng
        message = ("Another program is running. Please close other programs before running.\n\n"
                        "Một chương trình khác đang được chạy. Vui lòng đóng chương trình khác trước khi chạy.")

        # Hiển thị hộp thoại tự động đóng với tiêu đề cập nhật thời gian và biểu tượng lỗi
        dlg = AnotherProgramRunning(None, message=f"{message}")

        # Show the dialog and start the timer
        dlg.ShowModal()

        # Kết thúc ứng dụng
        dlg.Destroy()
        AnotherAppRunning.MainLoop()
        sys.exit(0)

def CloseProgram():
    """Thực hiện các hành động sau khi cửa sổ được đóng."""
    global LockFile
    LockFile = False

    # Đợi thread hoàn tất
    lock_thread.join()

    # Xóa file khóa nếu tồn tại
    if os.path.exists(lock_program):
        os.remove(lock_program)

    # Thoát chương trình
    sys.exit(0)

def CheckSettingsFile():
    global deleteValueInstall
    
    # Kiểm tra xem file có tồn tại không
    if os.path.exists(path_driver_select):
        try:
            # Đọc dữ liệu từ file JSON
            with open(path_driver_select, 'r', encoding='utf-8') as file:
                SelectInstallDriver = json.load(file)
            
            global pathnameInstall
            # Lấy đường dẫn từ key 'InstallDriver'
            pathnameInstall = SelectInstallDriver.get('InstallDriver', "")
            
            # Kiểm tra nếu đường dẫn không đúng định dạng .exe thì set lại thành ""
            pattern = r'^[A-Za-z]:\\(?:[^\\\/:*?"<>|\r\n]+\\)*[^\\\/:*?"<>|\r\n]+\.(exe)$'
            if not re.match(pattern, pathnameInstall):
                pathnameInstall = ""
                SelectInstallDriver['InstallDriver'] = pathnameInstall
                
                # Lưu lại file JSON
                with open(path_driver_select, 'w', encoding='utf-8') as file:
                    json.dump(SelectInstallDriver, file, ensure_ascii=False, indent=4)
                deleteValueInstall = False
                return False

            # Nếu đúng định dạng, kiểm tra xem tệp có tồn tại không
            elif os.path.exists(pathnameInstall):
                deleteValueInstall = True
                return True
            else:
                # Nếu tệp không tồn tại, reset giá trị và set deleteValueInstall = False
                pathnameInstall = ""
                SelectInstallDriver['InstallDriver'] = pathnameInstall
                
                # Lưu lại file JSON
                with open(path_driver_select, 'w', encoding='utf-8') as file:
                    json.dump(SelectInstallDriver, file, ensure_ascii=False, indent=4)
                deleteValueInstall = False
                return False

        except Exception as e:
            print(e)
            deleteValueInstall = False
            return False
    else:
        print(f"File {path_driver_select} không tồn tại.")
        return False
    
def LicenseTermsCheck():
    key_path = r"SOFTWARE\TDP"  # Đường dẫn tới khóa
    value_name = "AcceptLicenseTerms"  # Tên giá trị cần kiểm tra

    try:
        # Mở khóa Registry
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            try:
                # Lấy giá trị trong Registry
                value, _ = winreg.QueryValueEx(key, value_name)
                if value == "Accepted":
                    print("Giá trị đã được chấp nhận, không cần hiển thị lại điều khoản.")
                    return  # Nếu giá trị là "Accepted", không làm gì thêm
                else:
                    print(f"Fail: Giá trị là '{value}' (không phải 'Accepted'). ")
                    # Nếu giá trị không phải "Accepted", hiển thị hộp thoại
            except FileNotFoundError:
                print(f"Không tìm thấy giá trị '{value_name}' trong khóa.")
                # Nếu không tìm thấy giá trị, hiển thị lại điều khoản
                pass  # Tiếp tục hiển thị hộp thoại
    except FileNotFoundError:
        print(f"Không tìm thấy khóa '{key_path}'.")
        # Nếu không tìm thấy khóa, hiển thị lại điều khoản
    except PermissionError:
        print("Không đủ quyền để truy cập Registry.")
        return

    # Nếu không có giá trị hoặc giá trị không phải "Accepted", hiển thị hộp thoạ
    Privacy = wx.App(False)
    dialog = PrivacyCheck(None, title="Terms of Use" if current_language == 'en' else 'Điều khoản sử dụng')
    dialog.Show()
    Privacy.MainLoop()
     
def CheckProcessRunning(path):
    try:
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            exe_path = proc.info.get('exe')
            name = proc.info.get('name')  # Lấy tên tiến trình
            
            # So khớp cả đường dẫn và tên file nếu cần
            if exe_path and exe_path.lower() == path.lower():
                return True
            elif name and name.lower() == os.path.basename(path).lower():
                return True
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass
    return False

# Tạo file lock mới để đánh dấu chương trình đang chạy
def create_lock_file():
    # Tạo tệp khóa mới để đánh dấu chương trình đang chạy
    with open(lock_program, 'w') as f:
        f.write("Program running...")

        # Khóa tệp
        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1024) 

        try:
            # Giữ tệp khóa mở khi LockFile là True
            while LockFile:
                time.sleep(1)
                pass  # Có thể thay thế bằng các thao tác khác nếu cần
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")
        finally:
            # Khi LockFile == False, tệp sẽ tự động đóng
            print("Khóa đã được gỡ bỏ.")


# Khởi động luồng để tạo tệp khóa
lock_thread = threading.Thread(target=create_lock_file)
lock_thread.start()

language_data = configparser.ConfigParser()
language, region = locale.getdefaultlocale()
substring = language[1:5] 

CheckSettingsFile() 

def read_language_from_json(file_path):
    """Đọc ngôn ngữ từ file JSON và trả về giá trị."""
    if not os.path.exists(file_path):
        print(f"File {file_path} không tồn tại.")
        return 'en'  # Mặc định nếu file không tồn tại

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Tải nội dung file JSON vào biến data
        current_language = data.get('current_language', 'en')  # Mặc định là 'en'
        return current_language
    
def restart_function():
    time.sleep(1)
    os.system("shutdown /r /t 0")

def restart_computer():
    # Tạo một luồng để khởi động lại
    thread = threading.Thread(target=restart_function)
    thread.start()

def detect_language():
    global current_language
    # Kiểm tra tệp cấu hình JSON có tồn tại không
    if os.path.exists(file_ini_language):
        try:
            with open(file_ini_language, 'r', encoding='utf-8') as configfile:
                config = json.load(configfile)
                
            # Đọc ngôn ngữ từ file JSON
            current_language = config.get('current_language', '')

            # Nếu ngôn ngữ trong file JSON không hợp lệ, tạo lại file
            if current_language not in ['vi', 'en']:
                raise ValueError("Ngôn ngữ không hợp lệ trong file JSON.")

        except (ValueError, FileNotFoundError, json.JSONDecodeError):
            # Nếu có lỗi khi đọc file JSON hoặc giá trị sai, ghi lại file
            print("Thông tin trong file JSON không chính xác, ghi lại file.")
            current_language = 'vi' if locale.getdefaultlocale()[0] == 'vi_VN' else 'en'
            write_json_file(current_language)

    else:
        # Nếu file JSON không tồn tại, xác định ngôn ngữ dựa trên hệ thống
        current_language = 'vi' if locale.getdefaultlocale()[0] == 'vi_VN' else 'en'

        # Ghi thông tin vào file JSON
        write_json_file(current_language)

def write_json_file(language):
    """Hàm ghi ngôn ngữ vào file JSON."""
    config = {
        'current_language': language,
    }
    with open(file_ini_language, 'w', encoding='utf-8') as configfile:
        json.dump(config, configfile, ensure_ascii=False, indent=4)

class PrivacyCheck(wx.Dialog):
    def __init__(self, parent, title):
        super(PrivacyCheck, self).__init__(parent, title=title, size=(500, 400))

        # Tạo panel chính
        panel = wx.Panel(self)

        # Tạo box sizer chính để chứa các thành phần
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Khung văn bản hiển thị nội dung License với Word Wrap để tự xuống dòng
        self.license_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP)
        vbox.Add(self.license_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Hiển thị nội dung từ file license
        self.load_license()

        # Tạo label để hỏi người dùng có đồng ý không
        question_label = wx.StaticText(panel, label="Do you agree to the terms of use?" if current_language == 'en' else 'Bạn có đồng ý với điều khoản sử dụng không?')
        vbox.Add(question_label, flag=wx.LEFT | wx.ALL, border=10)

        # Tạo box sizer để chứa các nút đồng ý và không đồng ý
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Thêm không gian linh hoạt để đẩy các nút sang phải
        hbox.AddStretchSpacer()

        # Nút "Không đồng ý"
        disagree_button = wx.Button(panel, label='Decline' if current_language == 'en' else 'Không đồng ý')
        hbox.Add(disagree_button, flag=wx.RIGHT, border=10)

        # Nút "Đồng ý"
        agree_button = wx.Button(panel, label='Accept'if current_language == 'en' else 'Đồng ý')
        hbox.Add(agree_button, flag=wx.RIGHT, border=10)

        # Thêm các nút vào sizer chính
        vbox.Add(hbox, flag=wx.EXPAND | wx.ALL, border=10)

        # Gắn panel vào sizer chính
        panel.SetSizer(vbox)

        # Liên kết sự kiện cho các nút
        agree_button.Bind(wx.EVT_BUTTON, self.on_agree)
        disagree_button.Bind(wx.EVT_BUTTON, self.on_disagree)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Đặt focus vào nút "Đồng ý"
        agree_button.SetFocus()

    def load_license(self):
        """Đọc nội dung từ file license và hiển thị vào TextCtrl."""
        try:
            with open(license_en if current_language == 'en' else license_vi, 'r', encoding='utf-8') as file:
                self.license_text.SetValue(file.read())

        except FileNotFoundError:
            self.license_text.SetValue("Không tìm thấy file license.")

    def on_agree(self, event):
        self.Destroy()
        WriteAceptedLicenseTerms()

    def on_disagree(self, event):
        """Xử lý khi người dùng chọn không đồng ý."""
        self.Destroy()  # Đảm bảo cửa sổ bị đóng trước
        CloseProgram()

    def on_close(self, event):
        """Xử lý khi người dùng nhấn nút đóng cửa sổ."""
        self.Destroy()  # Đảm bảo cửa sổ bị đóng trước
        CloseProgram()

def CheckProcessDriver(process_list):
    global ProcessToCheck
    # Lặp qua danh sách các tiến trình (Install, Uninstall)
    for process in process_list:
        if process == "Uninstall":
            if os.path.exists("C:\\CNTemp\\CNABBUND.INI"):
                ProcessToCheck = "Uninstall"
                break
            else:
                ProcessToCheck = None
        
        elif process == "Install":
            if os.path.exists("C:\\Program Files\\Canon\\InstTemp\\SetupUIK.dll"):
                try:
                    os.remove("C:\\Program Files\\Canon\\InstTemp\\SetupUIK.dll")
                except PermissionError:
                    ProcessToCheck = "Install"
                    break
            else:
                ProcessToCheck = None
        else:
            ProcessToCheck = None

def DisableButtonRestart():
    global DisableRestartButton  # Sử dụng biến toàn cục DisableRestartButton
    if DisableRestartButton:  # Kiểm tra nếu DisableRestartButton là True
        wx.MessageBox(  # Hiển thị hộp thoại lỗi
            language_data['Text_Messagebox']['cannotRestart'],  # Thông báo lỗi
            language_data['title_messagebox']['Title_Messagebox-error'],  # Tiêu đề hộp thoại
            wx.OK | wx.ICON_ERROR  # Thông báo dạng lỗi
        )
        return False  # Trả về False, ngừng tiếp tục thực hiện
    return True  # Nếu không có lỗi, trả về True

def DisableAllButtons():
    global DisableAllButton, DisableRestartButton
    DisableRestartButton = True
    DisableAllButton = True
    try:
        install_button.Disable()
        uninstall_button.Disable()
        if 'install_lang_button' in globals():
            if deleteValueInstall == False:
                try:
                    install_lang_button.Disable()
                except Exception as e:
                    print("Error: ", e)
    except:
        pass

def EnableAllButtons():
    global DisableAllButton, DisableRestartButton
    DisableRestartButton = False
    DisableAllButton = False
    try:
        install_button.Enable()
        uninstall_button.Enable()
        if 'install_lang_button' in globals():
            if deleteValueInstall == False:
                install_lang_button.Enable()
    except:
        pass

class ChoiceDriverInstall(wx.Dialog):
    def __init__(self, parent, current_language, *args, **kw):
        super(ChoiceDriverInstall, self).__init__(parent, *args, **kw)
        self.current_language = current_language  # Sử dụng current_language đã truyền vào

        self.SetSize((320, 150))
        self.SetTitle(language_data['Title_Program']['Title_select_driver'])
        self.Center()

        # Disable resizing and maximize box
        self.SetWindowStyle(wx.DEFAULT_DIALOG_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.text_display = wx.StaticText(panel, label=language_data['Text_Dialog']['SelectDriverInstall'], style=wx.ALIGN_CENTER)
        self.text_display.Wrap(280)
        vbox.Add(self.text_display, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.lbp6300 = wx.Button(panel, label="Canon LBP6300")
        self.lbp2900 = wx.Button(panel, label="Canon LBP2900")
        hbox.Add(self.lbp6300, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(self.lbp2900, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(hbox, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.lbp6300.Bind(wx.EVT_BUTTON, self.Canon_LBP6300)
        self.lbp2900.Bind(wx.EVT_BUTTON, self.Canon_LBP2900)

    def Canon_LBP6300(self, event):
        setup_file = file_setup_driver_vi_6300 if self.current_language == "vi" else file_setup_driver_en_6300
        wx.CallAfter(self.StartInstallation, setup_file)
        wx.CallAfter(self.Destroy)

    def Canon_LBP2900(self, event):
        setup_file = file_setup_driver_vi_2900 if self.current_language == "vi" else file_setup_driver_en_2900
        wx.CallAfter(self.StartInstallation, setup_file)
        wx.CallAfter(self.Destroy)

    def StartInstallation(self, setup_file):
        DisableAllButtons()
        with wx.ProgressDialog(language_data['Title_Program']['Title_install'], language_data['Text_Dialog']['LoadingDriverInstall'], maximum=100, style=wx.PD_APP_MODAL | wx.PD_SMOOTH) as dlg:
            time.sleep(1)
            def run():
                try:
                    process = subprocess.Popen([setup_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    process.wait()
                    wx.CallAfter(EnableAllButtons)
                except Exception as e:
                    wx.CallAfter(wx.MessageBox,
                        f"An error occurred during installation:\n{e}",
                        "Error",
                        wx.OK | wx.ICON_ERROR
                    )
                    wx.CallAfter(EnableAllButtons)
            threading.Thread(target=run, daemon=True).start()

def SelectDriverInstall(current_language):
    dialog = ChoiceDriverInstall(None, current_language=current_language)
    dialog.ShowModal()
    dialog.Destroy()

class ChoiceDriverUninstall(wx.Dialog):
    def __init__(self, parent, current_language, *args, **kw):
        super(ChoiceDriverUninstall, self).__init__(parent, *args, **kw)
        self.current_language = current_language  # Sử dụng current_language đã truyền vào

        self.SetSize((340, 150))
        self.SetTitle(language_data['Title_Program']['Title_select_driver'])
        self.Center()

        # Disable resizing and maximize box
        self.SetWindowStyle(wx.DEFAULT_DIALOG_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.text_display = wx.StaticText(panel, label=language_data['Text_Dialog']['SelectDriverUninstall'], style=wx.ALIGN_CENTER)
        self.text_display.Wrap(280)
        vbox.Add(self.text_display, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.lbp6300 = wx.Button(panel, label="Canon LBP6300")
        self.lbp2900 = wx.Button(panel, label="Canon LBP2900")
        hbox.Add(self.lbp6300, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(self.lbp2900, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(hbox, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.lbp6300.Bind(wx.EVT_BUTTON, self.Canon_LBP6300)
        self.lbp2900.Bind(wx.EVT_BUTTON, self.Canon_LBP2900)

    def Canon_LBP6300(self, event):
        Uninstall_file = file_Uninstall_driver_vi_6300 if self.current_language == "vi" else file_Uninstall_driver_en_6300
        wx.CallAfter(self.StartUninstallation, Uninstall_file)
        wx.CallAfter(self.Destroy)

    def Canon_LBP2900(self, event):
        Uninstall_file = file_Uninstall_driver_vi_2900 if self.current_language == "vi" else file_Uninstall_driver_en_2900
        wx.CallAfter(self.StartUninstallation, Uninstall_file)
        wx.CallAfter(self.Destroy)

    def StartUninstallation(self, Uninstall_file):
        DisableAllButtons()
        with wx.ProgressDialog(language_data['Title_Program']['Title_install'], language_data['Text_Dialog']['LoadingDriverUninstall'], maximum=100, style=wx.PD_APP_MODAL | wx.PD_SMOOTH) as dlg:
            time.sleep(1)
            def run():
                try:
                    process = subprocess.Popen([Uninstall_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    process.wait()
                    wx.CallAfter(EnableAllButtons)
                except Exception as e:
                    wx.CallAfter(wx.MessageBox,
                        f"An error occurred during uninstallation:\n{e}",
                        "Error",
                        wx.OK | wx.ICON_ERROR
                    )
                    wx.CallAfter(EnableAllButtons)
            threading.Thread(target=run, daemon=True).start()

def SelectDriverUninstall(current_language):
    dialog = ChoiceDriverUninstall(None, current_language=current_language)
    dialog.ShowModal()
    dialog.Destroy()

class InstallLanguageDialog(wx.Dialog):
    def __init__(self, printer_name, *args, **kw):
        super(InstallLanguageDialog, self).__init__(None, title="Cài đặt ngôn ngữ cho trình điều khiển cho máy in Canon", size=(400, 210))

        self.printer_name = printer_name
        self.Center()

        # Disable thu phóng và cực đại hoá
        self.SetWindowStyle(wx.DEFAULT_DIALOG_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        # Tạo một bảng điều khiển để chứa các thành phần giao diện
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Tạo các nút
        self.lbp6300 = wx.RadioButton(panel, label="Cài đặt LBP6300")
        self.lbp2900 = wx.RadioButton(panel, label="Cài đặt LBP2900")
        vbox.Add(self.lbp6300, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.lbp2900, flag=wx.LEFT | wx.TOP, border=10)

        # Tạo chữ tĩnh và set ở giữa
        self.log = wx.StaticText(panel, label="", style=wx.ALIGN_CENTER)
        self.log.Wrap(360)  
        vbox.Add(self.log, proportion=1, flag=wx.EXPAND | wx.TOP, border=20)
        
        # Tạo thanh tiến trình ở giữa
        self.gauge = wx.Gauge(panel, range=100, size=(360, 25), style=wx.GA_HORIZONTAL)
        vbox.Add(self.gauge, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=10)

        # Tạo nút Cài đặt và để nó ở giữa
        self.install_button = wx.Button(panel, label="Cài đặt")
        vbox.Add(self.install_button, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        # Gán nút vào lệnh
        self.install_button.Bind(wx.EVT_BUTTON, self.OnInstall)

    def OnInstall(self, event):
        driver_choice = None
        if self.lbp6300.GetValue():
            driver_choice = "Canon LBP6300"
        elif self.lbp2900.GetValue():
            driver_choice = "Canon LBP2900"
        else:
            wx.MessageBox('Vui lòng chọn một tùy chọn.', 'Thông báo', wx.OK | wx.ICON_WARNING)
            return

        wx.CallLater(500, self.StartInstallation, driver_choice)

    def StartInstallation(self, driver_choice):
        self.gauge.SetValue(0)
        self.UpdateLog("Đang bắt đầu cài đặt ngôn ngữ...")
        
        self.Disable()
        
        thread = threading.Thread(target=self.InstallDriver, args=(driver_choice,))
        thread.start()

    def InstallDriver(self, driver_choice):
        Check_Files()
        DisableAllButtons()
        self.install_button.Disable()
        try:
            if driver_choice == "Canon LBP2900":
                # Tạo thư mục sao lưu nếu chưa tồn tại
                backup_dir = ".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup"
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                # Tạo một danh sách các tệp cần sao lưu, xóa và sao chép
                files_to_backup = [
                    "CNAB4PMD.DLL", "CNAB4SWD.EXE", "CNAB4UND.DLL", "CNAB4UND.EXE", 
                    "CNAB4809.DLL", "CPC1UKA4.DLL", "CPC10DA4.EXE", "CPC10EA4.DLL", 
                    "CPC10SA4.DLL", "CPC10VA4.EXE"
                ]
                files_to_delete = [
                    "CNAB4PMD.DLL", "CNAB4SWD.EXE", "CNAB4UND.DLL", "CNAB4UND.EXE", 
                    "CNAB4809.DLL", "CPC1UKA4.DLL", "CPC10EA4.DLL", "CPC10SA4.DLL", 
                    "CPC10VA4.EXE", "CNAB4UND.EXE", "CNAB4UND.DLL"
                ]
                files_to_copy = [
                    "CNAB4PMD.DLL", "CNAB4SWD.EXE", "CNAB4UND.DLL", "CNAB4UND.EXE", 
                    "CNAB4809.DLL", "CPC1UKA4.DLL", "CPC10EA4.DLL", "CPC10SA4.DLL", 
                    "CPC10VA4.EXE", "CNAB4UND.DLL", "CNAB4UND.EXE"
                ]

                # Định nghĩa các bước với các tệp được sao lưu, xóa và sao chép
                steps = [
                    ("Đang dừng tác vụ...", [
                        "taskkill /F /IM CNAB4SWK.EXE > NUL 2>&1",
                        "taskkill /F /IM CNAB4LAD.EXE > NUL 2>&1",
                        "taskkill /F /IM CNAB4RPD.EXE > NUL 2>&1",
                        "taskkill /F /IM CPC10DA4.EXE > NUL 2>&1",
                        "taskkill /F /IM CPC10VA4.EXE > NUL 2>&1",
                    ]),
                    ("Đang sao lưu các tệp...", [
                        f"xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\{file}\" .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup\\" 
                        for file in files_to_backup
                    ]),
                    ("Đang xóa các tệp cũ...", [
                        f"del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\{file}\""
                        for file in files_to_delete
                    ]),
                    ("Đang sao chép các tệp mới...", [
                        f"xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\{file}\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\""
                        for file in files_to_copy
                    ])
                ]

            elif driver_choice == "Canon LBP6300":
                # Tạo thư mục sao lưu nếu chưa tồn tại
                backup_dir = ".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup"
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                # Cập nhật các danh sách tệp cho Canon LBP6300
                files_to_backup = [
                    "PCL5ERES.DLL", "CNABBUND.DLL", "CNABBSTD.DLL", "CNABBM.DLL",
                    "CNAP2NSD.DLL", "CNABBPMK.DLL", "CNABB809.DLL", "CPC10SAK.DLL",
                    "CPC10EAK.DLL", "CNXPCP32.DLL"
                ]
                files_to_delete = [
                    "PCL5ERES.DLL", "CNABBUND.DLL", "CNABBSTD.DLL", "CNABBM.DLL", 
                    "CNAP2NSD.DLL", "CNABBPMK.DLL", "CNABB809.DLL", "CPC10SAK.DLL",
                    "CPC10EAK.DLL", "CNXPCP32.DLL"
                ]
                files_to_copy = [
                    "PCL5ERES.DLL", "CNABBUND.DLL", "CNABBSTD.DLL", "CNABBM.DLL",
                    "CNAP2NSD.DLL", "CNABBPMK.DLL", "CNABB809.DLL", "CPC10SAK.DLL",
                    "CPC10EAK.DLL", "CNXPCP32.DLL"
                ]
                
                # Định nghĩa các bước với các tệp được sao lưu, xóa và sao chép
                steps = [
                    ("Đang dừng tác vụ...", [
                        "taskkill /F /IM CNABBSWK.EXE > NUL 2>&1",
                        "taskkill /F /IM CNAP2LAK.EXE > NUL 2>&1",
                        "taskkill /F /IM CNAP2RPK.EXE > NUL 2>&1",
                    ]),
                    ("Đang sao lưu các tệp...", [
                        f"xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\{file}\" .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup\\" 
                        for file in files_to_backup
                    ]),
                    ("Đang xóa các tệp cũ...", [
                        f"del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\{file}\""
                        for file in files_to_delete
                    ]),
                    ("Đang sao chép các tệp mới...", [
                        f"xcopy /Y \".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\{file}\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\""
                        for file in files_to_copy
                    ])
                ]

            step_count = len(steps)
            for i, (step_description, commands) in enumerate(steps):
                self.UpdateLog(step_description)
                for command in commands:
                    subprocess.run(command, shell=True)
                wx.CallAfter(self.UpdateGauge, int((i + 1) / step_count * 100))

            self.UpdateLog("Cài đặt hoàn tất.")
            time.sleep(1)
            # Gọi destroy sau khi chạy xong
            wx.CallAfter(self.Destroy)
            global DisableRestartButton
            DisableRestartButton = False
            command_restart()
        except Exception as e:
            self.UpdateLog(f"Lỗi: {e}")
            wx.CallAfter(EnableAllButtons)
        finally:
            # Bật lại tất cả các nút sau khi chạy xong
            wx.CallAfter(EnableAllButtons)
    def UpdateGauge(self, value):
        self.gauge.SetValue(value)

    def UpdateLog(self, message):
        wx.CallAfter(self.log.SetLabel, message)
        wx.CallAfter(self.log.GetParent().Layout)

def Install_driver_vietnam_dialog():
    dialog = InstallLanguageDialog(None)
    dialog.ShowModal()
    dialog.Destroy()

time.sleep(0.3)

detect_language()

LicenseTermsCheck()

def load_language(current_language):
    Check_Files()
    global language_data, panel
    file_path = os.path.join('Languages',  f'{current_language}.lng')
    if os.path.exists(file_path):
        confirm_Change_Language = wx.MessageBox(
        language_data['Text_Messagebox']['confirm-change-language'],
        language_data['title_messagebox']['Title_Messagebox-yesno'],
        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
    )
        if confirm_Change_Language == wx.YES:
            file_path = os.path.join('Languages', f'{current_language}.lng')
            config = configparser.ConfigParser()
            with open(file_path, 'r', encoding='utf-8') as file:
                config.read_file(file)
            language_data = config
            update_config_language(current_language, file_ini_language)

            # Xoá tất cả object cũ để cập nhật object mới
            for child in frame.GetChildren():
                child.Destroy()

            # Tạo panel and sizer
            panel = wx.Panel(frame)
            vbox = wx.BoxSizer(wx.VERTICAL)

            frame.SetSize((250, 200) if current_language == "vi" else (230, 165))
            frame_title = language_data['Title_Program']['Title']  # Đặt title từ file lng
            frame.SetTitle(frame_title)
            
            try:
                # Tạo menu và nút nhấn
                create_menu_bar()
                create_buttons(current_language)
                if current_language == 'vi':
                    if deleteValueInstall == True:
                        install_lang_button.Disable()
            except Exception as e:
                wx.MessageBox(
                            f"An error occurred while switching languages.\n {e} Exiting...",
                            "Error!",
                            wx.OK | wx.NO_DEFAULT | wx.ICON_ERROR
                )
                
                CloseProgram()

            frame.Layout()
            frame.Refresh()
            if DisableAllButton == True:
                DisableAllButtons()
            else:
                try:
                    wx.CallAfter(EnableAllButtons)
                except:
                    pass

        else:
            notification.notify(
                title=language_data['title_messagebox']['Title_Messagebox-info'],
                message=language_data['Text_Messagebox']['cancel_action'],
                app_icon=file_icon,
                timeout=2, # Thời gian để hiển thị Thông báo
            )

    else:
        if current_language == "vi":
            wx.MessageBox(
                f"The language you selected cannot be displayed due to missing files: {file_vi}",
                language_data['title_messagebox']['Title_Messagebox-error'],
                wx.OK | wx.ICON_ERROR
            )
        else:
            wx.MessageBox(
                f"Ngôn ngữ bạn chọn không thể hiển thị do thiếu tệp: {file_en}",
                language_data['title_messagebox']['Title_Messagebox-error'],
                wx.OK | wx.ICON_ERROR
            )

def create_menu_bar():
    """Tạo thanh menu dựa vào ngôn ngữ hiện tại"""
    Check_Files()
    menu_bar = wx.MenuBar()
    file_menu = wx.Menu()
    ManualSelectExe = wx.Menu()  # Tạo một menu con cho "Change EXE"
    help_menu = wx.Menu()

    # Resize hình ảnh
    def load_and_resize_image(path, size):
        try:
            image = wx.Image(path, wx.BITMAP_TYPE_PNG)
            image = image.Rescale(*size)
            return wx.Bitmap(image)
        except Exception as e:
            return wx.Bitmap()  #

    # Set kích cỡ của Icon
    icon_size = (16, 16)
    icon_size_vi = (24, 16)
    icon_size_us = (25, 16)  

    # Load và resize hình ảnh
    lang_icon = load_and_resize_image(icon_change_language, icon_size)
    english_icon = load_and_resize_image(icon_us, icon_size_us)
    vietnamese_icon = load_and_resize_image(icon_vi, icon_size_vi)
    exit_icon = load_and_resize_image(icon_exit, icon_size)
    about_icon = load_and_resize_image(icon_info, icon_size)
    restart_icon = load_and_resize_image(icon_restart, icon_size)

    # Menu chọn ngôn ngữ
    file_submenu = wx.Menu()
    current_language = read_language_from_json(file_ini_language)
    
    if current_language == 'vi':
        english_item = file_submenu.Append(wx.ID_ANY, "English")
        english_item.SetBitmap(english_icon)
        file_submenu.Bind(wx.EVT_MENU, lambda evt: load_language('en'), english_item)
    elif current_language == 'en':
        vietnamese_item = file_submenu.Append(wx.ID_ANY, "Vietnamese")
        vietnamese_item.SetBitmap(vietnamese_icon)
        file_submenu.Bind(wx.EVT_MENU, lambda evt: load_language('vi'), vietnamese_item)

    InstallSelectManual = ManualSelectExe.Append(wx.ID_ANY, language_data['Menu_Program']['ActionInstallSelect'])
    ManualSelectExe.Bind(wx.EVT_MENU, DialogSelectManualInstall, InstallSelectManual)
    UninstallSelectManual = ManualSelectExe.Append(wx.ID_ANY, language_data['Menu_Program']['ActionUninstallSelect'])
    ManualSelectExe.Bind(wx.EVT_MENU, DialogSelectManualUninstall, UninstallSelectManual)    

    lang_submenu_item = file_menu.AppendSubMenu(file_submenu, language_data['Menu_Program']['menuChangeLanguage'])
    lang_submenu_item.SetBitmap(lang_icon)
    file_menu.AppendSeparator()
    changeExe = file_menu.AppendSubMenu(ManualSelectExe, language_data['Menu_Program']['menuManualSelectFile'])
    file_menu.AppendSeparator()
    restart_item = file_menu.Append(wx.ID_ANY, language_data['Menu_Program']['menuRestartComputer'])
    restart_item.SetBitmap(restart_icon)
    frame.Bind(wx.EVT_MENU, Restart_Computer_function)
    file_menu.AppendSeparator()
    exit_item = file_menu.Append(wx.ID_EXIT, language_data['Menu_Program']['menuExit'])
    exit_item.SetBitmap(exit_icon)
    frame.Bind(wx.EVT_MENU, on_exit, exit_item)

    menu_bar.Append(file_menu, language_data['Menu_Program']['menuFile'])

    about_item = help_menu.Append(wx.ID_ABOUT, language_data['Menu_Program']['menuAbout'])
    about_item.SetBitmap(about_icon)
    frame.Bind(wx.EVT_MENU, on_about, about_item)

    menu_bar.Append(help_menu, language_data['Menu_Program']['menuHelp'])

    frame.SetMenuBar(menu_bar)

def create_buttons(current_language):
    """Tạo các nút nhấn dựa vào ngôn ngữ hiện tại"""
    Check_Files()
    global deleteValueInstall
    if frame.GetChildren():
        frame.GetChildren()[0].Destroy()

    panel = wx.Panel(frame)
    vbox = wx.BoxSizer(wx.VERTICAL)

    def load_and_resize_image(path, size):
        try:
            image = wx.Image(path, wx.BITMAP_TYPE_PNG)
            image = image.Rescale(*size)
            return wx.Bitmap(image)
        except Exception as e:
            return wx.Bitmap()  

    # Resize icon
    icon_size = (16, 16) 

    # Load và resize icon
    install_icon = load_and_resize_image(icon_install, icon_size)
    uninstall_icon = load_and_resize_image(icon_uninstall, icon_size)
    lang_icon = load_and_resize_image(icon_terminal, icon_size)

    # Tọ button kièm icon
    global install_button
    install_button = wx.Button(panel, label=language_data['Text_Button']['Button_Install_text'])
    install_button.SetBitmap(install_icon)
    install_button.Bind(wx.EVT_BUTTON, Install_Driver)
    vbox.Add(install_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

    global install_lang_button

    if current_language == 'vi':
        install_lang_button = wx.Button(panel, label=language_data['Text_Button']['Install_Language_Vietnam'])
        install_lang_button.SetBitmap(lang_icon)
        install_lang_button.Bind(wx.EVT_BUTTON, Install_language_vietnam_driver)
        vbox.Add(install_lang_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        if deleteValueInstall == True:
            install_lang_button.Disable()
        else:
            install_lang_button.Enable()

    global uninstall_button
    uninstall_button = wx.Button(panel, label=language_data['Text_Button']['Button_Uninstall_text'])
    uninstall_button.SetBitmap(uninstall_icon)
    uninstall_button.Bind(wx.EVT_BUTTON, Uninstall_Driver)
    vbox.Add(uninstall_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

    panel.SetSizer(vbox)
    panel.Layout()
    frame.Layout()
    frame.Refresh()

def are_drivers_installed(driver_names):
    try:
        # Chạy lệnh để lấy danh sách các driver máy in đã cài đặt
        result = subprocess.run(['wmic', 'printer', 'get', 'drivername'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Chia kết quả đầu ra thành các dòng và lọc bỏ các dòng trống
        driver_list = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        
        # Kiểm tra xem tất cả các driver mục tiêu có nằm trong danh sách driver đã cài đặt không
        all_drivers_installed = all(
            any(name.lower() in driver_name.lower() for driver_name in driver_list)
            for name in driver_names
        )
        
        return all_drivers_installed
    except Exception as e:
        print(f"Error: {e}")
        return False

driver_names = ["Canon LBP6300", "Canon LBP2900"]

def Uninstall_Driver(event):
    """
    Gỡ cài đặt driver máy in Canon.
    """
    Check_Files()
    current_language = read_language_from_json(file_ini_language)
    DisableAllButtons()

    def uninstall_thread():
        try:
            if are_drivers_installed(driver_names):
                wx.CallAfter(lambda: SelectDriverUninstall(current_language))
            elif are_drivers_installed("Canon LBP6300"):
                if current_language == "vi":
                    Uninstall_file = file_Uninstall_driver_vi_6300                
                else:
                    Uninstall_file = file_Uninstall_driver_en_6300

                    # Khởi chạy tiến trình con
                process = subprocess.Popen([Uninstall_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

                    # Hàm đọc và in dòng ra màn hình trong thời gian thực
                def read_stream(stream, label):
                    for line in iter(stream.readline, ''):
                        print(f"{label}: {line.strip()}")
                    stream.close()

                # Tạo luồng đọc stdout và stderr
                stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, "STDOUT"))
                stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, "STDERR"))

                # Bắt đầu các luồng
                stdout_thread.start()
                stderr_thread.start()

                # Đợi tiến trình kết thúc
                process.wait()

                # Đợi các luồng hoàn thành
                stdout_thread.join()
                stderr_thread.join()

            elif are_drivers_installed("Canon LBP2900"):
                if current_language == "vi":
                    Uninstall_file = file_Uninstall_driver_vi_2900                
                else:
                    Uninstall_file = file_Uninstall_driver_en_2900
                
                # Khởi chạy tiến trình con
                process = subprocess.Popen([Uninstall_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
                # Hàm đọc và in dòng ra màn hình trong thời gian thực
                def read_stream(stream, label):
                    for line in iter(stream.readline, ''):
                        print(f"{label}: {line.strip()}")
                    stream.close()

                # Tạo luồng đọc stdout và stderr
                stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, "STDOUT"))
                stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, "STDERR"))

                # Bắt đầu các luồng
                stdout_thread.start()
                stderr_thread.start()

                # Đợi tiến trình kết thúc
                process.wait()

                # Đợi các luồng hoàn thành
                stdout_thread.join()
                stderr_thread.join()
            else:
                wx.MessageBox(
                        language_data['Text_Messagebox']['not_install_driver'],
                        language_data['title_messagebox']['Title_Messagebox-error'],
                        wx.OK | wx.ICON_ERROR
                    )
        except Exception as e:
            wx.MessageBox(
                f"{language_data['Text_Messagebox']['unknown_error']}\n{e}",
                language_data['title_messagebox']['Title_Messagebox-error'],
                wx.OK | wx.ICON_ERROR
            )
        finally:
            wx.CallAfter(EnableAllButtons)

    uninstall_driver_thread = threading.Thread(target=uninstall_thread)
    uninstall_driver_thread.start()

def Install_Driver(event):
    """Cài đặt driver Canon"""
    
    def install_thread():
        try:
            Check_Files()
            # Đọc lại cấu hình để cập nhật ngôn ngữ
            current_language = read_language_from_json(file_ini_language)
            wx.CallAfter(lambda: SelectDriverInstall(current_language))
        except Exception as e:
            wx.CallAfter(wx.MessageBox,
                f"{language_data['Text_Messagebox']['unknown_error']}\n{e}",
                language_data['title_messagebox']['Title_Messagebox-error'],
                wx.OK | wx.ICON_ERROR
            )
        finally:
            wx.CallAfter(EnableAllButtons)

    if not pathnameInstall:
        threading.Thread(target=install_thread, daemon=True).start()
    else:
        class ManualDriverInstall(threading.Thread):
            def __init__(self, finishCommandInstall=None):
                super().__init__(daemon=True)
                self.finishCommandInstall = finishCommandInstall

            def run(self):
                try:
                    DisableAllButtons()
                    process = subprocess.Popen(
                        [pathnameInstall],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    print("Running Process...")
                    stdout, stderr = process.communicate()
                    if process.returncode == 0:
                        print(f"Process completed successfully:\n{stdout}")
                    else:
                        print(f"Process failed with error:\n{stderr}")
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    if self.finishCommandInstall:
                        wx.CallAfter(self.finishCommandInstall)  # Gọi callback khi hoàn tất

        def commandOnFinishInstall():
            """Callback thực hiện sau khi thread hoàn tất."""
            EnableAllButtons()

        try:
            DisableAllButtons()
            # Tạo và chạy thread, truyền callback vào
            thread = ManualDriverInstall(finishCommandInstall=commandOnFinishInstall)
            thread.start()
        except Exception as e:
            wx.MessageBox(
                f"Đã xảy ra lỗi khi cố gắng chạy chương trình: {e}" if current_language == 'vi' else f"An error occurred while trying to run the program: {e}",
                "Lỗi" if current_language == 'vi' else "Error",
                wx.OK | wx.ICON_ERROR
            )

def Install_language_vietnam_driver(event):
    """Cài đặt ngôn ngữ Việt"""
    DisableAllButtons()
    Check_Files()

    # Kiểm tra các driver đã cài đặt
    lbp6300_installed = are_drivers_installed("Canon LBP6300")
    lbp2900_installed = are_drivers_installed("Canon LBP2900")

    installed_drivers = []

    if lbp6300_installed:
        installed_drivers.append("Canon LBP6300")
    if lbp2900_installed:
        installed_drivers.append("Canon LBP2900")

    # Nếu không có driver nào được cài đặt
    if not installed_drivers:
        wx.MessageBox(
            language_data['Text_Messagebox']['not_install_driver'],
            language_data['title_messagebox']['Title_Messagebox-error'],
            wx.OK | wx.ICON_ERROR
        )
        wx.CallAfter(EnableAllButtons)
        return

    # Mở hộp thoại cài đặt
    try:
        if len(installed_drivers) == 1:
            # Nếu chỉ có 1 driver, tự động chọn nó và bắt đầu cài đặt
            selected_driver = installed_drivers[0]
            dialog = InstallLanguageDialog(None, selected_driver=selected_driver)
            dialog.StartInstallation(selected_driver)

        else:
            # Nếu có nhiều driver, hiển thị hộp thoại chọn driver
            Install_driver_vietnam_dialog()
            EnableAllButtons()
    except Exception as e:
        wx.MessageBox(
            f"{language_data['Text_Messagebox']['unknown_error']}\n{e}",
            language_data['title_messagebox']['Title_Messagebox-error'],
            wx.OK | wx.ICON_ERROR
        )  
    finally:
        EnableAllButtons()

class SelectManualDriverInstall(wx.Dialog):
    def __init__(self, parent, title, current_language):
        super(SelectManualDriverInstall, self).__init__(parent, title=title, size=(450, 160))

        panel = wx.Panel(self)
        self.current_language = current_language

        # Tạo text
        text = wx.StaticText(panel, label=language_data['Text_Dialog']['InfoManualSelect'], pos=(10, 10))

        # Tạo đường dẫn (ô dòng đơn - single line)
        self.text_path = wx.TextCtrl(panel, pos=(25, 45), size=(240, 22), style=wx.TE_READONLY)
        self.text_path.SetHint(language_data['LabelGUI']['PathManualDriver'])

        # Kiểm tra và load file json nếu tồn tại
        if os.path.exists(path_driver_select):
            try:
                with open(path_driver_select, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    InstallPath = data.get('InstallDriver', "")
                    self.text_path.SetValue(InstallPath)
            except Exception as e:
                print(e)

        # Tạo nút Browse
        browse_button = wx.Button(panel, label=language_data['Text_Button']['BrowseFileDriver'], pos=(270, 45), size=(70, 25))
        browse_button.Bind(wx.EVT_BUTTON, self.onBrowse)
        
        # Tạo nút Delete Value
        delete_button = wx.Button(panel, label=language_data['Text_Button']['DeleteValue'], pos=(343, 45), size=(88, 25))
        delete_button.Bind(wx.EVT_BUTTON, self.Delete_value)

        # Tạo nút OK
        ok_button = wx.Button(panel, label="OK" if current_language == 'en' else 'Đồng ý' , pos=(352, 92), size=(73, 24))
        self.Bind(wx.EVT_BUTTON, self.OnOK, ok_button)

    def Delete_value(self, event):
        self.text_path.SetValue("")

    def onBrowse(self, event):
        current_language = read_language_from_json(file_ini_language)
        try:
            # Tạo hộp thoại chọn file .exe
            with wx.FileDialog(self, language_data['Title_Program']['DialogSelectManualInstall'], wildcard="Executable files (*.exe)|*.exe",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # Người dùng đã hủy, thoát ra.

                global pathnameInstall
                # Lấy đường dẫn của file được chọn
                pathnameInstall = fileDialog.GetPath()

                # Kiểm tra nếu tệp tồn tại
                if not os.path.exists(pathnameInstall):
                    if  current_language == 'vi':
                        wx.MessageBox(f"Tệp không tồn tại: {pathnameInstall}", "Lỗi", wx.ICON_ERROR)
                    else: 
                        wx.MessageBox(f"File not found: {pathnameInstall}", "Error", wx.ICON_ERROR)
                    return

                # Hiển thị đường dẫn trong ô line
                self.text_path.SetValue(pathnameInstall)
                
                global SelectInstallDriver
                # Cập nhật đường dẫn vào dictionary
                SelectInstallDriver = {
                    'InstallDriver': pathnameInstall  # Sử dụng str thay vì set
                }
        except Exception as e:
            wx.MessageBox(f"An error occurred while selecting a file: {str(e)}", "Lỗi", wx.ICON_ERROR)

    def OnOK(self, event):
        current_language = read_language_from_json(file_ini_language)
        try:
            # Lấy đường dẫn từ ô text
            pathnameInstall = self.text_path.GetValue()

            # Cập nhật đường dẫn vào file JSON
            if pathnameInstall or pathnameInstall == "": 
                SelectInstallDriver = {
                    'InstallDriver': pathnameInstall  # Sử dụng str thay vì set
                }
                
                # Ghi lại file JSON sau khi cập nhật
                with open(path_driver_select, 'w', encoding='utf-8') as json_file:
                    json.dump(SelectInstallDriver, json_file, ensure_ascii=False, indent=4)

                # Khóa nút install_lang_button nếu có đường dẫn hợp lệ
                if not pathnameInstall == "" and os.path.exists(pathnameInstall) and current_language == 'vi':
                    install_lang_button.Disable()
                else:
                    try:
                        if current_language == "vi":
                            install_lang_button.Enable()
                    except Exception as e:
                        print(e)
                if not pathnameInstall == "":
                    wx.MessageBox(f"Đã lưu đường dẫn: {pathnameInstall}" if current_language == 'vi' else f"Saved path: {pathnameInstall}", "Thông báo" if current_language == "vi" else "Infomation", wx.ICON_INFORMATION)
                else:
                    wx.MessageBox(f"Đã xóa đường dẫn." if current_language == 'vi' else "Deleted Directory", "Thông báo" if current_language == "vi" else "Infomation", wx.ICON_INFORMATION)
            else:
                wx.MessageBox("Đường dẫn không tồn tại hoặc trống." if current_language == "vi" else "Path does not exist or is empty.", "Lỗi" if current_language == 'vi' else 'Error', wx.ICON_ERROR)

            self.Close()

        except Exception as e:
            print(e)

def DialogSelectManualInstall(event):
    current_language = read_language_from_json(file_ini_language)
    if DisableAllButton == True:
        wx.MessageBox(
            "This option cannot be selected while installing/uninstalling a driver." if current_language == 'en' else 'Không thể chọn tuỳ chọn này khi đang cài đặt / gỡ cài đặt trình điều khiển.',
            "Error!" if current_language == 'en' else 'Lỗi!',
            wx.OK | wx.ICON_ERROR  # Thông báo dạng lỗi
        )
        return
    dialog=SelectManualDriverInstall(None, title=language_data['Title_Program']['SelectManualDriver'], current_language=current_language)
    dialog.ShowModal()
    dialog.Destroy()

def DialogSelectManualUninstall(event):
    current_language = read_language_from_json(file_ini_language)
    if DisableAllButton == True:
        wx.MessageBox(
            "This option cannot be selected while installing/uninstalling a driver." if current_language == 'en' else 'Không thể chọn tuỳ chọn này khi đang cài đặt / gỡ cài đặt trình điều khiển.',
            "Error!" if current_language == 'en' else 'Lỗi!',
            wx.OK | wx.ICON_ERROR  # Thông báo dạng lỗi
        )
        return



def update_config_language(new_language, config_file_path):
    """Cập nhật ngôn ngữ mới vào file JSON."""
    
    Check_Files() 
    
    # Kiểm tra xem file JSON có tồn tại không
    if not os.path.exists(config_file_path):
        # Nếu không tồn tại, tạo file JSON mới và ghi giá trị mặc định là 'en'
        with open(config_file_path, 'w', encoding='utf-8') as config_file:
            json.dump({"current_language": "en"}, config_file, ensure_ascii=False, indent=4)

    # Đọc file JSON hiện có
    with open(config_file_path, 'r', encoding='utf-8') as config_file:
        config_data = json.load(config_file)  # Tải nội dung file JSON vào biến
    
    # Cập nhật ngôn ngữ mới
    config_data["current_language"] = new_language
    
    # Ghi lại các thay đổi vào file JSON
    with open(config_file_path, 'w', encoding='utf-8') as config_file:
        json.dump(config_data, config_file, ensure_ascii=False, indent=4)

class LicenseFrame(wx.Frame):
    def __init__(self, parent, title, license_file_path):
        super(LicenseFrame, self).__init__(parent, title=title, size=(400, 300))

        self.license_file_path = license_file_path 

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        scrolled_window = wx.ScrolledWindow(panel, size=(380, 280))
        scrolled_window.SetScrollRate(20, 20)
        vbox_scrolled = wx.BoxSizer(wx.VERTICAL)

        # Set kích thước tối thiểu cho cửa sổ license
        self.SetMinSize((300, 250))

        Check_Files()
        try:
            with open(self.license_file_path, 'r', encoding='utf-8') as file:
                license_text = file.read()
        except Exception as e:
            license_text = f"Could not load license file: {str(e)}"


        text_ctrl = wx.TextCtrl(scrolled_window, value=license_text, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_BESTWRAP)
        vbox_scrolled.Add(text_ctrl, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        scrolled_window.SetSizer(vbox_scrolled)

        vbox.Add(scrolled_window, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        
        btn_ok = wx.Button(panel, label='OK')
        btn_ok.Bind(wx.EVT_BUTTON, self.OnClose)
        vbox.Add(btn_ok, flag=wx.ALIGN_RIGHT | wx.ALL, border=5) 

        panel.SetSizer(vbox)

        self.SetIcon(wx.Icon(file_icon))  # Set icon cửa sổ license

    def OnClose(self, event):
        self.Close()

class About(wx.Dialog):
    def __init__(self, parent, current_language, title, file_icon, license_file_path):
        super(About, self).__init__(parent, title=title, size=(420, 222))

        self.license_file_path = license_file_path

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Load và resize icon
        icon_img = wx.Image(file_icon, wx.BITMAP_TYPE_ANY)
        icon_img = icon_img.Scale(50, 50, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(icon_img))

        # Chỉnh chữ bên phải Icon
        text_vbox = wx.BoxSizer(wx.VERTICAL)

        # Text content based on language
        if current_language == "vi":
            label_about1 = f"Công cụ cài đặt trình điều khiển máy in Canon.\nPhiên bản v.{__version__}\nCopyright ©️ 2023-2025 TranPhuong319. Mọi quyền được bảo lưu."
            label_about2 = "\nTrình điều khiển máy in Canon.\nCopyright ©️ 2009-2012 Canon Inc. Mọi quyền được bảo lưu."
        else:
            label_about1 = f"Canon printer driver installation tool.\nVersion v.{__version__}\nCopyright ©️ 2023-2025 TranPhuong319. All rights reserved."
            label_about2 = "\nCanon Driver.\nCopyright ©️ 2009-2012 Canon Inc. All rights reserved."

        web = "https://github.com/TranPhuong319/ToolDriverPrinter/"

        
        text1 = wx.StaticText(panel, wx.ID_ANY, label_about1)
        text_vbox.Add(text1, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=5)

        # Thêm block văn bản cạnh biểu tượng
        website_link = wx.adv.HyperlinkCtrl(panel, wx.ID_ANY, web)
        text_vbox.Add(website_link, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=5)

        # Add the second block of text under the link
        text2 = wx.StaticText(panel, wx.ID_ANY, label_about2)
        text_vbox.Add(text2, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=5)

        hbox.Add(bitmap, flag=wx.ALL, border=5)
        hbox.Add(text_vbox, proportion=1, flag=wx.EXPAND)

        vbox.Add(hbox, flag=wx.ALL | wx.EXPAND, border=5)

        # Add các icon như OK, Cancel, License
        hbox_btn = wx.BoxSizer(wx.HORIZONTAL)

        # License button on the far left
        btn_license = wx.Button(panel, label=language_data['Text_Button']['LicenseButton'])  # Add License button
        btn_license.Bind(wx.EVT_BUTTON, self.show_license_action)  # Bind event for License button
        hbox_btn.Add(btn_license, flag=wx.ALL, border=5)  # License button on the far left

        # Thêm khoảng cách nút License
        hbox_btn.AddStretchSpacer()

        # Add nút report
        btn_report = wx.Button(panel, label=language_data['Text_Button']['ButtonBug'])  # Add Report button
        btn_report.Bind(wx.EVT_BUTTON, self.report_bug_action)  # Bind event for Report button
        hbox_btn.Add(btn_report, flag=wx.ALL, border=5)

        btn_ok = wx.Button(panel, wx.ID_OK, label='OK' if current_language == 'en' else 'Đồng ý')
        btn_ok.Bind(wx.EVT_BUTTON, self.OkButton)
        hbox_btn.Add(btn_ok, flag=wx.ALL, border=5)
        self.SetAffirmativeId(wx.ID_OK) 
        btn_ok.SetFocus()  

        vbox.Add(hbox_btn, flag=wx.EXPAND | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def report_bug_action(self, event):
        """Mở web báo lỗi chương trình"""
        webbrowser.open(bug_url)

    def show_license_action(self, event):
        """Hiện license dựa triên ngôn ngữ"""
        current_language = read_language_from_json(file_ini_language)
        if (os.path.exists(license_vi) and current_language == 'vi') or (os.path.exists(license_en) and current_language == 'en'):
            license_frame = LicenseFrame(self, title=language_data['Title_Program']['LicenseFrame'], license_file_path=self.license_file_path)
            license_frame.Show()
        else:
            wx.MessageBox(
                "Could not load license file because is missing!" if current_language == 'en' else "Không thể đọc tệp License do tệp không tồn tại!",
                "Error!" if current_language == 'en' else "Lỗi",
                wx.OK | wx.ICON_ERROR
        )

    def OkButton(self, event):
        self.Destroy()

def on_about(event):
    Check_Files()
    try:
        current_language = read_language_from_json(file_ini_language)
        if current_language == "vi":
            title = "Giới thiệu"
        else:
            title = "About"
        licenseFile = license_vi if current_language == 'vi' else license_en
        dialog = About(frame, current_language, title, file_icon, licenseFile)
        dialog.ShowModal()
        try:
            dialog.Destroy()
        except:
            pass
    except Exception as e:
        frame.Destroy()
        wx.MessageBox(
            f"{language_data['Text_Messagebox']['unknown_error']}\n{e}.\n{'Exiting...'}",
            language_data['title_messagebox']['Title_Messagebox-error'],
            wx.OK | wx.ICON_ERROR
        )
        wx.CallAfter(sys.exit)

def command_restart():
    """Khởi động lại máy tính"""
    if not DisableButtonRestart():
        return  # Thoát khi bị lỗi

    confirm_restart_pc = wx.MessageBox(
                        language_data['Text_Messagebox']['confirm_restart_pc'],
                        language_data['title_messagebox']['Title_Messagebox-yesno'],
                        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
    )
    if confirm_restart_pc == wx.YES:
        restart_computer()
        CloseProgram()

def Restart_Computer_function(event):
    """Khởi động lại máy tính qua nút nhấn"""
    if not DisableButtonRestart():
        return  # Thoát khi bị lỗi

    confirm_restart_pc = wx.MessageBox(
                        language_data['Text_Messagebox']['confirm_restart_pc'],
                        language_data['title_messagebox']['Title_Messagebox-yesno'],
                        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
    )
    if confirm_restart_pc == wx.YES:
        restart_computer()
        CloseProgram()

def on_exit(event):
    """Đóng chương trình"""
    # Kiểm tra trạng thái trước khi đóng
    global pathnameInstall
    pathnameInstall = os.path.abspath(pathnameInstall)
    print(pathnameInstall)
    print(CheckProcessRunning(pathnameInstall))
    if deleteValueInstall == True:
        if CheckProcessRunning(pathnameInstall):
            messageClosingError()
            return
        else:
            CloseProgram()
    else:
        CheckProcessDriver(nameProcessInfo)
    if ProcessToCheck == "Install" or ProcessToCheck == "Uninstall":
        messageClosingError()
    else:
        CloseProgram()

class window(wx.App):
    def OnInit(self):
        global frame
        global current_language
        # Xác định kích thước cửa sổ dựa trên ngôn ngữ
        window_size = (250, 200) if current_language == "vi" else (230, 165)

        # Tạo cửa sổ chính với kích thước đã xác định
        frame = wx.Frame(None, 
                 title=language_data['Title_Program']['Title'],
                 style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX),
                 size=window_size)
        frame.Bind(wx.EVT_CLOSE, on_closing)

        if os.path.exists(file_icon):
            frame.SetIcon(wx.Icon(file_icon))
        try:
            create_menu_bar()
        except Exception as e:
            wx.MessageBox(
                        f"{language_data['Text_Messagebox']['CannotLoadProgram']}\n {e}\nExiting...",
                        "Error!",
                        wx.OK | wx.ICON_ERROR
            )
            CloseProgram()

        create_buttons(current_language)

        frame.Show()
        return True

def messageClosingError():
            wx.MessageBox(
                language_data['Text_Messagebox']['not_close_window'],
                language_data['title_messagebox']['Title_Messagebox-warning'],
                wx.OK | wx.ICON_WARNING
            )

def on_closing(event):
    """Đóng chương trình bằng nút X"""
    # Kiểm tra trạng thái trước khi đóng
    global pathnameInstall
    pathnameInstall = os.path.abspath(pathnameInstall)
    print(pathnameInstall)
    print(CheckProcessRunning(pathnameInstall))
    if deleteValueInstall == True:
        if CheckProcessRunning(pathnameInstall):
            messageClosingError()
            return
        else:
            CloseProgram()
    else:
        CheckProcessDriver(nameProcessInfo)
    if ProcessToCheck == "Install" or ProcessToCheck == "Uninstall":
        messageClosingError()
    else:
        CloseProgram()
          
detect_language()

with open(f'Languages\{current_language}.lng', 'r', encoding='utf-8') as file:
    language_data.read_file(file)

TDP = window()
TDP.MainLoop()