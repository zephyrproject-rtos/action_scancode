FROM zephyrprojectrtos/docker-scancode:v0.3

COPY entrypoint.sh /entrypoint.sh
COPY license_check.py /license_check.py

ENTRYPOINT ["/entrypoint.sh"]
