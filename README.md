# Universal-template-fuzzing

Grammar based template fuzzing

# Usage

Go html/template fuzzing with coverage:
```
python3 html-fuzz.py
python3 css-fuzz.py
python3 js-fuzz.py
```

Twig, Django, Tornado fuzzing without coverage:

```
python3 universal_testgen.py <css/js/html> <Twig/Tornado/Django>
```

# Possible findings

Fuzzer can found:

- Lack of sanitization inside Django js literal context
- Lack of sanitization inside Tornado js literal context
- CVE-2023-24538