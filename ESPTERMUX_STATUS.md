# ESPTermux experimental fork

This is a **development scaffold**, not yet a functional independent Termux distribution.

- Application id: `dev.mexicanbr.esptermux` (distinct from Termux).
- Android USB-host attachment matching for Espressif, CP210x, CH34x and FTDI vendor IDs.
- Uses native Android USB permission prompt; no Termux:API app required.
- Material 3 theme base for terminal activity; terminal viewport color scheme is intentionally preserved.
- GitHub Actions builds an experimental debug APK, and will report build failures.

## Known blockers (important)

1. The upstream Termux bootstrap contains a **hardcoded** `/data/data/com.termux/files/usr` prefix. A distinct app ID needs its own bootstrap **and rebuilt packages** targeting `/data/data/dev.mexicanbr.esptermux/files/usr`. The upstream bootstrap does not work as-is. The Gradle APK task is not proof that the shell starts.
2. Android USB Host APIs do not automatically create accessible Linux `/dev/ttyUSB*` ports for applications. A native integrated serial driver and an OS-device access strategy are still required for serial terminal, firmware upload and tooling. No fake device paths or custom shell commands have been added.
3. The USB device filter is broad by vendor, so compatible non-ESP devices can also trigger the prompt.
4. PlatformIO, ESP-IDF, esptool, MicroPython, Wi-Fi/BLE, and on-device compilation must be individually integrated and verified. They are **not yet** supported by the fork.
5. This project preserves normal terminal usage goals, but compatibility requires a complete rebuilt bootstrap and package ecosystem.

Upstream project: https://github.com/termux/termux-app (GPL-3.0).

## Release gate

The CI build is **diagnostic only** until a rebuilt bootstrap passes
`python3 scripts/audit_bootstrap.py --require-relocatable bootstrap-*.zip`.
A Gradle success alone is not a release. The bundled upstream bootstrap still
contains hundreds of hardcoded old-prefix references, including native ELF
executables. Scripts and `LD_LIBRARY_PATH` workarounds are not a replacement
for rebuilding the binaries and package repository for this application ID.
The audit gate is intentionally strict and will currently fail.
