from odoo import models, fields


class BurgerProduct(models.Model):
    _name = 'burger.product'
    _description = 'Producto de Hamburguesería'
    _order = 'product_type, name'

    name = fields.Char(string='Nombre', required=True)
    product_type = fields.Selection([
        ('burger', 'Hamburguesa'),
        ('drink', 'Bebida'),
        ('side', 'Acompañamiento'),
        ('other', 'Otro'),
    ], string='Tipo', required=True, default='burger')
    price = fields.Float(string='Precio', required=True, digits=(10, 2))
    description = fields.Text(string='Descripción')
    image = fields.Image(string='Imagen')
    available_ingredient_ids = fields.Many2many(
        'burger.ingredient',
        'burger_product_ingredient_rel',
        'product_id',
        'ingredient_id',
        string='Ingredientes Disponibles',
    )
    active = fields.Boolean(default=True)
