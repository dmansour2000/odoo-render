FROM odoo:16

# Copy custom addons
COPY ./addons /mnt/extra-addons

USER odoo
