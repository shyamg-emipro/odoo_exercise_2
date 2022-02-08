from odoo import models, fields, api


class Lead(models.Model):
    _name = "crm.lead.ept"
    _description = "CRM Lead"

    partner_id = fields.Many2one(comodel_name="res.partner.ept", string="Partner", help="Customer")
    order_ids = fields.One2many(comodel_name="sale.order.ept", inverse_name="lead_id", string="Orders",
                                help="Order generated by this lead", readonly=True)
    team_id = fields.Many2one(comodel_name="crm.team.ept", string="Team", help="Team who generated this lead")
    user_id = fields.Many2one(comodel_name="res.users", string="Sales Person",
                              help="Sales Person who generated this lead")
    lead_line_ids = fields.One2many(comodel_name="crm.lead.line.ept", inverse_name="lead_id", string="Lead Lines",
                                    help="Product and it's quantity")
    state = fields.Selection(string="State",
                             help="State of the Lead",
                             selection=[('New', 'New'), ('Qualified', 'Qualified'), ('Proposition', 'Proposition'),
                                        ('Won', 'Won'), ('Lost', 'Lost')],
                             default="New")
    won_date = fields.Date(string="Won Date", help="Date at which the lead is won", readonly=True)
    lost_reason = fields.Char(string="Lost Reason", help="Reason behind the loss of lead")
    next_followup_date = fields.Date(string="Follow Up Date",
                                     help="Date at which follow up from the customer has to be taken")
    partner_name = fields.Char(string="Partner Name", help="Name of the partner")
    partner_email = fields.Char(string="Partner Email", help="Email address of the partner")
    partner_country_id = fields.Many2one(comodel_name="res.country.ept", string="Country",
                                         help="Country where partner lives")
    partner_state_id = fields.Many2one(comodel_name="res.state.ept", string="State",
                                       help="State where partner lives")
    partner_city_id = fields.Many2one(comodel_name="res.city.ept", string="City",
                                      help="City where partner lives")
    partner_phone_no = fields.Char(string="Partner Phone No", help="Phone number of the partner")

    def change_state_to_qualified(self):
        self.state = "Qualified"

    def change_state_to_proposition(self):
        self.state = "Proposition"

    def change_state_to_won(self):
        self.state = "Won"
        self.won_date = fields.Datetime.today()

    def change_state_to_lost(self):
        self.state = "Lost"

    def generate_sales_quotation(self):
        order_line_data = []
        values = {'partner_id': self.partner_id}
        temp = self.env['sale.order.ept'].new(values)
        temp.onchange_partner_id()
        for line in self.lead_line_ids:
            order_line_data.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.expected_sell_qty,
                'unit_price': line.product_id.sale_price,
                'uom_id': line.uom_id.id
            }))
        order = self.env['sale.order.ept'].create({
            'partner_id': self.partner_id.id,
            'partner_invoice_id': temp.partner_invoice_id.id,
            'partner_shipping_id': temp.partner_shipping_id.id,
            'salesperson': self.user_id.id,
            'lead_id': self.id,
            'order_lines': order_line_data
        })

    def generate_customer(self):
        new_partner = self.env['res.partner.ept'].create({
            'name': self.partner_name,
            'country': self.partner_country_id.id,
            'state': self.partner_state_id.id,
            'city': self.partner_city_id.id,
            'email': self.partner_email,
            'mobile': self.partner_phone_no,
            'phone': self.partner_phone_no,
            'active': True,
            'address_type': "Invoice"
        })

        self.env['res.partner.ept'].create({
            'name': self.partner_name,
            'country': self.partner_country_id.id,
            'state': self.partner_state_id.id,
            'city': self.partner_city_id.id,
            'email': self.partner_email,
            'mobile': self.partner_phone_no,
            'phone': self.partner_phone_no,
            'active': True,
            'address_type': "Invoice",
            'parent_id': new_partner.id
        })

        self.env['res.partner.ept'].create({
            'name': self.partner_name,
            'country': self.partner_country_id.id,
            'state': self.partner_state_id.id,
            'city': self.partner_city_id.id,
            'email': self.partner_email,
            'mobile': self.partner_phone_no,
            'phone': self.partner_phone_no,
            'active': True,
            'address_type': "Shipping",
            'parent_id': new_partner.id
        })

        self.partner_id = new_partner.id