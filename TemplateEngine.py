# coding:utf-8

"""
模板方式技术可以采用1.编译期间模板填充 2.运行期生成
这里采用运行期方式
将模板编译成python代码,执行时候只要传入需要参数就会自动生成HTML

引擎期望使用方式如下：
# Make a Templite object.
templite = Templite('''
    <h1>Hello {{name|upper}}!</h1>
    {% for topic in topics %}
        <p>You are interested in {{topic}}.</p>
    {% endfor %}
    ''',
    {'upper': str.upper},
)

# Later, use it to render some data.
text = templite.render({
    'name': "Ned",
    'topics': ['Python', 'Geometry', 'Juggling'],
})
"""
'''
解析exec怎麼使用,exec用於執行文本快 如下
python_source = """
SEVENTEEN = 17
def three():
    return 3
"""

global_namespace = {}
exec(python_source, global_namespace)
print global_namespace['three']()

這樣source的代碼都會注入到global_namespace空間裡面並且使用
global_namespace裡面的變量 這樣我們把我們的變量直接放入
global_namespace這樣代碼裡面就會實時變化
'''
