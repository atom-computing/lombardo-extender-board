
all: lombardo.dtbo

lombardo.dtbo: lombardo.dts
	dtc -O dtb -o lombardo.dtbo lombardo.dts

clean:
	rm -rf lombardo.dtbo

load:
	mkdir /sys/kernel/config/device-tree/overlays/lombardo
	cat lombardo.dtbo > /sys/kernel/config/device-tree/overlays/lombardo/dtbo

unload:
	rmdir /sys/kernel/config/device-tree/overlays/lombardo
