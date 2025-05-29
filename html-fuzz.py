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
        
        f = open(f"html-test/{cnt}.tmpl", "w")
        s = "<html>\n" + str(inp) + "\n</html>"
        f.write(s)
        f.close()
    

        # cur_pl = "{" + f'"NAME":"{pl}"' + "}"
        cur_pl = json.dumps({"html_payload": f'{pl}'})

        new_data = open(f"html-data/{cnt}.json", "w")
        new_data.write(cur_pl)
        new_data.close()

        
        #  ~/bin/go1.18 run gen_templ.go cnt

        a = subprocess.Popen([
                "go1.18/go1.18", "test", "-coverprofile",
                "report/html-report.txt", "-covermode", "count", "-coverpkg", "html/template", "."
            ])
        _ = a.wait()


        newcoverage = parse_report_file("report/html-report.txt")
        updatedcoverage, _ = merge_reports(updatedcoverage, newcoverage)
        with open('total_coverage-html.out', 'w') as cov:
            cov.write('mode: count\n')
            for i in updatedcoverage.items():
                cov.write(f'{i[0].replace("std/","")} {i[1][0]} {i[1][1]}')

        out = open(f"./html-html/{cnt}.html")
        gen = out.read()
        out.close()


        b = subprocess.Popen(['node', 'detect_alert.js'],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)
        b.stdin.write((os.getcwd()+(f'/html-html/{cnt}.html' + '\n')).encode())
        b.stdin.close()
        ans = b.stdout.readline()
        print("BROWSER OUT -------", ans)
        if b'pwned_succesfull' in ans and pl in gen:
            f = open(f"successful-html/{cnt}.html", "w")
            f.write(gen)
            f.close()
            break

        cnt += 1
    





html_grammar = {
    "<start>": ["<tags>"],
    "<tags>": ["<single><tags>", "<double><tags>", ""],
    "<single>": [
        # "< <payload> />"
        "<link <attr> />",
        "<img <attr> />",
        "<br />",
        "<meta <attr> />",
        "<input <attr> />",
        "<hr />",
        '< <text> />',
        "<!-- <text> -->"
    ],
    "<double>": [
        "<a <attr> > <text> </a>",
        "<body <attr> > <text> </body>",
        "<div <attr> > <text> </div>",
        "<p <attr> > <text> </p>",
        "<span <attr> > <text> </span>",
        "<h1 <attr> > <text> </h1>",
        "<h2 <attr> > <text> </h2>",
        "<li <attr> > <text> </li>",
        "<table <attr> > <text> </table>",
        "<tr <attr> > <text> </tr>",
        "<td <attr> > <text> </td>",
        "<th <attr> > <text> </th>"
    ],
    "<attr>": [
        "",
        'href="<url>" <attr>',
        'src="<url>" <attr>',
        'alt="<text>" <attr>',
        'class="<text>" <attr>',
        'style="<text>" <attr>',
        'title="<text>" <attr>',
        'name="<text>" <attr>',
        'type="<text>" <attr>',
        'value="<text>" <attr>',
        'data-<text>="<text>" <attr>',
        'onload="<text>" <attr>',
    ],
    "<url>": ["<scheme><domain>"],
    "<scheme>": ['http://', "https://", "javascript://", "file://", "<payload>"],
    "<domain>": ['google.com', "<payload>"],
    "<text>": ["123", "zxc <payload>", "qwe", "qWe", "<payload>"],
    "<payload>":["{{.html_payload}}"]
}

initial_inputs = [
'<img src="http://google.com"  />',
'<img src="{{.html_payload}}google.com"  />',
'< zxc {{.html_payload}} />', 
# "<body <attr> > <text> </body>",
'<body onload="{{.html_payload}}"  > qwe </body>',
'<body  > zxc {{.html_payload}} </body>',
'<img src="https://{{.html_payload}}"  />',
'<img src="javascript://{{.html_payload}}"  />',
'<img src="javascript://{{.html_payload}}"  /><p class="qwe"  > qwe </p>',
# '<p <attr> > <text> </p>'
'<p class="qwe"  > qwe </p>',
'<p class="zxc {{.html_payload}}"  > qWe </p>',
'<p class="qwe"  > zxc {{.html_payload}} </p>',
'<span class="qwe"  > zxc {{.html_payload}} </span>',
'<table class="qwe"  > zxc {{.html_payload}} </table>',
'<li class="qwe"  > zxc {{.html_payload}} </li>',
'<h1 class="qwe"  > zxc {{.html_payload}} </h1>',
'<h2 class="qwe"  > zxc {{.html_payload}} </h2>',
"<!-- {{.html_payload}} -->"

# '<{{.html_payload}}/>'

]

epp = custom_fuzzer(
    grammar=html_grammar,
    oracle=oracle,
    inputs=initial_inputs,
    iterations=100
)
cnt = 1
epp.fuzz()