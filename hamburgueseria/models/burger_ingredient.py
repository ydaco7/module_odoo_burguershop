from odoo import models, fields


class BurgerIngredient(models.Model):
    _name = 'burger.ingredient'
    _description = 'Ingrediente de Hamburguesa'
    _order = 'ingredient_type, name'

    name = fields.Char(string='Nombre', required=True)
    ingredient_type = fields.Selection([
        ('base', 'Base'),
        ('extra', 'Extra'),
        ('sauce', 'Salsa'),
        ('vegetable', 'Vegetal'),
    ], string='Tipo', required=True, default='base')
    extra_price = fields.Float(string='Precio Extra', default=0.0, digits=(10, 2))
    active = fields.Boolean(default=True)
