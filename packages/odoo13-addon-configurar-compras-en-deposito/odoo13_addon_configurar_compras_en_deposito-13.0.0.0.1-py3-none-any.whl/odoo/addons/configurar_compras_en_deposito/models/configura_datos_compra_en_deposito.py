from odoo import models

import logging
_logger = logging.getLogger(__name__)

PICKING_TYPE_COMPRA_DIRECTA = 1

class CompraDepositoWizard(models.TransientModel):
    """ Wizard: *** """
    _name = 'configura.datos.compra.deposito.wizard.editorial'
    _description = "Wizard para ajustar valores de compras hechas en la base datos para el correcto funcionamiento de compra en depósito."

    def ajustar_valores_compra_deposito(self):
        _logger.debug("******** AJUSTE VALORES COMPRA EN DEPOSITO **********")

        domain = [
            ('picking_type_id', '=', PICKING_TYPE_COMPRA_DIRECTA),
            ('state', 'in', ['done', 'purchase']),
        ]
        purchase_orders = self.env['purchase.order'].search(domain)
        total_purchase_lines_mod = 0
        
        for purchase_order in purchase_orders:
            _logger.debug(f"*** PURCHASE ORDER ID {(purchase_order.id)} ")
            for purchase_line in purchase_order.order_line:
                _logger.debug(f"** PURCHASE ORDER LINE ID {(purchase_line.id)} ")
                purchase_line.liquidated_qty = purchase_line.qty_received
                purchase_line.is_liquidated = True
                total_purchase_lines_mod += 1

        total_purchase_lines = self.env['purchase.order.line'].search_count([])
        _logger.debug(f"***** TOTAL PURCHASE LINES: {(total_purchase_lines)} ")
        _logger.debug(f"***** TOTAL PURCHASE LINES AJUSTADAS: {(total_purchase_lines_mod)} ")

        domain = [
            ('picking_type_id', '!=', PICKING_TYPE_COMPRA_DIRECTA),
            ('state', 'in', ['done', 'purchase']),
        ]
        other_purchase_orders = self.env['purchase.order'].search(domain)
        total_other_purchase_lines = sum(len(order.order_line) for order in other_purchase_orders)
        _logger.debug(f"***** TOTAL PURCHASE LINES PICKING TYPE DIFERENTE: {(total_other_purchase_lines)} ")

        domain = [
            ('state', 'not in', ['done', 'purchase']),
        ]
        draft_purchase_orders = self.env['purchase.order'].search(domain)
        total_draft_purchase_lines = sum(len(order.order_line) for order in draft_purchase_orders)
        _logger.debug(f"***** TOTAL PURCHASE LINES OTRO STATE: {(total_draft_purchase_lines)} ")
