FROM odoo:16.0

USER root

# cache bust
RUN echo "v3"

COPY odoo.conf /etc/odoo/odoo.conf
COPY addons /mnt/extra-addons

USER odoo

EXPOSE 8069

CMD ["odoo", "--config=/etc/odoo/odoo.conf", "--init=base", "--without-demo=all"]