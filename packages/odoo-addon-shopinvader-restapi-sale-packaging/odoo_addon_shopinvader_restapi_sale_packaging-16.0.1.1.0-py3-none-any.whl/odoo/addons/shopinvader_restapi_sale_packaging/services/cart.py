# Copyright 2020 Camptocamp (http://www.camptocamp.com).
# Copyright 2023 Acsone (http://www.acsone.eu).
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component


class CartService(Component):
    _inherit = "shopinvader.cart.service"

    def _validator_add_item(self):
        res = super()._validator_add_item()
        res.update(self._validator_packaging_info())
        return res

    def _validator_update_item(self):
        res = super()._validator_update_item()
        res.update(self._validator_packaging_info())
        return res

    def _prepare_cart_item(self, params, cart):
        res = super()._prepare_cart_item(params, cart)
        res.update(self._packaging_values_from_params(params))
        if {"product_packaging_id", "product_packaging_qty"}.issubset(res.keys()):
            res.pop("product_uom_qty", None)
        return res

    def _get_line_copy_vals(self, line):
        res = super()._get_line_copy_vals(line)
        if line.product_packaging_qty:
            res.update(
                {
                    "packaging_id": line.product_packaging_id.id,
                    "packaging_qty": line.product_packaging_qty,
                }
            )
        return res

    def _upgrade_cart_item_quantity_vals(self, item, params, **kw):
        res = super()._upgrade_cart_item_quantity_vals(item, params, **kw)
        res.update(self._packaging_values_from_params(params))
        if {"product_packaging_id", "product_packaging_qty"}.issubset(res.keys()):
            res.pop("product_uom_qty", None)
        return res
