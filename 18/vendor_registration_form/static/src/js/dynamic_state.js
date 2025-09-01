odoo.define('vendor_registration_form.vendor_state_loader', function(require){
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.VendorStateLoader = publicWidget.Widget.extend({
        selector: 'form',
        events: {
            'change #country_id': '_onCountryChange',
        },

        _onCountryChange: function(ev){
            var countryId = $(ev.target).val();
            var $stateSelect = $('#state_id');
            
            $stateSelect.empty();
            if (countryId){
                this._rpc({
                    route: '/get/states',
                    params: { country_id: parseInt(countryId) },
                }).then(function(states){
                    $stateSelect.append('<option value="">Select State</option>');
                    states.forEach(function(state){
                        $stateSelect.append(`<option value="${state.id}">${state.name}</option>`);
                    });
                });
            }
        },
    });

    return publicWidget.registry.VendorStateLoader;
});
