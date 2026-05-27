from odoo import models, fields, api


class BurgerOrderLine(models.Model):
    _name = 'burger.order.line'
    _description = 'Línea de Pedido'

    order_id = fields.Many2one(
        'burger.order',
        string='Pedido',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        'burger.product',
        string='Producto',
        required=True,
    )
    quantity = fields.Integer(string='Cantidad', default=1)
    unit_price = fields.Float(
        string='Precio Unitario',
        digits=(10, 2),
    )
    extra_ingredient_ids = fields.Many2many(
        'burger.ingredient',
        'burger_order_line_extra_rel',
        'line_id',
        'ingredient_id',
        string='Ingredientes Extra',
    )
    remove_ingredient_ids = fields.Many2many(
        'burger.ingredient',
        'burger_order_line_remove_rel',
        'line_id',
        'ingredient_id',
        string='Sin Ingredientes',
    )
    extra_cost = fields.Float(
        string='Costo Extra',
        compute='_compute_extra_cost',
        store=True,
        digits=(10, 2),
    )
    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
        digits=(10, 2),
    )
    notes = fields.Char(string='Notas Especiales')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.price
            self.extra_ingredient_ids = [(5, 0, 0)]
            self.remove_ingredient_ids = [(5, 0, 0)]

    @api.depends('extra_ingredient_ids', 'extra_ingredient_ids.extra_price')
    def _compute_extra_cost(self):
        for line in self:
            line.extra_cost = sum(line.extra_ingredient_ids.mapped('extra_price'))

    @api.depends('quantity', 'unit_price', 'extra_cost')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * (line.unit_price + line.extra_cost)
