// coa_translator/coa_translator/doctype/account_translation/account_translation.js
frappe.ui.form.on('Account Translation', {
    refresh: function(frm) {
        frm.add_custom_button(__('Fetch Accounts'), function() {
            frm.call({
                doc: frm.doc,
                method: 'fetch_accounts',
                callback: function(r) {
                    frm.refresh();
                }
            });
        });
        
        frm.add_custom_button(__('Auto Translate'), function() {
            frappe.confirm(
                'This will start auto-translation using MyMemory API. Continue?',
                function() {
                    frm.call({
                        doc: frm.doc,
                        method: 'translate_accounts',
                        callback: function(r) {
                            frm.refresh();
                        }
                    });
                }
            );
        });
        
        frm.add_custom_button(__('Save Translations'), function() {
            frappe.confirm(
                'This will update all accounts with the translated names. Continue?',
                function() {
                    frm.call({
                        doc: frm.doc,
                        method: 'save_translations',
                        callback: function(r) {
                            frm.refresh();
                        }
                    });
                }
            );
        });
    }
});
