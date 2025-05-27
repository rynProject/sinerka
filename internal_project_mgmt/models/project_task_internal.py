from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProjectTaskInternal(models.Model):
    _name = 'project.task.internal'
    _description = 'Internal Project Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Task Name', required=True, tracking=True)
    project_id = fields.Many2one('project.internal', string='Project', ondelete='cascade')
    assigned_to = fields.Many2one('hr.employee', string='Assigned To', tracking=True)
    due_date = fields.Date(string='Due Date')
    state = fields.Selection([
        ('open', 'Open'),
        ('working', 'Working'),
        ('review', 'Review'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='open', tracking=True)
    description = fields.Html(string='Description')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Priority', default='medium', tracking=True)

    @api.constrains('due_date', 'project_id')
    def _check_due_date(self):
        for rec in self:
            if rec.due_date and rec.project_id.end_date and rec.due_date > rec.project_id.end_date:
                raise ValidationError(_("Due Date tidak boleh lebih dari End Date proyek."))

    @api.constrains('assigned_to', 'state')
    def _check_task_limit(self):
        for rec in self:
            if rec.assigned_to and rec.state != 'done':
                active_tasks = self.search_count([
                    ('assigned_to', '=', rec.assigned_to.id),
                    ('state', '!=', 'done'),
                    ('id', '!=', rec.id)
                ])
                if active_tasks >= 5:
                    raise ValidationError(_(
                        "Karyawan %s tidak boleh memiliki lebih dari 5 tugas aktif.") % rec.assigned_to.name)
