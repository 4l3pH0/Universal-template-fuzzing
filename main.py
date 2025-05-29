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
        "`; alert(1)`", "`--> alert(1)", "`- alert(1) -", '${alert(1)}', "' alert(1)", '" alert(1)', 'alert(1)'
    ]

    for pl in data:
        
        f = open(f"tests/{cnt}.tmpl", "w")
        s = "<html>\n<script>\n" + str(inp) + "\n</script>\n</html>"
        f.write(s)
        f.close()
    

        # cur_pl = "{" + f'"NAME":"{pl}"' + "}"
        cur_pl = json.dumps({"js_payload": f'{pl}'})

        new_data = open(f"data/{cnt}.json", "w")
        new_data.write(cur_pl)
        new_data.close()

        
        #  ~/bin/go1.18 run gen_templ.go cnt

        a = subprocess.Popen([
                "go1.18/go1.18", "test", "-coverprofile",
                "report/report.txt", "-covermode", "count", "-coverpkg", "html/template", "."
            ])
        _ = a.wait()


        newcoverage = parse_report_file("report/report.txt")
        updatedcoverage, _ = merge_reports(updatedcoverage, newcoverage)
        with open('total_coverage.out', 'w') as cov:
            cov.write('mode: count\n')
            for i in updatedcoverage.items():
                cov.write(f'{i[0].replace("std/","")} {i[1][0]} {i[1][1]}')

        out = open(f"html/{cnt}.html")
        gen = out.read()
        out.close()

        

        b = subprocess.Popen(['node', 'detect_alert.js'],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)
        b.stdin.write((os.getcwd()+(f'/html/{cnt}.html' + '\n')).encode())
        b.stdin.close()
        ans = b.stdout.readline()
        print("BROWSER OUT -------", ans)
        if b'pwned_succesfull' in ans and pl in gen:
            f = open(f"successful/{cnt}.html", "w")
            f.write(gen)
            f.close()
            break

        cnt += 1
    




grammar = {
    "<start>": ["<code>"],
    "<code>": ["<hashbang><js>"],
    "<hashbang>": ["", "#! <expr>\n"],
    # "<js>": ["<template_string>", "<htmlthing>", "<if_else>", "<forcycle>"],

    "<js>": ["<statement>"],
    "<statement>": [
                    "", 
                    "<assign><statement>", 
                    "<forstatement><statement>", 
                    "<funcstatement><statement>", 
                    "<ifstatement><statement>",
                    "<importstatement><statement>",
                    "<htmlcomment><statement>",
                    "<exportstatement><statement>",
                    "<yieldstatement><statement>",
                    "<template_string><statement>"
                    ],

    "<importstatement>": ["import {<stringliteral>}; "],
    "<exportstatement>": ["export <assign>; "],
    "<yieldstatement>": ["yield <stringliteral>; "],

    "<forstatement>": ["for (<expr>, <expr>, <expr>) { <statement> }; "],
    "<funcstatement>": ["(function(){ <funcbody> })()"],
    
    "<template_string>": ["`${ <expr> }`; ", "`${ <statement> }`; "],
    "<htmlcomment>": ["<!-- <expr> -->"],
    

    "<ifstatement>": ["if (<expr> == true) { <statement> }<maybe_else>; "],
    "<maybe_else>": ["", "else{ <statement> }"],
    
    "<expr>": [
        "x += <value>",
        "x -= <value>",
        "x *= <value>",
        "x /= <value>",
        "x %= <value>",
        "x **= <value>",
        "x <<= <value>",
        "x >>= <value>",
        "x |= <value>",
        "x ||= <value>",
        "x &= <value>",
        "<statement>",
        "<value>",
        "<assign>"
        ],


    "<funcbody>": ["<statement>return <maybe_value>;"],
    "<assign>": ["var x = <value>;", "const x = <value>;", "let x = <value>;"],
    "<value>": ["<stringliteral>", "<array>", "<template_string>"],
    "<stringliteral>": ["{{.js_payload}}"],
    "<array>": ["[<stringliteral>, <stringliteral>, <stringliteral>]"],
    "<maybe_value>": ["", "`<value>`", "<value>"]
}

# initial_inputs = ["", '`${ {{.js_payload}} }`; ', '`${ function(){ return `{{.js_payload}}`; } }`; ', '<!-- var x = {{.js_payload}}; -->']

initial_inputs = ["", '`${ {{.js_payload}} }`; ', '<!-- {{.js_payload}} -->', 'var x = {{.js_payload}};', 'if ({{.js_payload}} == true) { `${ {{.js_payload}} }`;  }; ', "#! let x = {{.js_payload}};\n", "(function(){ return `{{.js_payload}}`; })()", "`${ (function(){ return `{{.js_payload}}`; })() }`; ", "<!-- var x = {{.js_payload}}; -->" ]

epp = custom_fuzzer(
    grammar=grammar,
    oracle=oracle,
    inputs=initial_inputs,
    iterations=10
)
cnt = 1
epp.fuzz()