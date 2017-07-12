# coding:utf-8

'''
精简版本
使用字符串拼接方式
优点：简单
缺点：随着模板的修改每次需要修改python生成代码
<p>Welcome, Charlie!</p>
<p>Products:</p>
<ul>
    <li>Apple: $1.00</li>
    <li>Fig: $1.50</li>
    <li>Pomegranate: $3.25</li>
</ul>
'''

PAGE_HTML = """
<p>Welcome, {name}!</p>
<p>Products:</p>
<ul>
{products}
</ul>
"""

PRODUCT_HTML = '<li>{prodname}:{price}</li>'


def make_html(user_name, prods):
    out_html = PAGE_HTML
    prods_html = ''
    for pro_name, price in prods:
        prods_html += PRODUCT_HTML.format(prodname=pro_name, price=price)
    out_html = PAGE_HTML.format(name=user_name, products=prods_html)
    print out_html


products = [('cocoa', 1.8), ('sprite', '2')]
make_html('tony', products)
