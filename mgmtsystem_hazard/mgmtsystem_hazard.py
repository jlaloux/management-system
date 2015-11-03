# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields


def own_company(self):
    return self.env.user.company_id.id


def _parse_risk_formula(formula, a, b, c):
    """Calculate the risk replacing the variables A, B, C into the formula."""
    f = formula.replace('A', str(a)).replace('B', str(b)).replace('C', str(c))
    return eval(f)


class mgmtsystem_hazard_type(models.Model):
    _name = "mgmtsystem.hazard.type"
    _description = "Type of hazard"

    name = fields.Char('Type', size=50, required=True, translate=True)
    description = fields.Text('Description')


class mgmtsystem_hazard_risk_computation(models.Model):

    _name = "mgmtsystem.hazard.risk.computation"
    _description = "Computation Risk"

    name = fields.Char('Computation Risk', size=50, required=True, translate=True)
    description = fields.Text('Description')


class res_company(models.Model):
    _inherit = "res.company"

    def _get_formula(self):
        return self.env['mgmtsystem.hazard.risk.computation'].search([('name', '=', 'A * B * C')])

    risk_computation_id = fields.Many2one('mgmtsystem.hazard.risk.computation', 'Risk Computation', required=True,
                                          default=_get_formula)


class mgmtsystem_hazard_risk_type(models.Model):

    _name = "mgmtsystem.hazard.risk.type"
    _description = "Risk type of the hazard"

    name = fields.Char('Risk Type', size=50, required=True, translate=True)
    description = fields.Text('Description')


class mgmtsystem_hazard_origin(models.Model):

    _name = "mgmtsystem.hazard.origin"
    _description = "Origin of hazard"

    name = fields.Char('Origin', size=50, required=True, translate=True)
    description = fields.Text('Description')


class mgmtsystem_hazard_hazard(models.Model):

    _name = "mgmtsystem.hazard.hazard"
    _description = "Hazard"

    name = fields.Char('Hazard', size=50, required=True, translate=True)
    description = fields.Text('Description')


class mgmtsystem_hazard_probability(models.Model):

    _name = "mgmtsystem.hazard.probability"
    _description = "Probability of hazard"

    name = fields.Char('Probability', size=50, required=True, translate=True)
    value = fields.Integer('Value', required=True)
    description = fields.Text('Description')


class mgmtsystem_hazard_severity(models.Model):

    _name = "mgmtsystem.hazard.severity"
    _description = "Severity of hazard"

    name = fields.Char('Severity', size=50, required=True, translate=True)
    value = fields.Integer('Value', required=True)
    description = fields.Text('Description')


class mgmtsystem_hazard_usage(models.Model):

    _name = "mgmtsystem.hazard.usage"
    _description = "Usage of hazard"

    name = fields.Char('Occupation / Usage', size=50, required=True, translate=True)
    value = fields.Integer('Value', required=True)
    description = fields.Text('Description')


class mgmtsystem_hazard_control_measure(models.Model):

    _name = "mgmtsystem.hazard.control_measure"
    _description = "Control Measure of hazard"

    name = fields.Char('Control Measure', size=50, required=True, translate=True)
    responsible_user_id = fields.Many2one('res.users', 'Responsible', required=True)
    comments = fields.Text('Comments')
    hazard_id = fields.Many2one('mgmtsystem.hazard', 'Hazard', ondelete='cascade', select=True)


class mgmtsystem_hazard_test(models.Model):

    _name = "mgmtsystem.hazard.test"
    _description = "Implementation Tests of hazard"

    name = fields.Char('Test', size=50, required=True, translate=True)
    responsible_user_id = fields.Many2one('res.users', 'Responsible', required=True)
    review_date = fields.Date('Review Date', required=True)
    executed = fields.Boolean('Executed')
    hazard_id = fields.Many2one('mgmtsystem.hazard', 'Hazard', ondelete='cascade', select=True)


class mgmtsystem_hazard_residual_risk(models.Model):

    _name = "mgmtsystem.hazard.residual_risk"
    _description = "Residual Risks of hazard"

    # TODO: Check result
    def _compute_risk(self):
        self.env.user.company_id
        for residual_risk_id in self:
            if residual_risk_id.probability_id and residual_risk_id.severity_id and residual_risk_id.usage_id:
                residual_risk_id.risk = _parse_risk_formula(
                    mycompany.risk_computation_id.name,
                    obj.probability_id.value,
                    obj.severity_id.value,
                    obj.usage_id.value
                )
            else:
                residual_risk_id.risk = False

    name = fields.Char('Name', size=50, required=True, translate=True)
    probability_id = fields.Many2one('mgmtsystem.hazard.probability', 'Probability', required=True)
    severity_id = fields.Many2one('mgmtsystem.hazard.severity', 'Severity', required=True)
    usage_id = fields.Many2one('mgmtsystem.hazard.usage', 'Occupation / Usage')
    # TODO: Check result
    acceptability = fields.Boolean('Acceptability')
    justification = fields.Text('Justification')
    hazard_id = fields.Many2one('mgmtsystem.hazard', 'Hazard', ondelete='cascade', select=True)



class mgmtsystem_hazard(models.Model):

    _name = "mgmtsystem.hazard"
    _description = "Hazards of the health and safety management system"

    # TODO: Check result
    def _compute_risk(self):
        self.env.user.company_id
        for hazard_id in self:
            if hazard_id.probability_id and hazard_id.severity_id and hazard_id.usage_id:
                hazard_id.risk = _parse_risk_formula(
                    mycompany.risk_computation_id.name,
                    obj.probability_id.value,
                    obj.severity_id.value,
                    obj.usage_id.value
                )
            else:
                hazard_id.risk = False

    name = fields.Char('Name', size=50, required=True, translate=True)
    type_id = fields.Many2one('mgmtsystem.hazard.type', 'Type', required=True)
    hazard_id = fields.Many2one('mgmtsystem.hazard', 'Hazard', required=True)
    risk_type_id = fields.Many2one('mgmtsystem.hazard.risk.type', 'Risk Type', required=True)
    origin_id = fields.Many2one('mgmtsystem.hazard.origin', 'Origin', required=True)
    department_id = fields.Many2one('hr.department', 'Department', required=True)
    responsible_user_id = fields.Many2one('res.users', 'Responsible', required=True)
    analysis_date = fields.Date('Date', required=True)
    probability_id = fields.Many2one('mgmtsystem.hazard.probability', 'Probability', required=True)
    severity_id = fields.Many2one('mgmtsystem.hazard.severity', 'Severity', required=True)
    usage_id = fields.Many2one('mgmtsystem.hazard.usage', 'Occupation / Usage')
    # TODO: Check result
    risk = fields.Integer('Risk', compute='_compute_risk')
    acceptability = fields.Boolean('Acceptability')
    justification = fields.Text('Justification')
    control_measure_ids = fields.One2many('mgmtsystem.hazard.control_measure', 'hazard_id', 'Control Measures')
    test_ids = fields.One2many('mgmtsystem.hazard.test', 'hazard_id', 'Implementation Tests')
    residual_risk_ids = fields.One2many('mgmtsystem.hazard.residual_risk', 'hazard_id', 'Residual Risk Evaluations')
    company_id = fields.Many2one('res.company', 'Company', default=own_company)
