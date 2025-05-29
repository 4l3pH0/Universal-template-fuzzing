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


jscoverage = parse_report_file("./css_and_js_total_coverage.out")
csscoverage = parse_report_file("./total_coverage-html.out")
updatedcoverage, _ = merge_reports(jscoverage, csscoverage)
with open('all_coverage.out', 'w') as cov:
    cov.write('mode: count\n')
    for i in updatedcoverage.items():
        cov.write(f'{i[0].replace("std/","")} {i[1][0]} {i[1][1]}')