import os
import subprocess
import json
from fuzzer import custom_fuzzer


updatedcoverage = {}

def parse_report_file(filename):
    result = {}
    with open(filename, 'r') as file:
        for i in file.readlines()[1:]:
            a = i.split(' ')
            result[a[0]] = (a[1], a[2])
    return result

def merge_reports(oldreport, newreport):
    result = False
    for key, value in newreport.items():
        if key not in oldreport or (int(oldreport[key][1]) == 0 and int(newreport[key][1]) != 0):
            result = True
        if key not in oldreport or int(newreport[key][1]) > int(oldreport[key][1]):
            oldreport[key] = value
    return oldreport, result

def oracle(inp: str):
    global cnt
    global updatedcoverage
    

    data = [
        "`; alert(1)`", "`--> alert(1)", 'javascript:alert(1)', "`- alert(1) -", 'javascript:alert`1`','${alert(1)}', "' alert(1)", '" alert(1)', 'alert(1)', 'alert`1`'
    ]

    for pl in data:
        
        f = open(f"css-test/{cnt}.tmpl", "w")
        s = "<html>\n<style>\n" + str(inp) + "\n</style>\n</html>"
        f.write(s)
        f.close()
    

        # cur_pl = "{" + f'"NAME":"{pl}"' + "}"
        cur_pl = json.dumps({"css_payload": f'{pl}'})

        new_data = open(f"css-data/{cnt}.json", "w")
        new_data.write(cur_pl)
        new_data.close()

        
        #  ~/bin/go1.18 run gen_templ.go cnt

        a = subprocess.Popen([
                "go1.18/go1.18", "test", "-coverprofile",
                "report/css-report.txt", "-covermode", "count", "-coverpkg", "html/template", "."
            ])
        _ = a.wait()


        newcoverage = parse_report_file("report/css-report.txt")
        updatedcoverage, _ = merge_reports(updatedcoverage, newcoverage)
        with open('total_coverage-css.out', 'w') as cov:
            cov.write('mode: count\n')
            for i in updatedcoverage.items():
                cov.write(f'{i[0].replace("std/","")} {i[1][0]} {i[1][1]}')

        out = open(f"html/css-{cnt}.html")
        gen = out.read()
        out.close()


        b = subprocess.Popen(['node', 'detect_alert.js'],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)
        b.stdin.write((os.getcwd()+(f'/html/css-{cnt}.html' + '\n')).encode())
        b.stdin.close()
        ans = b.stdout.readline()
        print("BROWSER OUT -------", ans)
        if b'pwned_succesfull' in ans and pl in gen:
            f = open(f"successful/css-{cnt}.html", "w")
            f.write(gen)
            f.close()
            break

        cnt += 1
    





css_grammar = {
    "<start>": ["<stylesheet>"],
    "<stylesheet>": ["<rule>", "/* {{.css_payload}} */<rule>", "/* {{.css_payload}} */"],
    "<rule>": [
        "<selectors> { <declarations> }", 
        "<media_query> { <rule> }",
    ],
    "<selectors>": [
        "<selector><combinator><selector>", 
        "<selector>"
    ],
    "<selector>": [
        "<element>", 
        "<id_selector>", 
        "<pseudo_class>", 
        "<pseudo_element>", 
        
    ],
    "<element>": ["div", "span", "p", "h1", "h2", "a", "*"],
    "<id_selector>": ["#<payload>"],
    "<pseudo_class>": [":hover", ":focus", ":nth-child(<number>)"],
    "<pseudo_element>": ["::before", "::after", "::first-letter"],
    "<combinator>": [" ", ">", "+", "~", ""],
    "<media_query>": [
        "@media (min-width: <value>)", 
        "@media (max-width: <value>)"
    ],
    "<declarations>": [
        "<declaration> <declarations>", 
        "<declaration>"
    ],
    "<declaration>": ["<property>: <value>;"],
    "<property>": [
        "color", "background-color", "font-size", "margin", "padding", 
        "display", "border", "width", "height", "position", "top", "left", "background", "content"
    ],
    "<value>": [
        "<color>", "<length>", "<percentage>", "<url>", "auto", "none", "block", "inline-block", "'<payload>'"
    ],
    "<color>": ["red", "blue", "green", "rgb(<number>, <number>, <number>)", "<payload>"],
    "<length>": ["<number>px", "<number>em", "<number>rem"],
    "<percentage>": ["<number>%"],
    "<number>": ["0", "1", "2", "10", "100", "50", "20", "<payload>"],
    "<url>": ["url('<payload>')"],
    "<payload>": ['{{.css_payload}}']
}

# initial_inputs = ["", '`${ {{.css_payload}} }`; ', '`${ function(){ return `{{.css_payload}}`; } }`; ', '<!-- var x = {{.css_payload}}; -->']

# initial_inputs = ["", '`${ {{.css_payload}} }`; ', '<!-- {{.css_payload}} -->', 'var x = {{.css_payload}};', 'if ({{.css_payload}} == true) { `${ {{.css_payload}} }`;  }; ', "#! let x = {{.css_payload}};\n", "(function(){ return `{{.css_payload}}`; })()", "`${ (function(){ return `{{.css_payload}}`; })() }`; ", "<!-- var x = {{.css_payload}}; -->" ]

initial_inputs = [
"span::before { content: '{{.css_payload}}'; }",
"div::before { color: rgb(1, {{.css_payload}}, 50); }",
'p { color: {{.css_payload}}; padding: 20%; margin: 10px; }', 
'p { color: red; padding: {{.css_payload}}; margin: 10px; }',
'p { color: red; padding: 20%; margin: {{.css_payload}}; }',
"a { background: url('{{.css_payload}}'); }", 
"/* {{.css_payload}} */",
"#{{.css_payload}} { color: red; }"
]

epp = custom_fuzzer(
    grammar=css_grammar,
    oracle=oracle,
    inputs=initial_inputs,
    iterations=100
)
cnt = 1
epp.fuzz()