#!/bin/bash
set -e # if any make command fails it will give error

echo -e "\nStarted creating image"
cd /home/elm_ubuntu/bkp_vasu/final_rockpis_buildroot
make elmeasure-dual-dirclean
make elmeasure-dirclean

echo -e "\nSelect service\n1.Single service\n2.Dual service"
read service
echo "Paste the commit id"
read ID
echo -e "Select size\n1.1GB\n2.4GB\n3.8GB"
read size


if [ $service -eq 1 ]
then
 cd /home/elm_ubuntu/bkp_vasu/final_rockpis_buildroot/package/elmeasure
 sed -i '1s/.*/ELMEASURE_VERSION = '"$ID"'/' elmeasure.mk # To change the commit ID in .mk file
 echo "***Updated ID***"
 grep "ELMEASURE_VERSION =" elmeasure.mk # To check commit ID is updated or not
 cd /home/elm_ubuntu/bkp_vasu/final_rockpis_buildroot
 make elmeasure-rebuild
 make elmeasure-reinstall
 make

elif [ $service -eq 2 ]
then
 cd /home/elm_ubuntu/bkp_vasu/final_rockpis_buildroot/package/elmeasure-dual
 sed -i '1s/.*/ELMEASURE_DUAL_VERSION = '"$ID"'/' elmeasure-dual.mk
 echo "***Updated ID***"
 grep "ELMEASURE_DUAL_VERSION =" elmeasure-dual.mk
 cd /home/elm_ubuntu/bkp_vasu/final_rockpis_buildroot
 make elmeasure-dual-rebuild
 make elmeasure-dual-reinstall
 make
else
 echo "invalid"
fi

sudo  mkdir -p /media/dest
sudo  mkdir -p /media/src
sudo  mkdir -p /home/elm_ubuntu/gen_build

#image size
cd /home/elm_ubuntu/gen_build
if [ $size -eq 1 ]
then
 sudo dd if=/dev/zero of=root.img bs=1M count=0 seek=780
elif [ $size -eq 2 ]
then
 sudo dd if=/dev/zero of=root.img bs=1M count=0 seek=3400
elif [ $size -eq 3]
then 
 sudo dd if=/dev/zero of=root.img bs=1M count=0 seek=6800
else
 echo "invalid"
fi

# formating the image...
sudo mkfs.ext4 root.img
echo "format"

#mount src & dest...
sudo mount root.img /media/dest 
cd /home/elm_ubuntu/bkp_vasu/final_rockpis_buildroot/output/images
sudo mount rootfs.ext4 /media/src
echo "mount"

#configure root file system...
cd /media/src
sudo cp -rfp * /media/dest
echo "root file"

#unmount src & dest...
sudo umount /media/dest
cd
sudo umount /media/src
echo "unmount"

#check and repair file system...
cd /home/elm_ubuntu/gen_build
e2fsck -p -f root.img
echo "repair"

#Copy root image to make final image...
cp root.img /home/elm_ubuntu/bkp_vasu/Rock_Chip/rootfs
echo "copy"

#Build Final Image...
cd /home/elm_ubuntu/bkp_vasu/Rock_Chip
build/mk-image.sh -c rk3308 -t system -r rootfs/root.img

echo -e "\n***Image Created successfully***"







 




 

