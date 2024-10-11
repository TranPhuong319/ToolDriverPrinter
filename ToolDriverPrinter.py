# -*- coding: utf-8 -*-
# Printer driver installation tool
# Copyright ©️ 2023-2024 TranPhuong319
# Version 1.0.2
# Compile by Nuitka
import configparser; import os; import subprocess; import sys; import webbrowser; import wx.adv; import glob; import tempfile; from datetime import datetime
import wx ; import msvcrt ; import locale ; import psutil; import shutil; import threading; import time; import winsound; from plyer import notification; import fnmatch # Nhập thư viện cần thiết

# Thay đổi thư mục làm việc thành thư mục chứa tệp chạy
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# Định nghĩa các biến tập tin
file_icon = os.path.join('Icon', 'IconProgram.ico')
file_en = os.path.join('Languages', 'en.lng')
file_vi = os.path.join('Languages', 'vi.lng')
file_setup_driver_vi_6300 = os.path.join('LBP6300dn_R150_V110_W64_vi_VN_1', 'SetupDriver.exe')
file_Uninstall_driver_vi_6300= os.path.join('LBP6300dn_R150_V110_W64_vi_VN_1', 'MISC', 'CNABBUND.exe')
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
process_name_to_check_install = "SetupDriver.exe"
process_name_to_check_Uninstall = "CNABBUND.exe"
process_name_to_check_Uninstall_2900 = "CNAB4UND.exe"
file_ini = 'Config.ini'
settings_file = 'settings.ini'
restart_computer = 'shutdown -r -t 00'
temp_path = os.getenv('TEMP')
lock_program = os.path.join(temp_path, 'Program.LOCK')
driver_names = ["Canon LBP2900", "Canon LBP6300"]
DisableAllButton = False
DisableRestartButton = False
LockFile=True
bug_url = "https://github.com/TranPhuong319/ToolDriverPrinter/issues"
license_vi = os.path.join('License', 'LICENSE-vi')
license_en = os.path.join('License', 'LICENSE-en')
__version__ = '1.0.2.0'
# Đường dẫn đến thư mục hiện tại
src_base_path = os.getcwd()
deleteValueInstall = False
deleteValueUninstall = False

# Lấy đường dẫn đến thư mục temp
temp_folder_path = os.getenv('TEMP')

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
            def __init__(self, parent, message, timeout=5):
                super(MissingFileError, self).__init__(parent, title=f"Closing in {timeout} seconds", size=(410, 250))
                
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
                # Start playing the sound in a separate thread
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
                sys.exit()

        # Tạo ứng dụng wxPython
        MissingFile = wx.App(False)

        # Tạo hộp thoại tự động đóng
        message = (f"The program cannot be run because it is missing files that are important for operation! Exiting...\n\n"
                f"Chương trình không thể chạy được vì thiếu các tệp quan trọng để hoạt động! Đang thoát...\n\n"
                f"Missing File:\n{missing_file}")

        # Hiển thị hộp thoại tự động đóng với tiêu đề cập nhật thời gian và biểu tượng lỗi
        dlg = MissingFileError(None, message=f"{message}")
        # Show the dialog and start the timer
        dlg.ShowModal()

        # Kết thúc ứng dụng
        dlg.Destroy()
        MissingFile.MainLoop()
        sys.exit()

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
        print(f"Lock file '{lock_program}' removed successfully.")
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
        sys.exit()


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
config = configparser.ConfigParser()

language, region = locale.getdefaultlocale()
substring = language[1:5] 

if os.path.exists(settings_file):
    try:
        global InstallPath
        InstallPath = config.get('DriverSelectPath', 'InstallDriver')
    except:
        pass

def detect_language():
    global current_language
    # Xác định ngôn ngữ dựa trên file hệ thống hoặc ngôn ngữ máy
    language = locale.getdefaultlocale()[0]  # Lấy ngôn ngữ của hệ thống (e.g., 'vi_VN' hoặc 'en_US')

    # Kiểm tra tệp ini có tồn tại không
    if os.path.exists(file_ini):
        config.read(file_ini)

        try:
            # Đọc ngôn ngữ từ file ini
            current_language = config.get('Language', 'current_language')

            # Nếu ngôn ngữ trong file ini không hợp lệ, tạo lại file
            if current_language not in ['vi', 'en']:
                raise ValueError("Ngôn ngữ không hợp lệ trong file ini.")

        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            # Nếu có lỗi khi đọc file ini hoặc giá trị sai, ghi lại file ini
            print("Thông tin trong file ini không chính xác, ghi lại file.")
            current_language = 'vi' if language == 'vi_VN' else 'en'
            write_ini_file(current_language)

    else:
        # Nếu file ini không tồn tại, xác định ngôn ngữ dựa trên file ngôn ngữ hoặc hệ thống
        if os.path.exists(file_en) and (language == 'vi_VN' or not os.path.exists(file_vi)):
            current_language = 'vi' if language == 'vi_VN' else 'en'
        elif os.path.exists(file_en):
            current_language = 'en'
        elif os.path.exists(file_vi):
            current_language = 'vi'
        else:
            # Mặc định nếu không có file ngôn ngữ nào
            current_language = 'en'

        # Ghi thông tin vào file ini
        write_ini_file(current_language)

def write_ini_file(language):
    """Hàm ghi ngôn ngữ vào file ini"""
    config['Language'] = {
        'current_language': language,
    }
    with open(file_ini, 'w') as configfile:
        config.write(configfile)

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
            with open(r"License\LICENSE-en" if current_language == 'en' else r"License\LICENSE-vi", 'r', encoding='utf-8') as file:
                self.license_text.SetValue(file.read())

        except FileNotFoundError:
            self.license_text.SetValue("Không tìm thấy file license.")

    def on_agree(self, event):
        self.Destroy()

    def on_disagree(self, event):
        self.Destroy()
        global LockFile
        LockFile = False
        lock_thread.join()
        os.remove(lock_program)
        sys.exit()
    def on_close(self, event):
        """Xử lý khi người dùng nhấn nút đóng cửa sổ."""
        self.Destroy()
        global LockFile
        LockFile = False
        lock_thread.join()
        os.remove(lock_program)
        sys.exit()

def DisableButtonRestart():
    global DisableRestartButton
    if DisableRestartButton:
        wx.MessageBox(
            language_data['Text_Messagebox']['cannotRestart'],
            language_data['title_messagebox']['Title_Messagebox-error'],
            wx.OK | wx.ICON_ERROR
        )
        return False  # Indicate that an error occurred
    return True  # Indicate that it's safe to proceed

