# Rock Pi S Image Creation Script

## 1. What the Script Does

- Automates the creation of Rock Pi S (RK3308) system images.
- Supports both Single Service and Dual Service builds.
- Allows users to select the image size (1GB, 4GB, or 8GB).
- Updates the application's Git commit ID and generates the final system image.

## 2. How It Works

- Cleans the previous build files.
- Updates the selected service's Git commit ID in the corresponding `.mk` file.
- Rebuilds and reinstalls the selected application.
- Creates an EXT4 root filesystem image with the selected size.
- Copies the Buildroot root filesystem into the generated image.
- Checks and repairs the filesystem.
- Copies the generated root image to the Rockchip directory.
- Generates the final system image.

## 3. Steps to Use It

1. Open the Ubuntu terminal.
2. Log in to Raghu's PC.
   ```bash
   ssh elmpc_ubuntu@192.168.40.136
   ```
3. Create Directory.
   ```bash
   mkdir <directory_name>
   ```
4. Download the script.
   ```bash
   wget https://github.com/vinoth-elm/PQ-Development-Tools/blob/main/PQ-image-creation-tool/image_creation.sh
   ```
5. Change the permission for file.
   ```bash
   sudo chmod a+x image_creation.sh
   ```
6. Run the image creation script.
7. Select either Single Service or Dual Service.
8. Enter the Git commit ID.
9. Select the image size (1GB or 4GB or 8GB).
10. Wait until the image creation process is completed.

Note : Enter the Password if required.

11. Navigate to the Rockchip output directory:
   ```bash
   cd ~/bkp_vasu/Rock_Chip/out
   ```
11. Check for the successfully generated final system image.
