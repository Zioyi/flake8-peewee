import ast
from typing import Set

from flake8_peewee import Plugin


def _results(s: str) -> Set[str]:
    tree = ast.parse(s)
    plugin = Plugin(tree)
    return {f"{line}:{col} {msg}" for line, col, msg, _ in plugin.run()}


def test_trivial_case():
    assert _results("") == set()
    assert _results("UserPlan.select(UserPlan.user_id == 1).where()") == {"1:0 PWE101 select() or delete() inner comparison expression are not allowed"}
    assert _results("UserPlan.select().where(UserPlan.plan_id == 1)") == set()
    assert _results("UserPlan.select(UserPlan.user_id, UserPlan.plan_id).where(UserPlan.plan_id == 1)") == set()
    assert _results("""for up in UserPlan.select(UserPlan.user_id == 1).where():
    print(up)""") == {"1:10 PWE101 select() or delete() inner comparison expression are not allowed"}
    assert _results("""for up in UserPlan.select(UserPlan.user_id).where(UserPlan.user_id == 1).where():
    print(up)""") == set()
    assert _results("UserPlan.get_user_plan(user_id, plan_id)") == set()
    assert _results("""for uc in sc_models.UserCourse.select(sc_models.UserCourse.stage3_end_date <= date):
    try:
        sc_models.UserLearning.unlock_next_user_learning(uc.user_id, uc.course_id, date)
    except Exception as err:
        current_app.logger.error(err, exc_info=True)""") == {"1:10 PWE101 select() or delete() inner comparison expression are not allowed"}
    assert _results("sc_models.UserCourse.select(sc_models.UserCourse.stage3_end_date >= date)") == {"1:0 PWE101 select() or delete() inner comparison expression are not allowed"}
    assert _results("UserPlan.delete(UserPlan.user_id == 1).execute") == {"1:0 PWE101 select() or delete() inner comparison expression are not allowed"}


def test_plugin_version():
    assert isinstance(Plugin.version, str)
    assert "." in Plugin.version


def test_plugin_name():
    assert isinstance(Plugin.name, str)