def DisableAllButtons():
    global DisableAllButton, DisableRestartButton
    DisableRestartButton = True
    DisableAllButton = True
    try:
        install_button.Disable()
        uninstall_button.Disable()
        if 'install_lang_button' in globals():
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
            install_lang_button.Enable()
    except:
        pass

class ChoiceDriverInstall(wx.Dialog):
    def __init__(self, parent, current_language, *args, **kw):
        super(ChoiceDriverInstall, self).__init__(parent, *args, **kw)
        self.current_language = current_language  # Sử dụng current_language đã truyền vào
        print(f"[DEBUG] current_language in ChoiceDriverInstall: {self.current_language}")  # Debugging

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
        print(f"[DEBUG] Canon_LBP6300 current_language: {self.current_language}")
        setup_file = file_setup_driver_vi_6300 if self.current_language == "vi" else file_setup_driver_en_6300
        print(f"[DEBUG] Setup file chosen: {setup_file}")
        wx.CallAfter(self.StartInstallation, setup_file)
        wx.CallAfter(self.Destroy)

    def Canon_LBP2900(self, event):
        print(f"[DEBUG] Canon_LBP2900 current_language: {self.current_language}")
        setup_file = file_setup_driver_vi_2900 if self.current_language == "vi" else file_setup_driver_en_2900
        print(f"[DEBUG] Setup file chosen: {setup_file}")
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
                        f"Đã xảy ra lỗi trong quá trình cài đặt:\n{e}",
                        "Lỗi",
                        wx.OK | wx.ICON_ERROR
                    )
                    wx.CallAfter(EnableAllButtons)
            threading.Thread(target=run, daemon=True).start()



def SelectDriverInstall(current_language):
    print(f"[DEBUG] current_language at start: {current_language}")
    dialog = ChoiceDriverInstall(None, current_language=current_language)
    dialog.ShowModal()
    dialog.Destroy()

class ChoiceDriverUninstall(wx.Dialog):
    def __init__(self, parent, current_language, *args, **kw):
        super(ChoiceDriverUninstall, self).__init__(parent, *args, **kw)
        self.current_language = current_language  # Sử dụng current_language đã truyền vào
        print(f"[DEBUG] current_language in ChoiceDriverUninstall: {self.current_language}")  # Debugging

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
        print(f"[DEBUG] Canon_LBP6300 current_language: {self.current_language}")
        Uninstall_file = file_Uninstall_driver_vi_6300 if self.current_language == "vi" else file_Uninstall_driver_en_6300
        print(f"[DEBUG] Setup file chosen: {Uninstall_file}")
        wx.CallAfter(self.StartUninstallation, Uninstall_file)
        wx.CallAfter(self.Destroy)

    def Canon_LBP2900(self, event):
        print(f"[DEBUG] Canon_LBP2900 current_language: {self.current_language}")
        Uninstall_file = file_Uninstall_driver_vi_2900 if self.current_language == "vi" else file_Uninstall_driver_en_2900
        print(f"[DEBUG] Setup file chosen: {Uninstall_file}")
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
                        f"Đã xảy ra lỗi:\n{e}",
                        "Lỗi",
                        wx.OK | wx.ICON_ERROR
                    )
                    wx.CallAfter(EnableAllButtons)
            threading.Thread(target=run, daemon=True).start()

def SelectDriverUninstall(current_language):
    print(f"[DEBUG] current_language at start: {current_language}")
    dialog = ChoiceDriverUninstall(None, current_language=current_language)
    dialog.ShowModal()
    dialog.Destroy()

