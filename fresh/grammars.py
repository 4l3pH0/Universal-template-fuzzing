css_grammar = {
    "<start>": ["<stylesheet>"],
    "<stylesheet>": ["<rule>", "/* TERM */<rule>", "/* TERM */"],
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
    "<payload>": ['TERM']
}

html_grammar = {
    "<start>": ["<tags>"],
    "<tags>": ["<single> <tags>", "<double> <tags>", ""],
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
    "<payload>":["TERM"]
}

js_grammar = {
    "<start>": ["<code>"],
    "<code>": ["<js>", "<hashbang><js>"],
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
    "<stringliteral>": ["TERM"],
    "<array>": ["[<stringliteral>, <stringliteral>, <stringliteral>]"],
    "<maybe_value>": ["", "`<value>`", "<value>"]
}

