from odoo import models, fields


class CrmLeadExtended(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"

    def action_new_quotation(self):
        action = super(CrmLeadExtended, self).action_new_quotation()
        # tag_ids = [(6, 0, action['context']['default_tag_ids'][0][2].append(self.env.ref("sale_order_extended.crm_tags_sale_order_extended").id))]
        action['context']['default_lead_id'] = self.id
        # action['context']['default_tag_ids'] = tag_ids
        return action
