from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_grade = fields.Selection([
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ], string='Partner Grade', default='bronze')

    customer_count_by_grade = fields.Char(
        string='Customer Count by Grade',
        compute='_compute_customer_count_by_grade',
        store=False
    )

    @api.depends('partner_grade', 'is_company')
    def _compute_customer_count_by_grade(self):
        grades = ['bronze', 'silver', 'gold']
        counts = {}
        Partner = self.env['res.partner']

        for grade in grades:
            count = Partner.search_count([
                ('is_company', '=', True),
                ('partner_grade', '=', grade)
            ])
            counts[grade] = count

        result = ", ".join(f"{grade.capitalize()}: {counts[grade]}" for grade in grades)

        for rec in self:
            rec.customer_count_by_grade = result
