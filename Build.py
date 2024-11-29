# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time
import getpass

while True:
    try:
        def check_python_version():
            if sys.version_info < (3, 8, 6):
                print(f"Error: Current Python version is {sys.version}. Minimum required version is 3.8.6.")
                return False
            else:
                print(f"Current Python version is {sys.version}. Minimum required version is satisfied.")
                return True

        # Kiểm tra xem Python có được cài đặt hay không
        def check_python_installed():
            try:
                subprocess.check_call(["python", "--version"])
                return True
            except FileNotFoundError:
                return False

        # Hàm cài đặt Python
        def install_python():
            response = input("Python is not installed or the version is incorrect. Would you like to install Python 3.8.6? (y/n): ").strip().lower()
            while response not in ['y', 'n']:
                print("Invalid input. Please re-enter.")
                response = input("Python is not installed or the version is incorrect. Would you like to install Python 3.8.6? (y/n): ").strip().lower()

            if response == 'y':
                # Tải xuống và cài đặt Python 3.8.6
                print("Downloading Python 3.8.6...")
                download_url = "https://www.python.org/ftp/python/3.8.6/python-3.8.6-amd64.exe"
                installer_path = os.path.join(os.getenv("TEMP"), "python-3.8.6.exe")

                # Tải Python 3.8.6
                subprocess.run(["curl", "-L", download_url, "-o", installer_path], check=True)

                print("Installing Python 3.8.6...")

                while True:
                    try:
                        # Cài đặt Python với quyền quản trị (UAC)
                        subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], check=True)
                        print("Install was Successful!")
                        subprocess.run(["python", "-m", "pip", "install", "--upgrade", 
                        "wxpython", "psutil", "nuitka", "win10toast", "plyer", "pillow"])
                        main()
                    except subprocess.CalledProcessError as e:
                        print(e)
                        if e.returncode == 1602:
                            print("An error occurred during installation.")
                            response = input("Do you want to reinstall? (y/n): ").strip().lower()
                            while response not in ['y', 'n']:
                                print("Invalid input. Please re-enter.")
                                response = input("Do you want to reinstall? (y/n): ").strip().lower()
                            
                            if response == 'y':
                                print("Installing Python 3.8.6...")
                                try:
                                    # Khởi chạy lại tệp cài đặt với quyền quản trị (UAC)
                                    subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], check=True)
                                    print("Install was Successful")
                                    subprocess.run(["python", "-m", "pip", "install", "--upgrade", 
                                    "wxpython", "psutil", "nuitka", "win10toast", "plyer", "pillow"])
                                    main()
                                    
                                except subprocess.CalledProcessError as inner_e:
                                    print("An error occurred during installation.")
                                    retry_response = input("Do you want to reinstall? (y/n): ").strip().lower()
                                    while retry_response not in ['y', 'n']:
                                        print("Invalid input. Please re-enter.")
                                        retry_response = input("Do you want to reinstall? (y/n): ").strip().lower()

                                    if retry_response == 'n':
                                        print("Installation was cancelled!")
                                        sys.exit(1)
                            elif response == 'n':
                                print("Installation was cancelled!")
                                sys.exit(1)
            elif response == "n":
                print("Installation was cancelled!")
                sys.exit(1)
            else:
                time.sleep(2)

        def signAllFiles(namefile, pathpfx, password, algorithmSign, timestamp):
            if not timestamp == "":
                signtoolcmd = f"signtool sign /f {pathpfx} /p {password} /fd {algorithmSign} /tr {timestamp} /td {algorithmSign} /v {namefile}"
            else:
                signtoolcmd = f"signtool sign /f {pathpfx} /p {password} /fd {algorithmSign} /v {namefile}"
            subprocess.run(f"cmd /c {signtoolcmd}")
        os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
        sys.stdout.reconfigure(encoding='utf-8')
        os.system("title Build project 'ToolDriverPrinter' wizard")

        version_goc = ""
        runBuildAll = False

        def clear_screen():
            os.system('cls' if os.name == 'nt' else 'clear')

        def main_menu():
            clear_screen()
            print("=" * 66)
            print("               Build project 'ToolDriverPrinter' wizard")
            print("=" * 66)
            print("\n                [1] Build ToolDriverPrinter")
            print("\n")
            print("\n                [2] Build Fix_not_run_program")
            print("\n")
            print("\n                [3] Build All")
            print("\n")
            print("\n                [4] Install/Update request library")
            print("\n")
            print("\n                [X] Exit")
            print("\n")
            print("\n" + "=" * 66 + "\n")
            choice = input("Your choice: ").strip().upper()
            return choice
        
        def signFile(namefile, runBuildAll):
            def tpcon():
                pathpfx = input("Enter the path certificate (*.pfx): ")
                password = getpass.getpass("Enter the password: ")
                algorithmSign = input("Enter the signing algorithm (default is SHA256):")
                print("\n")
                print("=" * 66)
                print("                    Select timestamp services")
                print("=" * 66)
                print("\n")
                print("           [1] Digicert: http://timestamp.digicert.com")
                print("\n")
                print("           [2] Sectigo: http://timestamp.sectigo.com")
                print("\n")
                print("           [3] GlobalSign: http://timestamp.globalsign.com/tsa/r6advanced1")
                print("\n")
                print("           [4] Certum: http://time.certum.pl")
                print("\n")
                timestamp = input("Select timestamp: ")
                if algorithmSign == "":
                    algorithmSign = "SHA256"
                    print(f"Algorithm: {algorithmSign}")
                if timestamp == "1":
                    timestamp = "http://timestamp.digicert.com"
                elif timestamp == "2":
                    timestamp = "http://timestamp.sectigo.com"
                elif timestamp == "3":
                    timestamp = "http://timestamp.globalsign.com/tsa/r6advanced1"
                elif timestamp == "4":
                    timestamp = "http://time.certum.pl"
                else:
                    timestamp = ""
                if not timestamp == "":
                    signtoolcmd = f"signtool sign /f {pathpfx} /p {password} /fd {algorithmSign} /tr {timestamp} /td {algorithmSign} /v {namefile}"
                else:
                    signtoolcmd = f"signtool sign /f {pathpfx} /p {password} /fd {algorithmSign} /v {namefile}"
                subprocess.run(f"cmd /c {signtoolcmd}")
            if runBuildAll == False:
                signTDP = input("\nDo you wanna sign this software? (Y/N): ")
                if signTDP == "Y" or signTDP == "y":
                    tpcon()
            else:
                tpcon()

        def build_tool_driver_printer(version):
            if runBuildAll == False:
                print("=" * 66)
                print("                     Build ToolDriverPrinter")
                print("=" * 66)

                if not version:
                    version = input("\nEnter the program version (format n.n.n.n): ").strip()        
                    print(f"Using Version: {version}")
                    print("\n>> Starting building ToolDriverPrinter...\n")
                else:
                    pass
            
            cmd = [
                "nuitka ",
                r"ToolDriverPrinter/ToolDriverPrinter.py ",
                r"--windows-icon-from-ico=ToolDriverPrinter/Icon/IconProgram.ico ",
                "--windows-uac-admin",
                "--onefile ",
                "--standalone ",
                "--lto=yes ",
                "--clang ",
                "--follow-imports ",
                "--windows-console-mode=disable ",
                "--remove-output ",
                "--noinclude-default-mode=error ",
                "--company-name=TranPhuong319 ",
                '--file-description="Easy Printer Driver Install/Uninstall Tool" ',
                '--product-name="Easy Printer Driver Install/Uninstall Tool" ',
                f"--file-version={version} ",
                f"--product-version={version} ",
                '--copyright="Copyright © 2023-2024 TranPhuong319. All rights reserved"'
            ]

            cmd = " ".join(cmd)
            
            # Dùng cmd để thực thi lệnh
            subprocess.run(
                f"cmd /c {cmd}",
            )
            if runBuildAll == False:
                signFile("ToolDriverPrinter.exe", runBuildAll)
                input("\nPress Enter to return...")

        def build_tools(version):
            if runBuildAll == False:
                print("=" * 66)
                print("                            Build Tools")
                print("=" * 66)
                print("\n")
                if not version:
                    version = input("Enter the program version (format n.n.n.n): ").strip()
                    print(f"Using Version: {version}")
                    print("\n>> Starting building Tools...\n")
                else:
                    pass

            cmd = [
                "nuitka" ,
                '"ToolDriverPrinter\\Tools_py\\Fix_not_run_program.py"',
                "--windows-uac-admin",
                "--onefile",
                "--standalone",
                "--lto=yes",
                "--clang",
                "--follow-imports",
                "--windows-console-mode=disable",
                "--remove-output",
                "--noinclude-default-mode=error",
                "--company-name=TranPhuong319",
                '--file-description="Fix not run Program" ',
                '--product-name="Fix not run Program" ',
                f"--file-version={version}",
                f"--product-version={version}",
                '--copyright="Copyright © 2023-2024 TranPhuong319. All rights reserved"',
            ]
            cmd = " ".join(cmd)
            
            subprocess.run(f"cmd /c {cmd}")
            
            if runBuildAll == False:
                signFile("Fix_not_run_program.exe", runBuildAll)
                input("\nPress Enter to return...")

        def build_all():
            clear_screen()
            print("=" * 66)
            print("                        Build All Components")
            print("=" * 66)
            print("\n")
            global runBuildAll
            runBuildAll = True

            # Yêu cầu nhập phiên bản cho ToolDriverPrinter
            version_tdp = input("Enter the program version for ToolDriverPrinter (format n.n.n.n): ").strip()

            # Nếu người dùng không nhập phiên bản cho Tools, dùng phiên bản của ToolDriverPrinter
            version_tools = input("Enter the program version for Tools (format n.n.n.n): ").strip()
            
            # Nếu không nhập phiên bản cho Tools, sử dụng phiên bản của ToolDriverPrinter
            if not version_tools:
                version_tools = version_tdp  # Sử dụng phiên bản của ToolDriverPrinter cho Tools

            # Gọi hàm Build ToolDriverPrinter và Build Tools với các phiên bản đã nhập
            print("\n>> Starting building ToolDriverPrinter with version", version_tdp, "...\n")
            build_tool_driver_printer(version_tdp)  # Gọi hàm Build ToolDriverPrinter
            
            print("\n>> Starting building Tools with version", version_tools, "...\n")
            build_tools(version_tools)  # Gọi hàm Build Tools
            
            print("\n")
            sign = input("Do you wanna sign all Files?(Y/N) ")
            if sign == "Y" or sign == "y":
                pathpfx = input("Enter the path certificate (*.pfx): ")
                password = getpass.getpass("Enter the password: ")
                algorithmSign = input("Enter the signing algorithm (default is SHA256):")
                print("\n")
                print("=" * 66)
                print("                    Select timestamp services")
                print("=" * 66)
                print("\n")
                print("           [1] Digicert: http://timestamp.digicert.com")
                print("\n")
                print("           [2] Sectigo: http://timestamp.sectigo.com")
                print("\n")
                print("           [3] GlobalSign: http://timestamp.globalsign.com/tsa/r6advanced1")
                print("\n")
                print("           [4] Certum: http://time.certum.pl")
                print("\n")
                timestamp = input("Select timestamp: ")
                if algorithmSign == "":
                    algorithmSign = "SHA256"
                    print(f"Algorithm: {algorithmSign}")
                if timestamp == "1":
                    timestamp = "http://timestamp.digicert.com"
                elif timestamp == "2":
                    timestamp = "http://timestamp.sectigo.com"
                elif timestamp == "3":
                    timestamp = "http://timestamp.globalsign.com/tsa/r6advanced1"
                elif timestamp == "4":
                    timestamp = "http://time.certum.pl"
                else:
                    timestamp = ""
                signAllFiles("ToolDriverPrinter.exe", pathpfx, password, algorithmSign, timestamp)
                signAllFiles("Fix_not_run_program.exe", pathpfx, password, algorithmSign, timestamp)
            print("\n")
            input("\nCompleted! Press Enter to return to the main menu.")
            runBuildAll = False

        def install_update_library():
            clear_screen()
            print("=" * 66)
            print("                       Install/Update Library")
            print("=" * 66)
            print("\n>> Installing/Updating necessary libraries...\n")
            subprocess.run(["python", "-m", "pip", "install", "--upgrade", 
                            "wxpython", "psutil", "nuitka", "win10toast", "plyer", "pillow"])
            print("\nCompleted! Press Enter to return to the main menu.")
            input()

        def exit_program():
            clear_screen()
            print("=" * 66)
            print("                            Exit Program")
            print("=" * 66)
            print("\n>> Thanks for using the program.")
            print("\n" + "=" * 66 + "\n")
            input("Press Enter to exit...")
            sys.exit()

        if __name__ == "__main__":
            def main():
                if not check_python_installed() or not check_python_version():
                    install_python()

                while True:
                    choice = main_menu()
                    if choice == "1":
                        build_tool_driver_printer(version_goc)
                    elif choice == "2":
                        build_tools(version_goc)
                    elif choice == "3":
                        build_all()
                    elif choice == "4":
                        install_update_library()
                    elif choice == "X":
                        exit_program()
                    else:
                        print("\nInvalid choice. Please try again.")
                        time.sleep(2)
            main()
    except KeyboardInterrupt:
        print("\n")
        confirmExit = input("Do you want to exit? (Y/N): ")
        if confirmExit == "y" or confirmExit == "Y":
            sys.exit(0)
        else:
            continue