class InstallLanguageDialog(wx.Dialog):
    def __init__(self, printer_name, *args, **kw):
        super(InstallLanguageDialog, self).__init__(None, title="Cài đặt ngôn ngữ cho trình điều khiển cho máy in Canon", size=(400, 210))

        self.printer_name = printer_name
        self.Center()

        # Disable resizing and maximize box
        self.SetWindowStyle(wx.DEFAULT_DIALOG_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        # Create a panel to contain the interface elements
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create radio buttons
        self.lbp6300 = wx.RadioButton(panel, label="Cài đặt LBP6300")
        self.lbp2900 = wx.RadioButton(panel, label="Cài đặt LBP2900")
        vbox.Add(self.lbp6300, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.lbp2900, flag=wx.LEFT | wx.TOP, border=10)

        # Create a StaticText with centered alignment
        self.log = wx.StaticText(panel, label="", style=wx.ALIGN_CENTER)
        self.log.Wrap(360)  
        vbox.Add(self.log, proportion=1, flag=wx.EXPAND | wx.TOP, border=20)
        
        # Create a Gauge with centered alignment
        self.gauge = wx.Gauge(panel, range=100, size=(360, 25), style=wx.GA_HORIZONTAL)
        vbox.Add(self.gauge, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=10)

        # Create the install button and center it
        self.install_button = wx.Button(panel, label="Cài đặt")
        vbox.Add(self.install_button, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        # Bind the button click event
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
        recheck_and_set_new_dir()
        DisableAllButtons()
        self.install_button.Disable()
        try:
            if driver_choice == "Canon LBP2900":
                steps = [
                            ("Đang dừng tác vụ...", [
                                "taskkill /F /IM CNAB4SWK.EXE > NUL 2>&1",
                                "taskkill /F /IM CNAB4LAD.EXE > NUL 2>&1",
                                "taskkill /F /IM CNAB4RPD.EXE > NUL 2>&1",
                                "taskkill /F /IM CPC10DA4.EXE > NUL 2>&1",
                                "taskkill /F /IM CPC10VA4.EXE > NUL 2>&1",
                            ]),
                            ("Đang sao lưu các tệp...", [
                                "if exist .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup rd /s /q .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup > NUL 2>&1",
                                "mkdir .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup",
                                "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAB4PMD.DLL\" .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup\\",
                                "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAB4SWD.EXE\" .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup\\",
                                "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAB4UND.DLL\" .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup\\",
                                "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAB4UND.EXE\"   .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup\\",
                                "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAB4809.DLL\" .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup\\",
                                "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC1UKA4.DLL\" .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup\\",
                                "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC10DA4.EXE\" .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup\\",
                                "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC10EA4.DLL\" .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup\\",
                                "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC10SA4.DLL\" .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup\\",
                                "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC10VA4.EXE\" .\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\Backup\\",
                            ]),
                            ("Đang xóa các tệp cũ...", [
                                "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAB4PMD.DLL\" ",
                                "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAB4SWD.EXE\" ",
                                "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAB4UND.DLL\" ",
                                "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAB4UND.EXE\" ",
                                "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAB4809.DLL\" ",
                                "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC1UKA4.DLL\" ",
                                "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC10EA4.DLL\" ",
                                "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC10SA4.DLL\" ",
                                "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC10VA4.EXE\" ",
                                "del /s /q \"C:\\Program Files\\Canon\\PrnUninstall\\Canon LBP2900\\CNAB4UND.EXE\" ",
                                "del /s /q \"C:\\Program Files\\Canon\\PrnUninstall\\Canon LBP2900\\CNAB4UND.DLL\" ",
                            ]),
                            ("Đang sao chép các tệp mới...", [
                                "xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\CNAB4PMD.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                                "xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\CNAB4SWD.EXE\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                                "xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\CNAB4UND.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                                "xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\CNAB4UND.EXE\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                                "xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\CNAB4809.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                                "xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\CPC1UKA4.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                                "xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\CPC10EA4.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                                "xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\CPC10SA4.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                                "xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\CPC10VA4.EXE\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                                "xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\CNAB4UND.DLL\" \"C:\\Program Files\\Canon\\PrnUninstall\\Canon LBP2900\\\"",
                                "xcopy /Y \".\\LBP2900_R150_V330_W64_vi_VN_2\\x64\\MISC\\DLL_Vietnam\\CNAB4UND.EXE\" \"C:\\Program Files\\Canon\\PrnUninstall\\Canon LBP2900\\\"",
                            ])
                        ]
                
            elif driver_choice == "Canon LBP6300":
                steps = [
                    ("Đang dừng tác vụ...", [
                        "taskkill /F /IM CNABBSWK.EXE > NUL 2>&1",
                        "taskkill /F /IM CNAP2LAK.EXE > NUL 2>&1",
                        "taskkill /F /IM CNAP2RPK.EXE > NUL 2>&1",
                    ]),
                    ("Đang sao lưu các tệp...", [
                        "if exist .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup rd /s /q .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup > NUL 2>&1",
                        "mkdir .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup",
                        "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\PCL5ERES.DLL\" .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup\\",
                        "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNABBUND.DLL\" .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup\\",
                        "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNABBSTD.DLL\" .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup\\",
                        "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNABBM.DLL\"   .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup\\",
                        "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAP2NSD.DLL\" .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup\\",
                        "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNABBPMK.DLL\" .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup\\",
                        "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNABB809.DLL\" .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup\\",
                        "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC10SAK.DLL\" .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup\\",
                        "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC10EAK.DLL\" .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup\\",
                        "xcopy /Y \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNXPCP32.DLL\" .\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\Backup\\",
                    ]),
                    ("Đang xóa các tệp cũ...", [
                        "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\PCL5ERES.DLL\" ",
                        "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNABBUND.DLL\" ",
                        "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNABBSTD.DLL\" ",
                        "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNABBM.DLL\" ",
                        "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNAP2NSD.DLL\" ",
                        "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNABBPMK.DLL\" ",
                        "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNABB809.DLL\" ",
                        "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC10SAK.DLL\" ",
                        "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CPC10EAK.DLL\" ",
                        "del /s /q \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\CNXPCP32.DLL\" ",
                    ]),
                    ("Đang sao chép các tệp mới...", [
                        "xcopy /Y \".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\PCL5ERES.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                        "xcopy /Y \".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\CNABBUND.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                        "xcopy /Y \".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\CNABBSTD.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                        "xcopy /Y \".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\CNABBM.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                        "xcopy /Y \".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\CNAP2NSD.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                        "xcopy /Y \".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\CNABBPMK.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                        "xcopy /Y \".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\CNABB809.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                        "xcopy /Y \".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\CPC10SAK.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                        "xcopy /Y \".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\CPC10EAK.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                        "xcopy /Y \".\\LBP6300dn_R150_V110_W64_vi_VN_1\\MISC\\DLL_Vietnam\\CNXPCP32.DLL\" \"C:\\Windows\\System32\\spool\\drivers\\x64\\3\\\"",
                    ])
                ]

            # Execute each step
            step_count = len(steps)
            for i, (step_description, commands) in enumerate(steps):
                self.UpdateLog(step_description)
                for command in commands:
                    subprocess.run(command, shell=True)
                wx.CallAfter(self.UpdateGauge, int((i + 1) / step_count * 100))

            self.UpdateLog("Cài đặt hoàn tất.")
            time.sleep(1)
                        # Ensure to call Destroy from the main thread
            wx.CallAfter(self.Destroy)
            confirm_restart_pc = wx.MessageBox(
                        language_data['Text_Messagebox']['confirm_restart_pc'],
                        language_data['title_messagebox']['Title_Messagebox-yesno'],
                        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
            )
            
            if confirm_restart_pc == wx.YES:
                subprocess.run(restart_computer, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
                sys.exit()
            wx.CallAfter(EnableAllButtons)
        except Exception as e:
            self.UpdateLog(f"Lỗi: {e}")
            wx.CallAfter(EnableAllButtons)
        finally:
            # Re-enable the dialog after installation is complete
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

class CopyFilesDialog(wx.Frame):
    def __init__(self, parent, total_files):
        super().__init__(parent, style=wx.STAY_ON_TOP | wx.NO_BORDER | wx.FRAME_SHAPED | wx.FRAME_NO_TASKBAR)
        
        # Tạo panel và sizer chính
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Tạo sizer ngang cho icon và văn bản
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Thay đổi kích thước của icon và hiển thị
        icon_img = wx.Image(file_icon, wx.BITMAP_TYPE_ICO)
        icon_img = icon_img.Scale(40, 40, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.Bitmap(icon_img)
        self.static_bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, bitmap)
        self.h_sizer.Add(self.static_bitmap, 0, wx.ALL, 10)
        
        # Thêm văn bản
        self.message = wx.StaticText(self.panel, label="Loading, Please wait... \n\nĐang khởi động, Vui lòng chờ...")
        self.h_sizer.Add(self.message, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        # Thêm sizer ngang vào sizer chính
        self.sizer.Add(self.h_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # Thêm sizer ngang cho thanh tiến trình và phần trăm
        self.progress_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Thêm thanh tiến trình
        self.progress_bar = wx.Gauge(self.panel, range=total_files, size=(200, 17), style=wx.GA_HORIZONTAL)
        self.progress_sizer.Add(self.progress_bar, 1, wx.ALL | wx.EXPAND, 5)

        # Tạo StaticText để hiển thị phần trăm
        self.percent_text = wx.StaticText(self.panel, label="0%")
        self.progress_sizer.Add(self.percent_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Thêm sizer tiến trình vào sizer chính
        self.sizer.Add(self.progress_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # Thiết lập sizer cho panel
        self.panel.SetSizer(self.sizer)
        self.SetSize((272, 134))  # Điều chỉnh kích thước của hộp thoại 
        self.Fit()
        self.Center()

    def update_progress(self, value):
        self.progress_bar.SetValue(value)
        percent = (value / self.progress_bar.GetRange()) * 100  # Tính phần trăm
        self.percent_text.SetLabel(f"{int(percent)}%")  # Cập nhật phần trăm hiển thị

def count_total_files(folders, src_base_path):
    total_files = 0
    for folder in folders:
        folder_path = os.path.join(src_base_path, folder)
        for root, dirs, files in os.walk(folder_path):
            total_files += len(files)
    return total_files

def copy_folders(folders, src_base_path, dst_base_path, dialog):
    total_files_copied = 0
    for folder in folders:
        src_folder_path = os.path.join(src_base_path, folder)
        dst_folder_path = os.path.join(dst_base_path, folder)
        try:
            if not os.path.exists(dst_folder_path):
                os.makedirs(dst_folder_path)
            
            print(f"Copying folder: {folder}")  # In ra tên thư mục đang sao chép
            
            for root, dirs, files in os.walk(src_folder_path):
                for dir_name in dirs:
                    src_dir = os.path.join(root, dir_name)
                    dst_dir = os.path.join(dst_folder_path, os.path.relpath(src_dir, src_folder_path))
                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir)
                
                for file_name in files:
                    src_file = os.path.join(root, file_name)
                    dst_file = os.path.join(dst_folder_path, os.path.relpath(src_file, src_folder_path))

                    # In thông tin tệp để đảm bảo rằng tệp đang được xử lý
                    print(f"Copying file: {src_file} to {dst_file}")
                    
                    shutil.copy2(src_file, dst_file)
                    total_files_copied += 1
                    wx.CallAfter(dialog.update_progress, total_files_copied)
        except Exception as e:
            print(f"Error while copying folder {folder}: {e}")
    
    time.sleep(1)
    wx.CallAfter(dialog.Destroy)

def start_copy_process():
    try:
        CopyDialog = wx.App(False)
        total_files = count_total_files(folders_to_copy, src_base_path)
        dialog = CopyFilesDialog(None, total_files)
        dialog.Show()
        thread = threading.Thread(target=copy_folders, args=(folders_to_copy, src_base_path, dst_base_path, dialog))
        thread.start()
        CopyDialog.MainLoop()
    except:
        sys.exit()

# Danh sách các thư mục cần sao chép
folders_to_copy = [
    "Icon",
    "Languages",
    "LBP6300dn_R150_V110_W64_uk_EN_1",
    "LBP6300dn_R150_V110_W64_vi_VN_1",
    "LBP2900_R150_V330_W64_vi_VN_2",
    "LBP2900_R150_V330_W64_uk_EN_2",
    "License"
]

# Xây dựng đường dẫn mới và tạo thư mục
dst_base_path = os.path.join(temp_folder_path, 'TDP')
if not os.path.exists(dst_base_path):
    os.makedirs(dst_base_path)

detect_language()
Privacy = wx.App(False)
dialog = PrivacyCheck(None, title="Terms of Use" if current_language == 'en' else 'Điều khoản sử dụng')
dialog.Show()
Privacy.MainLoop()

time.sleep(0.2)
# Khởi động quá trình sao chép
start_copy_process()

def is_process_running(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return True
    return False

def recheck_and_set_new_dir():        
    """Kiểm tra xem file tồn tại không nếu không thì set lại dir từ Temp"""
    missing_file_after_check = [f for f in files_to_check if not os.path.isfile(f)]
    
    if missing_file_after_check:
        # Define new paths for missing files in the temp directory
        global file_icon, file_en, file_vi, icon_vi, icon_us, license_en, license_vi
        global file_setup_driver_vi_6300, file_Uninstall_driver_vi_6300        
        global file_setup_driver_en_6300, file_Uninstall_driver_en_6300
        global file_setup_driver_vi_2900, file_Uninstall_driver_vi_2900
        global file_setup_driver_en_2900, file_Uninstall_driver_en_2900
        global icon_info, icon_change_language, icon_exit, icon_install, icon_uninstall, icon_terminal, icon_restart
        
        file_icon = os.path.join(temp_path, 'TDP', 'Icon', 'IconProgram.ico')
        file_en = os.path.join(temp_path, 'TDP', 'Languages', 'en.lng')
        file_vi = os.path.join(temp_path, 'TDP', 'Languages', 'vi.lng')
        file_setup_driver_vi_6300 = os.path.join(temp_path, 'TDP', 'LBP6300dn_R150_V110_W64_vi_VN_1', 'SetupDriver.exe')
        file_Uninstall_driver_vi_6300= os.path.join(temp_path, 'TDP', 'LBP6300dn_R150_V110_W64_vi_VN_1', 'MISC', 'CNABBUND.exe')
        file_setup_driver_en_6300 = os.path.join(temp_path, 'TDP', 'LBP6300dn_R150_V110_W64_uk_EN_1', 'SetupDriver.exe')
        file_Uninstall_driver_en_6300 = os.path.join(temp_path, 'TDP', 'LBP6300dn_R150_V110_W64_uk_EN_1', 'MISC', 'CNABBUND.exe')
        file_setup_driver_vi_2900 = os.path.join(temp_path, 'TDP', 'LBP2900_R150_V330_W64_vi_VN_2', 'x64', 'SetupDriver.exe')
        file_Uninstall_driver_vi_2900 = os.path.join(temp_path, 'TDP', 'LBP2900_R150_V330_W64_vi_VN_2', 'x64', 'MISC', 'CNAB4UND.exe')
        file_setup_driver_en_2900 = os.path.join(temp_path, 'TDP', 'LBP2900_R150_V330_W64_uk_EN_2', 'x64', 'SetupDriver.exe')
        file_Uninstall_driver_en_2900 = os.path.join(temp_path, 'TDP', 'LBP2900_R150_V330_W64_uk_EN_2', 'x64', 'MISC', 'CNAB4UND.exe')
        icon_uninstall = os.path.join(temp_path, 'TDP', 'Icon', 'uninstall.png')
        icon_install = os.path.join(temp_path, 'TDP', 'Icon', 'install.png')
        icon_info = os.path.join(temp_path, 'TDP', 'Icon', 'info.png')
        icon_change_language = os.path.join(temp_path, 'TDP', 'Icon', 'change_language.png')
        icon_terminal = os.path.join(temp_path, 'TDP', 'Icon', 'terminal.png')
        icon_exit = os.path.join(temp_path, 'TDP', 'Icon', 'exit.png')
        icon_vi = os.path.join(temp_path, 'TDP', 'Icon', 'vi.png')
        icon_us = os.path.join(temp_path, 'TDP', 'Icon', 'us.png')
        icon_restart = os.path.join(temp_path, 'TDP', 'Icon', 'restart.png')
        license_vi = os.path.join('TDP', 'License', 'LICENSE-vi')
        license_en = os.path.join('TDP', 'License', 'LICENSE-en')

        # Update files_to_check list with the new paths
        files_to_check_after_change = [file_icon, file_en, file_vi, file_setup_driver_vi_6300, 
                              file_Uninstall_driver_vi_6300, file_setup_driver_en_6300, file_Uninstall_driver_en_6300,
                              file_setup_driver_vi_2900, file_Uninstall_driver_vi_2900,
                              file_setup_driver_en_2900, file_Uninstall_driver_en_2900,
                              icon_uninstall, icon_install, icon_info, icon_change_language, icon_terminal, 
                              icon_exit, icon_vi, icon_us, icon_restart]

        missing_file_after_change = [f for f in files_to_check_after_change if not os.path.isfile(f)]
        for missing_files in missing_file_after_change:
            if missing_files:
                class MissingFileError(wx.Dialog):
                    def __init__(self, parent, message, timeout=5):
                        super(MissingFileError, self).__init__(parent, title=f"Closing in {timeout} seconds", size=(470, 250))
                        
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
                        # Start playing the sound in a separate thread
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

                # Tạo ứng dụng wxPython
                MissingFile = wx.App(False)

                # Tạo hộp thoại tự động đóng
                message = (f"The program cannot be run because it is missing files that are important for operation! Exiting...\n\n"
                        f"Chương trình không thể chạy được vì thiếu các tệp quan trọng để hoạt động! Đang thoát...\n\n"
                        f"Missing File:\n{missing_files}")

                # Hiển thị hộp thoại tự động đóng với tiêu đề cập nhật thời gian và biểu tượng lỗi
                dlg = MissingFileError(None, message=f"{message}")
                # Show the dialog and start the timer
                dlg.ShowModal()

                # Kết thúc ứng dụng
                dlg.Destroy()
                MissingFile.MainLoop()

def load_language(current_language):
    recheck_and_set_new_dir()
    global language_data, panel
    if missing_files:
        file_path = os.path.join(temp_path, 'TDP', 'Languages',  f'{current_language}.lng')
    else:
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
            update_config_language(current_language, file_ini)

            # Ensure all children are destroyed before creating new ones
            for child in frame.GetChildren():
                child.Destroy()

            # Create new panel and sizer
            panel = wx.Panel(frame)
            vbox = wx.BoxSizer(wx.VERTICAL)

            frame.SetSize((250, 210) if current_language == 'vi' else (250, 170))
            frame_title = language_data['Title_Program']['Title']  # Đặt title từ file lng
            frame.SetTitle(frame_title)
            
            try:
            # Create menu and buttons
                create_menu_bar()
                create_buttons(current_language)
            except Exception as e:
                wx.MessageBox(
                            f"An error occurred while switching languages.\n {e} Exiting...",
                            "Error!",
                            wx.OK | wx.NO_DEFAULT | wx.ICON_ERROR
                )
                global LockFile
                LockFile = False
                lock_thread.join()
                delete_directory(dst_base_path)
                wx.CallAfter(sys.exit)

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
                timeout=2,  # Time to show message
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
    recheck_and_set_new_dir()
    menu_bar = wx.MenuBar()
    file_menu = wx.Menu()
    ManualSelectExe = wx.Menu()  # Tạo một menu con cho "Change EXE"

    # Define a function to load and resize images
    def load_and_resize_image(path, size):
        try:
            image = wx.Image(path, wx.BITMAP_TYPE_PNG)
            image = image.Rescale(*size)
            return wx.Bitmap(image)
        except Exception as e:
            return wx.Bitmap()  # Return an empty bitmap in case of error

    # Set desired size for menu icons
    icon_size = (16, 16)
    icon_size_vi = (24, 16)
    icon_size_us = (25, 16)  # Adjust width and height as needed

    # Load and resize icons for menu items
    lang_icon = load_and_resize_image(icon_change_language, icon_size)
    english_icon = load_and_resize_image(icon_us, icon_size_us)
    vietnamese_icon = load_and_resize_image(icon_vi, icon_size_vi)
    exit_icon = load_and_resize_image(icon_exit, icon_size)
    about_icon = load_and_resize_image(icon_info, icon_size)
    restart_icon = load_and_resize_image(icon_restart, icon_size)

    # Language submenu
    file_submenu = wx.Menu()
    current_language = config.get('Language', 'current_language')
    
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
    frame.Bind(wx.EVT_MENU, Restart_Computer)
    file_menu.AppendSeparator()
    exit_item = file_menu.Append(wx.ID_EXIT, language_data['Menu_Program']['menuExit'])
    exit_item.SetBitmap(exit_icon)
    frame.Bind(wx.EVT_MENU, on_exit, exit_item)

    menu_bar.Append(file_menu, language_data['Menu_Program']['menuFile'])

    help_menu = wx.Menu()

    about_item = help_menu.Append(wx.ID_ABOUT, language_data['Menu_Program']['menuAbout'])
    about_item.SetBitmap(about_icon)
    frame.Bind(wx.EVT_MENU, on_about, about_item)

    menu_bar.Append(help_menu, language_data['Menu_Program']['menuHelp'])

    frame.SetMenuBar(menu_bar)

def create_buttons(current_language):
    """Tạo các nút nhấn dựa vào ngôn ngữ hiện tại"""
    recheck_and_set_new_dir()
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
            return wx.Bitmap()  # Return an empty bitmap in case of error

# Set desired size for icons
    icon_size = (16, 16)  # Adjust width and height as needed

    # Load and resize icons
    install_icon = load_and_resize_image(icon_install, icon_size)
    uninstall_icon = load_and_resize_image(icon_uninstall, icon_size)
    lang_icon = load_and_resize_image(icon_terminal, icon_size)

    # Create buttons with icons
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

# Ví dụ cách sử dụng
driver_names = ["Canon LBP6300", "Canon LBP2900"]

def Uninstall_Driver(event):
    """
    Gỡ cài đặt driver máy in Canon.
    """
    recheck_and_set_new_dir()
    config.read('ToolDriverCanon.ini')
    current_language = config.get('Language', 'current_language')
    DisableAllButtons()

    def uninstall_thread():
        try:
            if are_drivers_installed(driver_names):
                print(f"[DEBUG] Before calling SelectDriverUninstall: {current_language}")
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
            elif are_drivers_installed("Canon LBP2900"):
                if current_language == "vi":
                    Uninstall_file = file_Uninstall_driver_vi_2900                
                else:
                    Uninstall_file = file_Uninstall_driver_en_2900

                if is_process_running(process_name_to_check_Uninstall):
                    wx.MessageBox(
                        language_data['Text_Messagebox']['process_runned_uninstall'],
                        language_data['title_messagebox']['Title_Messagebox-error'],
                        wx.OK | wx.ICON_ERROR
                    )
                elif is_process_running(process_name_to_check_install):
                    wx.MessageBox(
                        language_data['Text_Messagebox']['process_runned_install'],
                        language_data['title_messagebox']['Title_Messagebox-error'],
                        wx.OK | wx.ICON_ERROR
                    )
                else:
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
            recheck_and_set_new_dir()
              # Đọc lại cấu hình để cập nhật ngôn ngữ
            config.read('ToolDriverCanon.ini')
            current_language = config.get('Language', 'current_language')
            print(f"[DEBUG] current_language in Install_Driver: {current_language}")
            print(f"[DEBUG] Before calling SelectDriverInstall: {current_language}")
            wx.CallAfter(lambda: SelectDriverInstall(current_language))
        except Exception as e:
            wx.CallAfter(wx.MessageBox,
                f"{language_data['Text_Messagebox']['unknown_error']}\n{e}",
                language_data['title_messagebox']['Title_Messagebox-error'],
                wx.OK | wx.ICON_ERROR
            )
        finally:
            wx.CallAfter(EnableAllButtons)

    threading.Thread(target=install_thread, daemon=True).start()

def Install_language_vietnam_driver(event):
    """Cài đặt ngôn ngữ Việt"""
    DisableAllButtons()
    recheck_and_set_new_dir()

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
    except Exception as e:
        wx.MessageBox(
            f"{language_data['Text_Messagebox']['unknown_error']}\n{e}",
            language_data['title_messagebox']['Title_Messagebox-error'],
            wx.OK | wx.ICON_ERROR
        )
        print(e)

class SelectManualDriverInstall(wx.Dialog):
    def __init__(self, parent, title, current_language):
        super(SelectManualDriverInstall, self).__init__(parent, title=title, size=(450, 160))

        panel = wx.Panel(self)
        self.current_language = current_language

        # Tạo text
        text = wx.StaticText(panel, label=language_data['Text_Dialog']['InfoManualSelect'], pos=(10, 10))

        # Tạo đường dẫn (ô dòng đơn - single line)
        self.text_path = wx.TextCtrl(panel, pos=(25, 45), size=(240, 22), style=wx.TE_READONLY)
        self.text_path.SetHint("Đường dẫn")

        if not os.path.exists(settings_file):
            pass
        else:
            config.read(settings_file)
            try:
                InstallPath = config.get('Driver_Select_path', 'InstallDriver')
                self.text_path.SetValue(InstallPath)
            except:
                os.remove(settings_file)

        # Tạo nút Browse
        browse_button = wx.Button(panel, label="Browse..." if current_language == 'en' else "Duyệt...", pos=(275, 45), size=(70, 25))
        browse_button.Bind(wx.EVT_BUTTON, self.onBrowse)
        
        # Tạo nút Delete Value
        delete_button = wx.Button(panel, label="Delete Value" if current_language == 'en' else "Xóa giá trị", pos=(350, 45), size=(75, 25))
        delete_button.Bind(wx.EVT_BUTTON, self.Delete_value)

        # Tạo nút OK
        ok_button = wx.Button(panel, label="OK" if current_language == 'en' else 'Đồng ý' , pos=(352, 92), size=(73, 24))
        self.Bind(wx.EVT_BUTTON, self.OnOK, ok_button)

    def Delete_value(self, event):
        self.text_path.SetValue("")
        global deleteValueInstall
        deleteValueInstall = True

    def onBrowse(self, event):
        try:
            # Tạo hộp thoại chọn file .exe
            with wx.FileDialog(self, "Chọn tệp cài đặt" if current_language == 'vi' else "Select Install file", wildcard="Executable files (*.exe)|*.exe",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # Người dùng đã hủy, thoát ra.

                # Lấy đường dẫn của file được chọn
                pathnameInstall = fileDialog.GetPath()

                # Kiểm tra nếu tệp tồn tại
                if not os.path.exists(pathnameInstall):
                    wx.MessageBox(f"Tệp không tồn tại: {pathnameInstall}", "Lỗi", wx.ICON_ERROR)
                    return

                # Hiển thị đường dẫn trong ô line
                self.text_path.SetValue(pathnameInstall)

                config['DriverSelectPath']={
                    'InstallDriver': {pathnameInstall}
                }
        
        except Exception as e:
            wx.MessageBox(f"Đã xảy ra lỗi khi chọn tệp: {str(e)}", "Lỗi", wx.ICON_ERROR)

    def OnOK(self, event):
        try:
            if deleteValueInstall:
                with open(settings_file, 'w', encoding='utf-8') as file:
                    config.write(file)
            else:
                pass
            self.Close()
            InstallPath = config.get('DriverSelectPath', 'InstallDriver')
        except Exception as e:
            wx.MessageBox(f"Đã xảy ra lỗi: {str(e)}", "Lỗi", wx.ICON_ERROR)

class SelectManualDriverUninstall(wx.Dialog):
    def __init__(self, parent, title, current_language):
        super(SelectManualDriverUninstall, self).__init__(parent, title=title, size=(450, 160))

        panel = wx.Panel(self)
        self.current_language = current_language

        # Tạo text
        text = wx.StaticText(panel, label=language_data['Text_Dialog']['InfoManualSelect'], pos=(10, 10))

        # Tạo đường dẫn (ô dòng đơn - single line)
        self.text_path = wx.TextCtrl(panel, pos=(25, 45), size=(240, 22), style=wx.TE_READONLY)
        self.text_path.SetHint("Đường dẫn")

        if not os.path.exists(settings_file):
            pass
        else:
            config.read(settings_file)
            UninstallPath = config.get('Driver_Select_path', 'UninstallDriver')
            self.text_path.SetValue(UninstallPath)

        # Tạo nút Browse
        browse_button = wx.Button(panel, label="Browse..." if current_language == 'en' else "Duyệt...", pos=(275, 45), size=(70, 25))
        browse_button.Bind(wx.EVT_BUTTON, self.onBrowse)
        
        # Tạo nút Delete Value
        delete_button = wx.Button(panel, label="Delete Value" if current_language == 'en' else "Xóa giá trị", pos=(350, 45), size=(75, 25))
        delete_button.Bind(wx.EVT_BUTTON, self.Delete_value)

        # Tạo nút OK
        ok_button = wx.Button(panel, label="OK" if current_language == 'en' else 'Đồng ý' , pos=(352, 92), size=(73, 24))
        self.Bind(wx.EVT_BUTTON, self.OnOK, ok_button)

    def Delete_value(self, event):
        self.text_path.SetValue("")

    def onBrowse(self, event):
        try:
            # Tạo hộp thoại chọn file .exe
            with wx.FileDialog(self, "Chọn tệp cài đặt" if current_language == 'vi' else "Select Install file", wildcard="Executable files (*.exe)|*.exe",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # Người dùng đã hủy, thoát ra.

                # Lấy đường dẫn của file được chọn
                pathname = fileDialog.GetPath()

                # Kiểm tra nếu tệp tồn tại
                if not os.path.exists(pathname):
                    wx.MessageBox(f"Tệp không tồn tại: {pathname}", "Lỗi", wx.ICON_ERROR)
                    return

                # Hiển thị đường dẫn trong ô line
                self.text_path.SetValue(pathname)

                config['Driver_Select_path']={
                    'UninstallDriver': {pathname}
                }
        
        except Exception as e:
            wx.MessageBox(f"Đã xảy ra lỗi khi chọn tệp: {str(e)}", "Lỗi", wx.ICON_ERROR)

    def OnOK(self, event):
        try:
            with open(settings_file, 'w', encoding='utf-8') as file:
                file.write(config)
            self.Close()
        except Exception as e:
            wx.MessageBox(f"Đã xảy ra lỗi: {str(e)}", "Lỗi", wx.ICON_ERROR)

def DialogSelectManualInstall(event):
    config.read(file_ini)
    current_language = config.get('Language', 'current_language')
    dialog=SelectManualDriverInstall(None, title=language_data['Title_Program']['SelectManualDriver'], current_language=current_language)
    dialog.ShowModal()
    dialog.Destroy()
def DialogSelectManualUninstall(event):
    print(2)
    pass

def update_config_language(new_language, config_file_path):
    """Cập nhật config ngôn ngữ mới"""
    recheck_and_set_new_dir()
    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w') as config_file:
            config_file.write("[Language]\n")
            config_file.write("current_language = en\n")

    config.read(config_file_path)  # Đọc tệp cấu hình hiện có
    
    if not config.has_section('Language'):
        config.add_section('Language')
    
    config.set('Language', 'current_language', new_language)
    
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

class LicenseFrame(wx.Frame):
    def __init__(self, parent, title, license_file_path):
        super(LicenseFrame, self).__init__(parent, title=title, size=(400, 300))

        self.license_file_path = license_file_path  # Save the license file path

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        scrolled_window = wx.ScrolledWindow(panel, size=(380, 280))
        scrolled_window.SetScrollRate(20, 20)
        vbox_scrolled = wx.BoxSizer(wx.VERTICAL)

        # Set minimum size for the License window
        self.SetMinSize((300, 250))

        recheck_and_set_new_dir()
        try:
            with open(self.license_file_path, 'r', encoding='utf-8') as file:
                license_text = file.read()
        except Exception as e:
            license_text = f"Could not load license file: {str(e)}"

        # Use wx.TextCtrl for displaying license content with word wrap enabled
        text_ctrl = wx.TextCtrl(scrolled_window, value=license_text, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_BESTWRAP)
        vbox_scrolled.Add(text_ctrl, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        scrolled_window.SetSizer(vbox_scrolled)

        vbox.Add(scrolled_window, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # OK Button to close the frame
        btn_ok = wx.Button(panel, label='OK')
        btn_ok.Bind(wx.EVT_BUTTON, self.OnClose)
        vbox.Add(btn_ok, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)  # Added border for spacing

        panel.SetSizer(vbox)

        # Hide the frame icon by setting an empty icon
        self.SetIcon(wx.Icon(file_icon))  # Set an empty icon to hide the default icon

    def OnClose(self, event):
        self.Close()

class About(wx.Dialog):
    def __init__(self, parent, current_language, title, file_icon, license_file_path):
        super(About, self).__init__(parent, title=title, size=(420, 222))

        self.license_file_path = license_file_path  # Save the license file path

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Horizontal sizer for icon and first block of text
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Load and resize the icon
        icon_img = wx.Image(file_icon, wx.BITMAP_TYPE_ANY)
        icon_img = icon_img.Scale(50, 50, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(icon_img))

        # Vertical sizer to hold text (aligned next to icon)
        text_vbox = wx.BoxSizer(wx.VERTICAL)

        # Text content based on language
        if current_language == "vi":
            label_about1 = f"Công cụ cài đặt trình điều khiển máy in Canon.\nPhiên bản v.{__version__}\nCopyright ©️ 2023-2024 TranPhuong319. All rights reserved."
            label_about2 = "\nTrình điều khiển máy in Canon.\nCopyright ©️ 2009-2012 Canon Inc. All rights reserved."
        else:
            label_about1 = f"Canon printer driver installation tool.\nVersion v.{__version__}\nCopyright ©️ 2023-2024 TranPhuong319. All rights reserved."
            label_about2 = "\nCanon driver.\nCopyright ©️ 2009-2012 Canon Inc. All rights reserved."

        web = "https://github.com/TranPhuong319/ToolDriverPrinter/"

        # Add the first block of text next to the icon
        text1 = wx.StaticText(panel, wx.ID_ANY, label_about1)
        text_vbox.Add(text1, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=5)

        # Add the website link directly under the first text block
        website_link = wx.adv.HyperlinkCtrl(panel, wx.ID_ANY, web)
        text_vbox.Add(website_link, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=5)

        # Add the second block of text under the link
        text2 = wx.StaticText(panel, wx.ID_ANY, label_about2)
        text_vbox.Add(text2, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=5)

        # Add the icon and the text_vbox to the horizontal sizer
        hbox.Add(bitmap, flag=wx.ALL, border=5)
        hbox.Add(text_vbox, proportion=1, flag=wx.EXPAND)

        # Add the horizontal sizer (icon + text) to the vertical sizer
        vbox.Add(hbox, flag=wx.ALL | wx.EXPAND, border=5)

        # License, Report, and OK buttons layout
        hbox_btn = wx.BoxSizer(wx.HORIZONTAL)

        # License button on the far left
        btn_license = wx.Button(panel, label='License' if current_language == "en" else 'Giấy phép')  # Add License button
        btn_license.Bind(wx.EVT_BUTTON, self.show_license_action)  # Bind event for License button
        hbox_btn.Add(btn_license, flag=wx.ALL, border=5)  # License button on the far left

        # Add a spacer after the License button
        hbox_btn.AddStretchSpacer()

        # Report and OK buttons on the right
        btn_report = wx.Button(panel, label=language_data['Text_Button']['ButtonBug'])  # Add Report button
        btn_report.Bind(wx.EVT_BUTTON, self.report_bug_action)  # Bind event for Report button
        hbox_btn.Add(btn_report, flag=wx.ALL, border=5)

        btn_ok = wx.Button(panel, wx.ID_OK, label='OK' if current_language == 'en' else 'Đồng ý')
        btn_ok.Bind(wx.EVT_BUTTON, self.OkButton)
        hbox_btn.Add(btn_ok, flag=wx.ALL, border=5)
        self.SetAffirmativeId(wx.ID_OK)  # Nút OK
        btn_ok.SetFocus()  

        # Add the button sizer to the vertical sizer
        vbox.Add(hbox_btn, flag=wx.EXPAND | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def report_bug_action(self, event):
        """Open the web page for reporting a bug"""
        bug_url = "https://github.com/TranPhuong319/ToolDriverCanon/issues"
        webbrowser.open(bug_url)

    def show_license_action(self, event):
        """Hiện license dựa triên ngôn ngữ"""
        config.read(file_ini)
        current_language = config.get('Language', 'current_language')
        if (os.path.exists(license_vi) and current_language == 'vi') or (os.path.exists(license_en) and current_language == 'en'):
            license_frame = LicenseFrame(self, title="License" if current_language == 'en' else 'Giấy phép', license_file_path=self.license_file_path)
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
    recheck_and_set_new_dir()
    try:
        config.read(file_ini)
        current_language = config.get('Language', 'current_language')
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
        wx.CallAfter(delete_directory(dst_base_path))
        wx.CallAfter(sys.exit)

def delete_directory(path):
    """Xóa thư mục và tất cả nội dung bên trong, sau đó đóng chương trình."""
    if os.path.isdir(path):
        try:
            print(f"Đang xóa thư mục: {path}")
            shutil.rmtree(path)  # Cố gắng xóa thư mục
            print(f"Đã xóa thành công thư mục: {path}")
        except (FileNotFoundError, PermissionError, OSError) as e:
            print(f"Không thể xóa thư mục {path}: {e}")  # In ra lỗi phát sinh khi xóa thư mục
    else:
        print(f"Đường dẫn {path} không phải là thư mục hợp lệ.")

    # Xóa file lock nếu tồn tại và đóng chương trình
    if os.path.exists(lock_program):
        lock_thread.join()
        os.remove(lock_program)

def Restart_Computer(event):
    """Khởi động lại máy tính"""
    recheck_and_set_new_dir()
    if not DisableButtonRestart():
        return  # Exit the function if an error occurred

    confirm_restart_pc = wx.MessageBox(
                        language_data['Text_Messagebox']['confirm_restart_pc'],
                        language_data['title_messagebox']['Title_Messagebox-yesno'],
                        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
    )
    if confirm_restart_pc == wx.YES:
        subprocess.run(restart_computer, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
        sys.exit()

def on_exit(event):
    """Đóng chương trình"""
    # Kiểm tra trạng thái trước khi đóng
    if is_process_running(process_name_to_check_install) or is_process_running(process_name_to_check_Uninstall):
        wx.MessageBox(
            language_data['Text_Messagebox']['not_close_window'],
            language_data['title_messagebox']['Title_Messagebox-warning'],
            wx.OK | wx.ICON_WARNING
        )
    else:
        global LockFile
        LockFile = False
        lock_thread.join()
        delete_directory(dst_base_path)
        wx.CallAfter(sys.exit)

class window(wx.App):
    def OnInit(self):
        global frame
        global current_language
        # Xác định kích thước cửa sổ dựa trên ngôn ngữ
        window_size = (250, 210) if current_language == "vi" else (250, 170)

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
                        f"An error occurred while loading program.\n {e}\nExiting...",
                        "Error!",
                        wx.OK | wx.ICON_ERROR
            )
            global LockFile
            LockFile = False
            lock_thread.join()
            delete_directory(dst_base_path)
            wx.CallAfter(sys.exit)

        create_buttons(current_language)

        frame.Show()
        return True
    
def on_closing(event):
    """Đóng chương trình"""
    # Kiểm tra trạng thái trước khi đóng
    if is_process_running(process_name_to_check_install) or is_process_running(process_name_to_check_Uninstall):
        wx.MessageBox(
            language_data['Text_Messagebox']['not_close_window'],
            language_data['title_messagebox']['Title_Messagebox-warning'],
            wx.OK | wx.ICON_WARNING
        )
    else:
        global LockFile
        LockFile = False
        lock_thread.join()
        delete_directory(dst_base_path)
        wx.CallAfter(sys.exit)
        
detect_language()

with open(f'Languages\{current_language}.lng', 'r', encoding='utf-8') as file:
    language_data.read_file(file)

TDP = window()
TDP.MainLoop()