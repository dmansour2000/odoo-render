#!/bin/bash
set -e

echo "Initializing Odoo database..."
odoo \
  --config=/etc/odoo/odoo.conf \
  --init=base \
  --without-demo=all \
  --stop-after-init

echo "Starting Odoo..."
exec odoo --config=/etc/odoo/odoo.conf