FROM odoo:16.0

COPY odoo.conf /etc/odoo/odoo.conf
COPY addons /mnt/extra-addons
COPY entrypoint.sh /tmp/entrypoint.sh

RUN sed 's/\r//' /tmp/entrypoint.sh > /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 8069

CMD ["/usr/local/bin/entrypoint.sh"]