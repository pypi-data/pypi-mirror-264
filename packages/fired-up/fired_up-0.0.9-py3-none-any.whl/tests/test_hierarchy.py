from fired_up import FiredUp, Group, Menu

class SomeGroup(Group):
  def set_value(self):
    self._globals["value"] = "testing value"
    return self

  def get_value(self):
    return self._globals["value"]

def test_hierachy_all(capture):
  with capture() as output:
    top = FiredUp(
      level0=SomeGroup,
      level1=Menu(
        level10=SomeGroup,
        level2=Menu(
          level20=SomeGroup
        )
      ),
      all_results=True,
      command="level1 level2 level20 set_value then level0 get_value then level1 level10 get_value then level1 level2 level20 get_value"
    )
  assert top._local_shared["globals"]["value"] == "testing value"
  assert output == ["testing value"] * 3

def test_hierachy_not_all(capture):
  with capture() as output:
    top = FiredUp(
      level0=SomeGroup,
      level1=Menu(
        level10=SomeGroup,
        level2=Menu(
          level20=SomeGroup
        )
      ),
      all_results=False,
      command="level1 level2 level20 set_value then level0 get_value then level1 level10 get_value then level1 level2 level20 get_value"
    )
  assert top._local_shared["globals"]["value"] == "testing value"
  assert output == ["testing value"]

def test_nested_menu_hierarchy_has_single_shared_globals():
  class Master(Group):
    def __post_construct_init__(self):
      self._globals["root"] = "set by master"

  class Slave(Group):
    pass

  top = FiredUp(
    menu=Menu(
      master=Master
    ),
    slave=Slave
  )

  assert isinstance(top.menu.master, Master)
  assert isinstance(top.slave, Slave)

  assert top.slave._shared        is top._local_shared
  assert top.menu._shared         is top._local_shared
  assert top.menu.master._shared  is top._local_shared
  
  assert top.slave._globals["root"] == "set by master"
