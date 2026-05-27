from odoo import models, fields, api


class BurgerOrder(models.Model):
    _name = 'burger.order'
    _description = 'Pedido de Hamburguesería'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_order desc, id desc'

    name = fields.Char(
        string='Número de Pedido',
        readonly=True,
        copy=False,
        default='Nuevo',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True,
        tracking=True,
    )
    date_order = fields.Datetime(
        string='Fecha',
        default=fields.Datetime.now,
        tracking=True,
    )
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('waiting', 'En Espera'),
        ('preparing', 'En Preparación'),
        ('ready', 'Listo'),
        ('delivered', 'Entregado'),
        ('returned', 'Devuelto'),
    ], string='Estado', default='draft', tracking=True, copy=False)
    order_line_ids = fields.One2many(
        'burger.order.line',
        'order_id',
        string='Líneas de Pedido',
    )
    amount_total = fields.Float(
        string='Total',
        compute='_compute_amount_total',
        store=True,
        digits=(10, 2),
    )
    return_reason = fields.Text(string='Motivo de Devolución', readonly=True)
    notes = fields.Text(string='Notas')

    @api.depends('order_line_ids.subtotal')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(order.order_line_ids.mapped('subtotal'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code('burger.order') or 'Nuevo'
                )
        return super().create(vals_list)

    def action_waiting(self):
        self.write({'state': 'waiting'})

    def action_preparing(self):
        self.write({'state': 'preparing'})

    def action_ready(self):
        self.write({'state': 'ready'})

    def action_delivered(self):
        self.write({'state': 'delivered'})

    def action_return(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Gestionar Devolución',
            'res_model': 'burger.return.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id},
        }
