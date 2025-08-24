import odoorpc
import json

db_name = 'odoo_18_enterprise'
user_name = 'admin'
password = 'admin'

# 准备对服务端的连接
odoo = odoorpc.ODOO('localhost', port=8092)
odoo.login(db_name, user_name, password) # login
service = odoo.env['intelligent.customer.service']

geo_info = service.browse(3).get_geo_info('59.174.16.231')

with open('geo_info.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(geo_info, ensure_ascii=False, indent=4))

print(geo_info)

