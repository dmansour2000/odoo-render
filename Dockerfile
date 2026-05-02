FROM odoo:16.0

# Copy custom config
COPY odoo.conf /etc/odoo/odoo.conf

# Optional: copy custom addons
# COPY ./addons /mnt/extra-addons

EXPOSE 8069

CMD ["odoo", "--config=/etc/odoo/odoo.conf"]