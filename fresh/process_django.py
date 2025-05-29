from django.template import Template, Context
import django.conf
import os
import json
import sys

def setup_django():
    if not django.conf.settings.configured:
        django.conf.settings.configure(TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    
                },
            },
        ])
    django.setup()

def process_template_django(id, payload_len):
    setup_django()
    template_path = f"./test_cases/{id}.tmpl"
    if not os.path.exists(template_path):
        print(f"Template file not found: {template_path}")
        return

    with open(template_path, "r") as f:
        template_str = f.read()

    for i in range(payload_len):
        payload_file = f"./payloads/{i}.json"
        if not os.path.exists(payload_file):
            print(f"Payload file not found: {payload_file}")
            continue

        with open(payload_file, "r") as f:
            payload_data = json.load(f)

        tmpl = Template(template_str)
        rendered_html = tmpl.render(Context(payload_data))

        os.makedirs("./html_outputs/", exist_ok=True)
        output_file = f"./html_outputs/{id}_{i}.html"
        with open(output_file, "w") as f:
            f.write(rendered_html)

        # print(f"Rendered HTML saved to: {output_file}")

if __name__ == "__main__":
    id = sys.argv[1]
    payload_len = int(sys.argv[2])
    process_template_django(id, payload_len)