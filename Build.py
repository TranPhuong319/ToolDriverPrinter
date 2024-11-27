# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time
import getpass

while True:
    try:
        def signAllFiles(namefile, pathpfx, password, algorithmSign, timestamp):
            if not timestamp == "":
                signtoolcmd = f"signtool sign /f {pathpfx} /p {password} /fd {algorithmSign} /tr {timestamp} /td {algorithmSign} /v {namefile}"
            else:
                signtoolcmd = f"signtool sign /f {pathpfx} /p {password} /fd {algorithmSign} /v {namefile}"
            subprocess.run(f"cmd /c {signtoolcmd}")
        os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
        os.system('chcp 65001 >nul')
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
                "ToolDriverPrinter.py ",
                "--windows-uac-admin ",
                r"--windows-icon-from-ico=Icon/IconProgram.ico ",
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
                '"Tools_py\\Fix_not_run_program.py"',
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
                            "wxpython", "psutil", "nuitka", "win10toast", "plyer", "pillow", "getpass"])
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
            
            while True:
                choice = main_menu()
                if choice == "1":
                    if runBuildAll == False:
                        clear_screen()
                        build_tool_driver_printer(version_goc)
                elif choice == "2":
                    if runBuildAll == False:
                        clear_screen()
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
    except KeyboardInterrupt:
        print("\n")
        confirmExit = input("Do you want to exit? (Y/N): ")
        if confirmExit == "y" or confirmExit == "Y":
            sys.exit(0)
        else:
            continue