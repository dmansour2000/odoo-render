FROM odoo:16.0

USER root

COPY odoo.conf /etc/odoo/odoo.conf
COPY addons /mnt/extra-addons
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN sed -i 's/\r//' /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh

USER odoo

EXPOSE 8069

CMD ["/usr/local/bin/entrypoint.sh"]