FROM odoo:16.0

USER root

COPY odoo.conf /etc/odoo/odoo.conf
COPY addons /mnt/extra-addons

USER odoo

EXPOSE 8069

CMD ["sh", "-c", "odoo --config=/etc/odoo/odoo.conf --init=base --without-demo=all --stop-after-init && odoo --config=/etc/odoo/odoo.conf"]