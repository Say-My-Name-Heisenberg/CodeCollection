from odoo import http
from odoo.http import request
import base64

class VendorRegistrationController(http.Controller):
    @http.route('/vendor/registration', auth='public', website=True)
    def portal_vendor_registration(self, **kwargs):
        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        cities = request.env['partner.city'].sudo().search([])
        return request.render('vendor_registration_form.vendor_registration_form_template', {'countries': countries,'states':states,'cities':cities})
    
    @http.route('/get/states', type='json', auth='public')
    def get_states(self, country_id):
        states = request.env['res.country.state'].sudo().search([('country_id', '=', int(country_id))])
        return [{'id': s.id, 'name': s.name} for s in states]

    @http.route('/portal/vendor/registration/submit', type='http', auth='public', website=True, csrf=True)
    def vendor_submit(self, **post):
        def read_file(field_name):
            file = request.httprequest.files.get(field_name)
            if file:
                return base64.b64encode(file.read()), file.filename
            return False, False

        uploaded_form, uploaded_form_filename = read_file('uploaded_form')
        id_authorised, id_authorised_filename = read_file('id_authorised')
        cr_copy, cr_copy_filename = read_file('cr_copy')
        vat_certificate, vat_certificate_filename = read_file('vat_certificate')
        tax_certificate, tax_certificate_filename = read_file('tax_certificate')
        stamped_bank_account, stamped_bank_account_filename = read_file('stamped_bank_account')

        vendor = request.env['vendor.registration'].sudo().create({
            'name': post.get('name'),
            'business_type': post.get('business_type'),
            'products_services': post.get('products_services'),
            'vendor_category': post.get('vendor_category'),
            'website': post.get('website'),
            'street1': post.get('street1'),
            'street2': post.get('street2'),
            'city': int(post.get('city_id')) if post.get('city_id') else False,
            'region': int(post.get('state_id')) if post.get('state_id') else False,
            'postal_code': post.get('postal_code'),
            'country': int(post.get('country_id')) if post.get('country_id') else False,
            'company_info': post.get('company_info'),
            'representative_name': post.get('representative_name'),
            'email': post.get('email'),
            'phone': post.get('phone'),

            'uploaded_form': uploaded_form,
            'uploaded_form_filename': uploaded_form_filename,

            'id_authorised': id_authorised,
            'id_authorised_filename': id_authorised_filename,

            'cr_copy': cr_copy,
            'cr_copy_filename': cr_copy_filename,

            'vat_certificate': vat_certificate,
            'vat_certificate_filename': vat_certificate_filename,

            'tax_certificate': tax_certificate,
            'tax_certificate_filename': tax_certificate_filename,

            'stamped_bank_account': stamped_bank_account,
            'stamped_bank_account_filename': stamped_bank_account_filename,
        })

        return request.render('vendor_registration_form.vendor_created_success_template')
