import random
import re
import subprocess
import os
import json
from collections import defaultdict

class GrammarGenerator:
    def __init__(self, grammar: dict, term: str):
        self.grammar = grammar
        self.term = term
        self.usage_counts = defaultdict(int)
    
    def generate_test(self, start_symbol="<start>"):
        return self._expand(start_symbol)
    
    def _expand(self, symbol, depth=0, max_depth=20):
        if depth > max_depth:
            return ""  # stop recursion with empty string

        if symbol not in self.grammar:
            return symbol.replace("TERM", self.term)

        choices = self.grammar[symbol]
        weights = [1 / (1 + self.usage_counts[choice]) for choice in choices]
        production = random.choices(choices, weights=weights)[0]
        self.usage_counts[production] += 1

        parts = re.findall(r'<[^>]+>|[^<>]+', production)
        return "".join(self._expand(part, depth + 1, max_depth) for part in parts).replace("TERM", self.term)
 


class Oracle:
    def __init__(self):
        self.engine_commands = {
            "Go": "go run process_template.go",
            "Django": "python process_django.py",
            "Jinja": "python process_template.py",
            "Twig": "php process_twig.php",
            "Tornado": "python process_tornado.py"
        }
        self.payload_dir = "./payloads"
        self.test_case_dir = "./test_cases"
        self.html_output_dir = "./html_outputs"
        os.makedirs(self.payload_dir, exist_ok=True)
        os.makedirs(self.test_case_dir, exist_ok=True)
        os.makedirs(self.html_output_dir, exist_ok=True)

    def test_input(self, engine: str, test_case: str, test_id: int):
        if engine not in self.engine_commands:
            raise ValueError(f"Unsupported engine: {engine}")
        
        test_case_path = os.path.join(self.test_case_dir, f"{test_id}.tmpl")
        with open(test_case_path, "w") as f:
            f.write(test_case)
        
        for i, payload in enumerate(self.generate_payloads(), start=0):
            json_path = os.path.join(self.payload_dir, f"{i}.json")
            with open(json_path, "w") as json_file:
                json.dump({"TEMPL_STR": payload}, json_file)
        
        command = self.engine_commands[engine]
        subprocess.run(command + " " + str(test_id) + " " + str(len(self.generate_payloads())), shell=True)
        
        self.detect_xss(test_id)
    
    def generate_payloads(self):
        return [
            "`; alert(1)`", "`--> alert(1)", 'javascript:alert(1)', "`- alert(1) -", 'javascript:alert`1`',
            "${alert(1)}", "' alert(1)", '" alert(1)', 'alert(1)', 'alert`1`'
        ]
    
    def detect_xss(self, test_id: int):
        html_path = os.path.join(self.html_output_dir, f"{test_id}.html")
        
        check_process = subprocess.run(
            ['node', 'alert.js', html_path], 
            capture_output=True, 
            text=True
        )

        output = check_process.stdout.strip()
        
        if "pwned_successful" in output:
            print(f"!!!!!!! XSS detected in {test_id}.tmpl")
            
            os.makedirs("./successful_templ", exist_ok=True)
            os.makedirs("./successful_html", exist_ok=True)
            
            successful_tmpl_path = f"./successful_templ/{test_id}.tmpl"
            with open(successful_tmpl_path, "w") as f:
                with open(f"./test_cases/{test_id}.tmpl", "r") as original:
                    f.write(original.read())

            successful_html_path = f"./successful_html/{test_id}.html"
            with open(successful_html_path, "w") as f:
                with open(html_path, "r") as original:
                    f.write(original.read())
        else:
            print(f"No XSS detected in {test_id}.tmpl")