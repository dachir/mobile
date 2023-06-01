import frappe
import json
from mobile.utils.permission_manager import hash_string

def hash_doctype(name):
    frappe.set_user("Administrator")

    # Load the document
    doc = frappe.get_doc("DocType", name)

    # Convert the document to a dictionary and hash
    doc_dict = json.loads(frappe.as_json(doc))
    hash_doctype = hash_string(doc_dict)

    # Save to Hash Doctype
    if len(frappe.db.get_list('Hash Doctype', {'name' : 'name'})) != 0:
        doc_name = frappe.get_doc("Hash Doctype", name)
        doc_name.delete()

    frappe.get_doc({
        'doctype': 'Hash Doctype',
        'doctype_name': name,
        'hash': hash_doctype,
    }).insert()

    frappe.set_user(frappe.session.user)

def get_module_doctype(user):
    pass
