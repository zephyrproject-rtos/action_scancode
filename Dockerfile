FROM ghcr.io/zephyrproject-rtos/scancode:v1.0.0

COPY entrypoint.sh /entrypoint.sh
COPY license_check.py /license_check.py

ENTRYPOINT ["/entrypoint.sh"]
