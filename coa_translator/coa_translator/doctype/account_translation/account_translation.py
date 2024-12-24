# coa_translator/coa_translator/doctype/account_translation/account_translation.py
import frappe
from frappe.model.document import Document
import requests
import json

class AccountTranslation(Document):
    @frappe.whitelist()
    def fetch_accounts(self):
        accounts = frappe.get_all("Account", 
            fields=["name", "account_name"],
            filters={"is_group": 0},
            order_by="name"
        )

        self.translations = []
        for account in accounts:
            self.append("translations", {
                "account": account.name,
                "account_name": account.account_name,
                "translated_name": ""
            })

        self.progress_bar = 0
        self.save()

    @frappe.whitelist()
    def translate_accounts(self):
        total = len(self.translations)
        for idx, row in enumerate(self.translations):
            if not row.translated_name:
                try:
                    url = f"https://api.mymemory.translated.net/get?q={row.account_name}&langpair=en|ar"
                    response = requests.get(url)
                    data = response.json()
                    row.translated_name = data['responseData']['translatedText']
                except Exception as e:
                    frappe.log_error(f"Translation error for {row.account_name}: {str(e)}")

            self.progress_bar = ((idx + 1) / total) * 100
            self.save()
            frappe.db.commit()

    @frappe.whitelist()
    def save_translations(self):
        for row in self.translations:
            if row.translated_name:
                account = frappe.get_doc("Account", row.account)
                account.account_name_arabic = row.translated_name
                account.save()

        frappe.msgprint("Translations saved successfully!")
