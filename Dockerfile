FROM odoo:16.0

COPY odoo.conf /etc/odoo/odoo.conf
COPY addons /mnt/extra-addons
COPY --chmod=755 entrypoint.sh /entrypoint.sh

EXPOSE 8069

CMD ["/entrypoint.sh"]