# Gateway Application Binary Compilation Script

## 1. What the Script Does

- Automates the compilation of the Gateway Application.
- Compiles all required C source files using the AArch64 GCC cross-compiler.
- Links all required libraries such as pthread, json-c, microhttpd, Paho MQTT, curl, and rt.
- Generates the Gateway Application binary (`gwbuild-Dual`).
- Checks whether the compilation is successful and displays the generated binary details.

## 2. How It Works

- Navigates to the Gateway Application source directory.
- Executes the GCC compilation command.
- Compiles all required C source files.
- Links the required libraries.
- Generates the output binary named `gwbuild-Dual`.
- Checks the compilation status.
- Displays a success or failure message.
- Displays the generated binary details if compilation is successful.

## 3. Steps to Use It

1. Open the Ubuntu terminal.
2. Log in to Vinoth's PC.
   ```bash
   ssh elmpc-357@192.168.40.145
   ```
3. Create Directory.
   ```bash
   mkdir <directory_name>
   ```
4. Download the script.
   ```bash
   wget https://github.com/vinoth-elm/PQ-Development-Tools/blob/main/PQ-Application-compiling-tool/PQ-compiling_script.sh
   ```
5. Change the permission for file.
   ```bash
   sudo chmod a+x PQ-compiling_script.sh
   ```
6. Run the compilation script:
   ```bash
   ./PQ-compiling_script.sh
   ```
7. Enter the source code path.
8. Wait until the compilation process is completed.

9. Check the compilation status:
   - If compilation is successful, a success message will be displayed.
   - If compilation fails, a failure message will be displayed.

10. Check the generated Gateway Application binary:

   ```bash
   ls -l gwbuild-Dual
   ```

11. Verify that the `gwbuild-Dual` binary has been generated successfully.

**Note:** Make sure all required source files, libraries, and the cross-compiler are available before running the script.
