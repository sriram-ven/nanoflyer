#!/usr//bin/bash

init_system () {
	# sudo -s
	sudo apt-get update
	sudo apt-get upgrade
	sudo reboot
}

wifi_setup () {
	# sudo -s
	git clone https://github.com/lwfinger/rtl8723bu.git
	cd rtl8723bu
	source dkms.conf
	sudo mkdir /usr/src/$PACKAGE_NAME-$PACKAGE_VERSION
	sudo cp -r core hal include os_dep platform dkms.conf Makefile rtl8723b_fw.bin /usr/src/$PACKAGE_NAME-$PACKAGE_VERSION
	sudo dkms add $PACKAGE_NAME/$PACKAGE_VERSION
	sudo dkms autoinstall $PACKAGE_NAME/$PACKAGE_VERSION
	sudo reboot now
	# nmcli r wifi on
	# nmcli d wifi list
	# nmcli d wifi connect [SSID] password [PASSWORD]
}

imu_setup() {
	#sudo -s
	sudo pip install sparkfun-qwiic-icm20948
	python setup.py install
	python setup.py sdist
	cd dist
	pip install sparkfun_qwiic_icm20948-<version>.tar.gz
}
