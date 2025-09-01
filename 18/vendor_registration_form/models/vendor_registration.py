from odoo import models, fields, api, _
from odoo.exceptions import UserError


class VendorRegistration(models.Model):
    _name = 'vendor.registration'
    _description = 'Vendor Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Company Name", required=True)
    business_type = fields.Selection([('one', 'Micro Enterprises'), ('two', 'Small Enterprises'), ('three', 'Medium Enterprises')], required=True)
    products_services = fields.Text(string="Products/Services Offered")
    website = fields.Char(string="Company Website")
    #company_address = fields.Char(string="Company address")
    street1 = fields.Char(string="Company Address")
    street2 = fields.Char(string="Street Address 2")
    city = fields.Many2one('partner.city')
    region = fields.Many2one('res.country.state')
    postal_code = fields.Char()
    country = fields.Many2one('res.country')
    company_info = fields.Text(string="Company Background Info")
    representative_name = fields.Char(string="Representative Name")
    email = fields.Char()
    phone = fields.Char()
    download_form = fields.Boolean(string="Downloaded Form", default=False)
    uploaded_form = fields.Binary(string="Registration Application Form")
    uploaded_form_filename = fields.Char()
    vendor_category = fields.Char(string="Vendor Category")
    id_authorised = fields.Binary(string="ID of authorized signature")
    id_authorised_filename = fields.Char()
    id_authorised_attachment_id = fields.Many2one('ir.attachment', string="ID of authorized signature")

    cr_copy = fields.Binary(string="CR Copy")
    cr_copy_filename = fields.Char()
    cr_copy_attachment_id = fields.Many2one('ir.attachment', string="CR Copy")

    vat_certificate = fields.Binary(string="Vat Certificate")
    vat_certificate_filename = fields.Char()
    vat_certificate_attachment_id = fields.Many2one('ir.attachment', string="Vat Certificate")

    tax_certificate = fields.Binary(string="Tax Certificate")
    tax_certificate_filename = fields.Char()
    tax_certificate_attachment_id = fields.Many2one('ir.attachment', string="Tax Certificate")

    stamped_bank_account = fields.Binary(string="Stamped Bank Account")
    stamped_bank_account_filename = fields.Char()
    stamped_bank_account_attachment_id = fields.Many2one('ir.attachment', string="Stamped Bank Account")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('purchase_user', 'Purchase User'),
        ('legal', 'Legal Review'),
        ('senior_accountant', 'Senior Accountant Review'),
        ('approved', 'Approved'),
        ('done', 'Vendor Created'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ], default='draft', string="Status", tracking=True)
    rejection_reason = fields.Text(string="Rejection Reason")
    partner_id = fields.Many2one('res.partner', string="Created Vendor")
    uploaded_form_attachment_id = fields.Many2one('ir.attachment', string='Uploaded Form')
    vendor_created = fields.Boolean(string="Vendor Created", default=False)

    def action_download_uploaded_form(self):
        """Return an action that downloads the attachment."""
        self.ensure_one()
        if not self.uploaded_form_attachment_id:
            return

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self.uploaded_form_attachment_id.id}?download=true',
            'target': 'new',
        }
        
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_send_to_purchase(self):
        for rec in self:
            rec.state = 'purchase_user'     

    def action_send_to_legal(self):
        for rec in self:
            rec.state = 'legal'  

    def action_send_to_senior_accountant(self):
        for rec in self:
            rec.state = 'senior_accountant'       

    def action_approve(self):
        for rec in self:
           rec.state = 'approved'

    def action_create_vendor(self):
        for rec in self:
            # Create a vendor record
            partner = self.env['res.partner'].create({
                'name': rec.name,
                'website': rec.website,
                'street': rec.street1,
                'street2': rec.street2,
                'city_id': rec.city.id,
                'state_id': rec.region.id,  # Optional: match by region if using states
                'zip': rec.postal_code,
                'country_id': rec.country.id,  # Optional: match by country if you convert `country` to a Many2one
                'email': rec.email,
                'phone': rec.phone,
                'comment': rec.company_info,
                'supplier_rank': 1,
            })
            rec.partner_id = partner.id
            rec.vendor_created = True

    def action_reject(self):
        for rec in self:
            if not rec.rejection_reason:
                raise UserError("Please provide a reason for rejection.")
            rec.state = 'rejected'
            if rec.email:
                template = self.env.ref('vendor_registration_form.vendor_rejection_email_template')
                template.send_mail(rec.id, force_send=True)        
                  
    def action_download_id_authorised(self):
        self.ensure_one()
        if not self.id_authorised_attachment_id:
            return
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self.id_authorised_attachment_id.id}?download=true',
            'target': 'new',
        }

                  
    def _compute_docs_readonly(self):
        for rec in self:
            rec.docs_readonly = rec.state != 'draft'

    docs_readonly = fields.Boolean(compute='_compute_docs_readonly', store=False)
    
    def action_view_vendor(self):
        return {
            'name': 'Vendor',
            'view_mode': 'form',
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
            'target': 'current',
            'type': 'ir.actions.act_window',
        }
