FROM odoo:16

USER root

# Optional: install extra Python deps
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt || true

# Copy custom addons
COPY ./addons /mnt/extra-addons

USER odoo
