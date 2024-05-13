from odoo import models, fields, api
from datetime import date


class DepartmentMove(models.Model):
    _name = 'department.move'
    _description = 'Employee transfer departments'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employees')
    old_department = fields.Many2one('hr.department', string='Old Department')
    new_department = fields.Many2one('hr.department', string='New Department')
    date_transfer = fields.Date(string='Date Transferred')


class InternUpgrade(models.Model):
    _name = 'intern.upgrade'
    _description = 'Intern upgrade to employee'
    _rec_name = 'intern_id'

    intern_id = fields.Many2one('hr.employee', string='Intern')
    date_upgrade = fields.Date(string='Date Upgraded')
    department = fields.Many2one('hr.department', string='Department')


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    def write(self, vals):
        dept_vals_lst = []
        intern_up_lst = []
        for record in self:
            if record.department_id.id != vals.get('department_id') \
                    and (vals.get('department_id') and record.department_id.id) and record.employee_type != 'trainee':
                dept_move_vals = {'employee_id': record.id, 'old_department': record.department_id.id,
                                  'new_department': vals.get('department_id'), 'date_transfer': date.today()}
                dept_vals_lst.append(dept_move_vals)
            if record.employee_type == 'trainee' and vals.get('employee_type') == 'employee':
                intern_up_vals = {'intern_id': record.id, 'date_upgrade': date.today(),
                                  'department': record.department_id.id}
                intern_up_lst.append(intern_up_vals)
        self.env['department.move'].create(dept_vals_lst)
        self.env['intern.upgrade'].create(intern_up_lst)
        return super(HrEmployeeInherit, self).write(vals)

    @api.onchange('job_id')
    def onchange_job_id(self):
        if self.job_id and self.job_id.job_type == 'intern':
            self.employee_type = "trainee"

    @api.onchange('department_id')
    def _onchange_department(self):
        if self.department_id:
            self.coach_id = self.department_id.manager_id
            if self.department_id.manager_id.user_id:
                self.leave_manager_id = self.department_id.manager_id.user_id


# class HrApplicantInherit(models.Model):
#     _inherit = 'hr.applicant'
#
#     def write(self, vals):
#         trainee_lst = []
#         for record in self:
#             if record.stage_id == record.env.ref('hr_recruitment.stage_job4') \
#                     and vals.get('stage_id') == record.env.ref('hr_recruitment.stage_job5').id:
#                 emp_id = record.emp_id
#                 if not emp_id:
#                     action = record.create_employee_from_applicant()
#                     emp_vals = {key.replace("default_", ""): value for key, value in action['context'].items() if
#                                 key.startswith("default_")}
#                     emp_id = self.env['hr.employee'].create(emp_vals)
#                 # trainee_vals = {'intern_id': emp_id.id, 'date_upgrade': date.today()}
#                 # trainee_lst.append(trainee_vals)
#                 if record.job_id.job_type == 'intern':
#                     trainee_vals = {'intern_id': emp_id.id, 'date_upgrade': date.today(),
#                                     'department': emp_id.department_id.id}
#                     trainee_lst.append(trainee_vals)
#
#         self.env['intern.upgrade'].create(trainee_lst)
#
#         return super(HrApplicantInherit, self).write(vals)


class HrJobInherit(models.Model):
    _inherit = 'hr.job'

    job_type = fields.Selection([('intern', 'TTS'), ('non_intern', 'Vị trí khác')])


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    employee_at_date = fields.Integer('Số lượng nhân viên tại ngày', compute="_compute_total_emp_at_date")

    def _compute_total_emp_at_date(self):
        filter_date = self.env.context.get('filter_date')
        for record in self:
            # Nếu có context lọc ngày thì tính toán theo ngày, không có thì lấy tổng số nhân viên hiện tại
            total_employee = self.env['hr.employee'].search_count(
                [('employee_type', 'in', ['employee', 'freelance']), ('department_id', '=', record.id)])
            # filter_date = '2022-06-02 00:00:00'
            if filter_date:
                total_applicant = self.env['hr.applicant'].search_count(
                    [('job_id.job_type', '!=', 'intern'), ('date_closed', '>=', filter_date),
                     ('date_closed', '<=', date.today()), ('department_id', '=', record.id)])
                total_upgrade = self.env['intern.upgrade'].search_count(
                    [('date_upgrade', '>=', filter_date), ('date_upgrade', '<=', date.today()),
                     ('department', '=', record.id)])
                total_resignation = self.env['hr.resignation'].search_count(
                    [('approved_revealing_date', '>=', filter_date), ('approved_revealing_date', '<=', date.today()),
                     ('department_id', '=', record.id)])
                total_move_in = self.env['department.move'].search_count(
                    [('date_transfer', '>=', filter_date), ('date_transfer', '<=', date.today()),
                     ('new_department', '=', record.id)])
                total_move_out = self.env['department.move'].search_count(
                    [('date_transfer', '>=', filter_date), ('date_transfer', '<=', date.today()),
                     ('old_department', '=', record.id)])

                record.employee_at_date = total_employee - total_applicant - total_upgrade - total_move_in + total_resignation + total_move_out
            else:
                record.employee_at_date = total_employee


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    @api.depends('equipment_assign_to', 'employee_id.department_id')
    def _compute_equipment_assign(self):
        res = super(MaintenanceEquipment, self)._compute_equipment_assign()
        for equipment in self:
            if equipment.equipment_assign_to == 'other':
                equipment.employee_id = equipment.employee_id
                equipment.department_id = equipment.employee_id.department_id
        return res


class Contract(models.Model):
    _inherit = 'hr.contract'

    @api.depends('employee_id', 'employee_id.department_id')
    def _compute_employee_contract(self):
        return super(Contract, self)._compute_employee_contract()


