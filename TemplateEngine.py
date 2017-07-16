# coding:utf-8
import re

"""
模板方式技术可以采用1.编译期间模板填充 2.运行期生成
这里采用运行期方式
将模板编译成python代码,执行时候只要传入需要参数就会自动生成HTML

引擎期望使用方式如下：
# Make a Templite object.
templite = Templite('''
    <h1>Hello {{name}}!</h1>
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

"""
CodeBuilder 方法

"""


class CodeBuilder(object):
    '''Build Source Code'''
    INDENT_STEPS = 4

    def __str__(self):
        return "".join([str(i) for i in self.code])

    def __init__(self, indent=0):
        self.code = []
        self.current_indent = indent

    def indent(self):
        self.current_indent += self.INDENT_STEPS

    def dedent(self):
        self.current_indent -= self.INDENT_STEPS

    def addLine(self, line):
        self.code.extend([" " * self.current_indent, line, "\n"])

    def add_section(self):
        section = CodeBuilder(self.current_indent)
        self.code.append(section)
        return section

    def get_globals(self):
        python_code = str(self)
        params = {}
        exec (python_code, params)
        return params


"""
    解析输入的html模板找出有多少变量 找出后定义到方法最前面
"""


class Template(object):
    def __init__(self, template_str):
        self.code = CodeBuilder()
        # 添加方法
        self.code.addLine("def generalHTML(context):")
        self.code.indent()
        # 定义一个装全局变量的容器
        self.all_vars = set()
        self.con_vars = set()
        # 转换context中变量为本地变量
        vars_code = self.code.add_section()

        # 定义一个结果列表和本地化方法
        self.code.addLine("result = []")
        self.code.addLine("append_result = result.append")
        self.code.addLine("extend_result = result.extend")
        self.code.addLine("to_str = str")
        # 定义buff缓冲
        buff = []

        # 定义刷新改buff
        def flush():
            if len(buff) == 1:
                self.code.addLine("append_result(%s)" % buff[0])
            elif len(buff) > 1:
                self.code.addLine("extend_result([%s])" % ', '.join(buff))
            else:
                pass
            del buff[:]

        # 解析输入模板
        tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", template_str)
        for item in tokens:
            if item.startswith('{#'):
                pass
            elif item.startswith('{{'):
                buff.append('to_str(%s)' % self.__expr__(item[2:-2]))
            elif item.startswith('{%'):
                flush()
                words = item[2:-2].strip().split()
                if words[0] == 'if':
                    self.code.addLine("if %s:" % self.__expr__(words[1]))
                    self.code.indent()
                elif words[0] == 'for':
                    self.con_vars.add(words[1])
                    self.code.addLine("for loc_%s in %s:" % (words[1], self.__expr__(words[3])))
                    self.code.indent()
                elif words[0] == 'end':
                    self.code.dedent()
            else:
                buff.append(repr(item))
        # 清空buff中内容
        flush()

        # 设置头部变量定义
        for key in self.all_vars - self.con_vars:
            vars_code.addLine("loc_%s = context[%r]" % (key, key))
        # 函數結束
        self.code.dedent()
        self.code.addLine("return ''.join(result)")

    def render(self, context):
        print str(self.code)
        print self.code.get_globals()['generalHTML'](context)

    def __expr__(self, expr):
        self.all_vars.add(expr)
        code = "loc_%s" % expr
        return code


#
template = Template('''
    <h1>Hello {{name}}!</h1>
    {% for topic in topics %}
        <p>You are interested in {{topic}}.</p>
    {% endfor %}
    ''')
template.render({"name": "tony", "topics": ["Study", "Money", "Beautiful Girl"]})


'''
def generalHTML(context):
    #枚举需要的变量
    loc_topics = context['topics']
    loc_name = context['name']
    
    #定义结果和函数本地化
    result = []
    append_result = result.append
    extend_result = result.extend
    to_str = str
    
    #拼接结果
    extend_result(['\n    <h1>Hello ', to_str(loc_name), '!</h1>\n    '])
    for loc_topic in loc_topics:
        extend_result(['\n        <p>You are interested in ', to_str(loc_topic), '.</p>\n    '])
        append_result('\n    ')
    return ''.join(result)

'''