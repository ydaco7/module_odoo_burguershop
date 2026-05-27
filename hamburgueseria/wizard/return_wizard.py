from odoo import models, fields
from odoo.exceptions import ValidationError


class BurgerReturnWizard(models.TransientModel):
    _name = 'burger.return.wizard'
    _description = 'Asistente de Devolución'

    order_id = fields.Many2one(
        'burger.order',
        string='Pedido',
        required=True,
    )
    return_date = fields.Date(
        string='Fecha de Devolución',
        default=fields.Date.today,
    )
    reason = fields.Text(
        string='Motivo de Devolución',
        required=True,
    )

    def action_confirm_return(self):
        if not self.reason:
            raise ValidationError('Debe especificar el motivo de la devolución.')
        self.order_id.write({
            'state': 'returned',
            'return_reason': self.reason,
        })
        self.order_id.message_post(
            body=f'Pedido devuelto el {self.return_date}. Motivo: {self.reason}',
        )
        return {'type': 'ir.actions.act_window_close'}
