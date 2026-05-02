FROM odoo:16.0-20250909

USER root

RUN echo "v6"

COPY odoo.conf /etc/odoo/odoo.conf
COPY addons /mnt/extra-addons
COPY start.py /start.py

USER odoo

EXPOSE 8069

CMD ["odoo", "--config=/etc/odoo/odoo.conf", "--database=odoodb_b6y6", "--update=web"]