from usdm_excel.option_manager import *

def test_create():
  object = OptionManager()
  assert len(object.items.keys()) == 0
  assert object.items == {}

def test_set():
  option_manager.items = {}
  option_manager.set('fred', 'value')
  assert len(option_manager.items.keys()) == 1
  assert option_manager.items['fred'] == 'value'

def test_get():
  option_manager.items = {}
  option_manager.items['fred'] = 'value'
  assert option_manager.get('fred') == 'value'

def test_clear():
  option_manager.items = {}
  option_manager.items['fred'] = 'value'
  assert len(option_manager.items.keys()) == 1
  option_manager.clear()
  assert len(option_manager.items.keys()) == 0

def test_options():
  option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.NONE)
  assert option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.NONE.value
  option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.EMPTY)
  assert option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value
  option_manager.set(Options.USDM_VERSION, 2)
  assert option_manager.get(Options.USDM_VERSION) == '2'
  option_manager.set(Options.USDM_VERSION, 3)
  assert option_manager.get(Options.USDM_VERSION) == '3'
  # option_manager.set(Options.ROOT, RootOption.API_COMPLIANT)
  # assert option_manager.get(Options.ROOT) == RootOption.API_COMPLIANT.value
  # option_manager.set(Options.DESCRIPTION, 'Some text')
  # assert option_manager.get(Options.DESCRIPTION) == 'Some text'