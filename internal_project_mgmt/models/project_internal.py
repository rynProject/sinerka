from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class ProjectInternal(models.Model):
    _name = 'project.internal'
    _description = 'Internal Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Project Name', required=True, tracking=True)
    manager_id = fields.Many2one('hr.employee', string='Project Manager', required=True, tracking=True)
    department_id = fields.Many2one('hr.department', string='Department', related='manager_id.department_id', store=True, readonly=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    task_ids = fields.One2many('project.task.internal', 'project_id', string='Tasks')
    task_count = fields.Integer(string='Task Count', compute='_compute_task_count')
    progress = fields.Float(string='Progress (%)', compute='_compute_progress', store=True)
    task_count = fields.Integer(compute='_compute_task_count', string="Task Count")

    def action_view_tasks(self):
        return {
            'name': 'Tasks',
            'type': 'ir.actions.act_window',
            'res_model': 'project.task.internal',
            'view_mode': 'tree,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    @api.depends('task_ids')
    def _compute_task_count(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)

    @api.constrains('end_date', 'start_date')
    def _check_dates(self):
        for rec in self:
            if rec.end_date and rec.start_date and rec.end_date < rec.start_date:
                raise ValidationError(_("End Date harus lebih besar dari Start Date."))

    @api.constrains('state', 'manager_id')
    def _check_active_project_unique(self):
        for rec in self:
            if rec.state == 'in_progress':
                existing = self.search([
                    ('id', '!=', rec.id),
                    ('state', '=', 'in_progress'),
                    ('manager_id', '=', rec.manager_id.id)
                ])
                if existing:
                    raise ValidationError(_("Manager %s sudah memiliki proyek aktif lain.") % rec.manager_id.name)

    def action_start(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_complete(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('task_ids.state')
    def _compute_progress(self):
        for rec in self:
            total_tasks = len(rec.task_ids)
            if total_tasks == 0:
                rec.progress = 0.0
            else:
                done_tasks = len(rec.task_ids.filtered(lambda t: t.state == 'done'))
                rec.progress = (done_tasks / total_tasks) * 100

    def _compute_task_count(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)

    @api.model
    def check_overdue_tasks(self):
        today = date.today()
        projects = self.search([
            ('end_date', '<', today),
            ('state', '!=', 'done')
        ])
        for project in projects:
            overdue_tasks = project.task_ids.filtered(lambda t: t.state != 'done')
            if overdue_tasks:
                template = self.env.ref('internal_project_mgmt.email_template_task_overdue')
                if template:
                    template.send_mail(project.id)