import json
import csv
from usdm_excel import USDMExcel
from bs4 import BeautifulSoup

SAVE_ALL = False

def save_error_csv(file, contents):
  writer = csv.DictWriter(file, fieldnames=['sheet','row','column','message','level'])
  writer.writeheader()
  writer.writerows(contents)

def to_int(value):
  try:
    return int(value)
  except:
    return None

def read_error_csv(file):
  reader = csv.DictReader(file)
  items = list(reader)
  for item in items:
    item['row'] = to_int(item['row'])
    item['column'] = to_int(item['column'])
  return items

def prep_errors_for_csv_compare(errors):
  for error in errors:
    error['sheet'] = error['sheet'] if error['sheet'] else ''
  return errors

def format_html(result):
  soup = BeautifulSoup(result, 'html.parser')
  return soup.prettify()

def run_test(filename, save=False):
  excel = USDMExcel(f"tests/integration_test_files/{filename}.xlsx")
  result = excel.to_json()
  errors = excel.errors()

  # Useful if you want to see the results.
  if save or SAVE_ALL:
    with open(f"tests/integration_test_files/{filename}.json", 'w', encoding='utf-8') as f:
      f.write(json.dumps(json.loads(result), indent=2))
    with open(f"tests/integration_test_files/{filename}_errors.csv", 'w',newline='') as f:
      save_error_csv(f, errors) 
  
  with open(f"tests/integration_test_files/{filename}.json", 'r') as f:
    expected = json.dumps(json.load(f)) # Odd, but doing it for consistency of processing
  assert result == expected
  with open(f"tests/integration_test_files/{filename}_errors.csv", 'r') as f:
    expected = read_error_csv(f)
  assert prep_errors_for_csv_compare(errors) == expected

def run_test_html(filename, save=False, highlight=False):
  suffix = "_highlight" if highlight else ""
  excel = USDMExcel(f"tests/integration_test_files/{filename}.xlsx")
  result = excel.to_html(highlight)
  errors = excel.errors()

  # Useful if you want to see the results.
  if save or SAVE_ALL:
    with open(f"tests/integration_test_files/{filename}{suffix}.html", 'w') as f:
      f.write(format_html(result))
    with open(f"tests/integration_test_files/{filename}{suffix}_html_errors.csv", 'w',newline='') as f:
      save_error_csv(f, errors) 

  with open(f"tests/integration_test_files/{filename}{suffix}.html", 'r') as f:
    expected = f.read()
  assert format_html(result) == expected
  with open(f"tests/integration_test_files/{filename}{suffix}_html_errors.csv", 'r') as f:
    expected = read_error_csv(f)
  assert prep_errors_for_csv_compare(errors) == expected

def run_test_timeline(filename, level=USDMExcel.FULL_HTML, save=False):
  excel = USDMExcel(f"tests/integration_test_files/{filename}.xlsx")
  result = excel.to_timeline(level)

  # Useful if you want to see the results.
  if save or SAVE_ALL:
    with open(f"tests/integration_test_files/{filename}_timeline_{level}.html", 'w') as f:
      f.write(result)
  
  with open(f"tests/integration_test_files/{filename}_timeline_{level}.html", 'r') as f:
    expected = f.read()
  assert result == expected

def run_test_ne(filename, save=False):
  result = {}
  excel = USDMExcel(f"tests/integration_test_files/{filename}.xlsx")
  result['n'], result['e'] = excel.to_nodes_and_edges()
  for type in ['n', 'e']:

    # Useful if you want to see the results.
    if save or SAVE_ALL:
      with open(f"tests/integration_test_files/{filename}_{type}.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(result[type], indent=2))
    
    with open(f"tests/integration_test_files/{filename}_{type}.json", 'r') as f:
      expected = json.load(f)
    assert result[type] == expected

def test_full_1():
  run_test('full_1')

def test_full_1_timeline():
  run_test_timeline('full_1')

def test_full_1_timeline_body():
  run_test_timeline('full_1', USDMExcel.BODY_HTML)

def test_full_1_html():
  run_test_html('full_1')

def test_full_1_ne():
  run_test_ne('full_1')

def test_full_2():
  run_test('full_2')

def test_full_2_html():
  run_test_html('full_2')

def test_encounter_1():
  run_test('encounter_1')

def test_simple_1():
  run_test('simple_1')

def test_scope_1():
  run_test('scope_1')

def test_amendment_1():
  run_test('amendment_1')

def test_eligibility_criteria_1():
  run_test('eligibility_criteria_1')

def test_simple_1_ne():
  run_test_ne('simple_1')

def test_simple_1_html():
  run_test_html('simple_1')

def test_config_1():
  run_test('config_1')

def test_config_2():
  run_test('config_2')

def test_no_activity_sheet():
  run_test('no_activity_sheet')

def test_address_comma():
  run_test('address')

def test_complex_1():
  run_test('complex_1')

def test_complex_1_ne():
  run_test_ne('complex_1')

def test_arms_epochs_1():
  run_test('arms_epochs')

def test_arms_epochs_1_ne():
  run_test_ne('arms_epochs')

def test_cycles_1():
  run_test('cycles_1')

def test_cycles_1_ne():
  run_test_ne('cycles_1')

def test_multiple_column_names():
  run_test('multiple_column_names')

def test_invalid_section_levels():
  run_test('invalid_section_levels')

def test_new_field_names():
  run_test('new_labels')

def test_timing_check():
  run_test('timing_check')

def test_v2_soa_1():
  run_test('simple_1_v2')

def test_v2_soa_2():
  run_test('decision_1_v2')

def test_timeline_1():
  run_test_timeline('simple_1_v2')

def test_timeline_2():
  run_test_timeline('decision_1_v2')

def test_timeline_3():
  run_test_timeline('complex_1')

def test_timeline_4():
  run_test_timeline('cycles_1')

def test_path_error():
  run_test('path_error')

def test_references():
  run_test('references')

def test_references_html():
  run_test_html('references')

def test_references_html_highlight():
  run_test_html('references', highlight=True)
