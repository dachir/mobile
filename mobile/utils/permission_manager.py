import frappe
from frappe.core.page.permission_manager.permission_manager import get_permissions
import hashlib

@frappe.whitelist()
def get_user_permissions(user: str):
	#frappe.only_for("System Manager")
    #if user != frappe.session.user:
    #    return
    
    user_doc = frappe.get_doc("User", user)
    if not user_doc: 
        return 

    frappe.set_user("Administrator")
    roles = []
    for role in user_doc.roles:
        permissions = get_permissions(None, role.role)
        role_doc = frappe._dict({
            "name": role.name,
            "role": role.role,
            "permissions": permissions
        })
        roles.append(role_doc)

    modules = frappe.db.sql(
        '''
            SELECT m.name, m.app_name
            FROM (
                SELECT name, app_name, %(user)s AS user 
                FROM `tabModule Def`
            ) AS m LEFT JOIN `tabBlock Module`b ON m.name = b.module AND m.user = b.parent
            WHERE m.user = %(user)s AND  b.module IS NULL
        ''',{"user":user }, as_dict =True,
    )

    permissions_doc_copy = frappe._dict({
        "name": user_doc.name,
        "username": user_doc.username,
        "mobile_no": user_doc.mobile_no,
        "roles": roles,
        "modules": modules,
    })

    permissions_doc = frappe._dict({
        "name": user_doc.name,
        "username": user_doc.username,
        "mobile_no": user_doc.mobile_no,
        "roles": roles,
        "modules": modules,
        "hash": hash_string(permissions_doc_copy),
    })

    frappe.set_user(frappe.session.user)
    return permissions_doc

def hash_string(doc_string):
    sorted_chars = sorted(doc_string)
    sorted_string = ''.join(sorted_chars)

    # Create a hash object using the SHA-256 algorithm
    hash_object = hashlib.sha256()

    # Update the hash object with the data
    hash_object.update(sorted_string.encode())   

    # Get the hash digest as a hexadecimal string
    return hash_object.hexdigest()