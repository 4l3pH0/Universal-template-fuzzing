from grammar_generator import GrammarGenerator
from grammar_generator import Oracle
from grammars import html_grammar
from grammars import css_grammar
from grammars import js_grammar
import sys


N_iters = 100


gen_type = sys.argv[1]
templ_kind = sys.argv[2]


universal_testgen = {
    "Go": {"engine": "html/template", "template_string": "{{TEMPL_STR}}"},
    "Tornado": {"engine": "Tornado", "template_string": "{{ escape(TEMPL_STR) }}"},
    "Django": {"engine": "Django", "template_string": "{{ TEMPL_STR }}"},
    "Twig": {"engine": "Twig", "template_string": "{{ TEMPL_STR }}"}
}


target = universal_testgen[templ_kind]

if gen_type == "html":
    gg = GrammarGenerator(grammar=html_grammar, term=target["template_string"])
elif gen_type == "css":
    gg = GrammarGenerator(grammar=css_grammar, term=target["template_string"])
elif gen_type == "js":
    gg = GrammarGenerator(grammar=js_grammar, term=target["template_string"])

oracle = Oracle()


for i in range(N_iters):
    if gg.grammar == css_grammar:
        test_case = "<html><head><style>" + gg.generate_test() + "</style></head></html>"
    elif gg.grammar == js_grammar:
        test_case = "<html><script>" + gg.generate_test() + "</script></html>"
    elif gg.grammar == html_grammar:
        test_case = "<html>" + gg.generate_test() + "</html>"
        
    oracle.test_input(engine=target["engine"], test_case=test_case, test_id=i)






