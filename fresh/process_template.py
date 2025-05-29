import json
import sys
import os
from jinja2 import Template

def process_template(id, payload_len):
    template_path = "./test_cases"
    payload_path = "./payloads"
    output_path = "./html_outputs"
    
    if not os.path.exists(template_path):
        print(f"Template file not found: {template_path}/{id}.tmpl")
        return
    with open(f"{template_path}/{id}.tmpl", "r") as f:
        template_str = f.read()
    
    
    for i in range(payload_len):
        if not os.path.exists(payload_path):
            print(f"Payload file not found: {payload_path}/{id}.json")
            return
        with open(f"{payload_path}/{i}.json", "r") as f:
            payload_data = json.load(f)
        
        template = Template(template_str)
        rendered_html = template.render(payload_data)
        
        os.makedirs("./html_outputs/", exist_ok=True)
        with open(f"{output_path}/{id}_{i}.html", "w") as f:
            f.write(rendered_html)
        
        # print(f"Rendered HTML saved to: {output_path}")

if __name__ == "__main__":
    id = sys.argv[1]
    payload_len = int(sys.argv[2])
    # print(id)
    process_template(id, payload_len)