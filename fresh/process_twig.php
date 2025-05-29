<?php

require_once 'vendor/autoload.php';
error_reporting(0);
use Twig\Environment;
use Twig\Loader\ArrayLoader;

function process_template($id, $payload_len) {
    
    $template_path = "./test_cases";
    $payload_path = "./payloads";
    $output_path = "./html_outputs";

    if (!file_exists("$template_path/$id.tmpl")) {
        echo "Template file not found: $template_path/$id.tmpl\n";
        return;
    }

    $loader = new \Twig\Loader\ArrayLoader([
        'template' => file_get_contents("$template_path/$id.tmpl")
    ]);
    $twig = new \Twig\Environment($loader);

    for ($i = 0; $i < $payload_len; $i++) {
        $payload_file = "$payload_path/$i.json";
        if (!file_exists($payload_file)) {
            echo "Payload file not found: $payload_file\n";
            continue;
        }

        $payload_data = json_decode(file_get_contents($payload_file), true);
        if ($payload_data === null) {
            echo "Invalid JSON in payload $i\n";
            continue;
        }

        try {
            $rendered = $twig->render('template', $payload_data);
        } catch (Exception $e) {
            echo "Twig rendering failed for $id/$i: ", $e->getMessage(), "\n";
            continue;
        }

        if (!file_exists($output_path)) {
            mkdir($output_path, 0777, true);
        }

        file_put_contents("$output_path/{$id}_{$i}.html", $rendered);
        // echo "Rendered HTML saved to: $output_path/{$id}_{$i}.html\n";
    }
}

require_once 'vendor/autoload.php';

if ($argc !== 3) {
    echo "Usage: php process_template.php <id> <payload_len>\n";
    exit(1);
}

process_template($argv[1], intval($argv[2]));
