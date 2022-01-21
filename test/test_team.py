import unittest

from src.models.team import Team


class TestTeam(unittest.TestCase):
    def test_init_team(self):
        # base a supprimer

        def test_init_team_id():
            # test identifier = int
            with self.assertRaises(TypeError):
                Team(identifier=123,
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test identifier = float
            with self.assertRaises(TypeError):
                Team(identifier=12.3,
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test identifier = bool
            with self.assertRaises(TypeError):
                Team(identifier=True,
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test identifier = list
            with self.assertRaises(TypeError):
                Team(identifier=["test"],
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test identifier = dict
            with self.assertRaises(TypeError):
                Team(identifier={"test": "dict"},
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test identifier = None
            with self.assertRaises(TypeError):
                Team(identifier=None,
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )

        def test_init_team_name():
            # test name = bool
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name=True,
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test name = int
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name=123,
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test name = float
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name=1.23,
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test name = list
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name=["test"],
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test name = dict
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name={"test": "dict"},
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )

        def test_init_team_group_name():
            # test group_names = str
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names="test",
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test group_names = int
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=123,
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test group_names = float
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=12.3,
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test group_names = bool
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=True,
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test group_names = dict
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names={"test": "dict"},
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )

        def test_init_team_admin_team():
            # test admin_team = int
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=123,
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test admin_team = str
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team="123",
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test admin_team = float
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=1.23,
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test admin_team = dict
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team={"test": "123"},
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )
            # test admin_team = bool
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=True,
                     channels=["channel1"],
                     icon_path=None,
                     participants=None,
                     )

        def test_init_team_channels():
            # test channels = str
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=123,
                     icon_path=None,
                     participants=None,
                     )
            # test channels = int
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=123,
                     icon_path=None,
                     participants=None,
                     )
            # test channels = float
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=1.23,
                     icon_path=None,
                     participants=None,
                     )
            # test channels = bool
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=True,
                     icon_path=None,
                     participants=None,
                     )
            # test channels = dict
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels={"test": "123"},
                     icon_path=None,
                     participants=None,
                     )

        def test_init_team_icon_path():
            # test icon_path = int
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=123,
                     participants=None,
                     )
            # test icon_path = float
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=1.23,
                     participants=None,
                     )
            # test icon_path = list
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=["123"],
                     participants=None,
                     )
            # test icon_path = dict
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path={"test": "123"},
                     participants=None,
                     )
            # test icon_path = bool
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=True,
                     participants=None,
                     )

        def test_init_team_participants():
            # test participants = int
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=123,
                     )
            # test participants = float
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=1.23,
                     )
            # test participants = str
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants="123",
                     )
            # test participants = dict
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants={"test": "123"},
                     )
            # test participants = bool
            with self.assertRaises(TypeError):
                Team(identifier="123",
                     name="test",
                     group_names=["test1"],
                     admin_team=["Vincent"],
                     channels=["channel1"],
                     icon_path=None,
                     participants=True,
                     )

        # lancement des tests
        test_init_team_id()
        test_init_team_name()
        test_init_team_group_name()
        test_init_team_admin_team()
        test_init_team_channels()
        test_init_team_icon_path()
        test_init_team_participants()
#                                                                          A faire
#
    def test_add_channel_to_current_team(self):
        team_de_test = Team(
            identifier="123456",
            name="test",
            group_names=["test1", "test2"],
            admin_team=["Vincent"],
            channels=["channel1", "channel2", "channel3"],
            icon_path=None,
            participants=["Vincent", "UserTest1", "Alice"]
        )
        with self.assertRaises(TypeError):
            team_de_test.add_channel_to_current_team(membre=123)
        with self.assertRaises(TypeError):
            team_de_test.add_channel_to_current_team(membre=["Vincent", "Alice"])
        with self.assertRaises(TypeError):
            team_de_test.add_channel_to_current_team(membre={"test": "123"})
        with self.assertRaises(TypeError):
            team_de_test.add_channel_to_current_team(membre=True)

    def test_add_channel_on_db(self):
        team_de_test = Team(
            identifier="123456",
            name="test",
            group_names=["test1", "test2"],
            admin_team=["Vincent"],
            channels=["channel1", "channel2", "channel3"],
            icon_path=None,
            participants=["Vincent", "UserTest1", "Alice"]
        )
        with self.assertRaises(TypeError):
            team_de_test.add_channel_on_db(membre=123)
        with self.assertRaises(TypeError):
            team_de_test.add_channel_on_db(membre=["Vincent", "Alice"])
        with self.assertRaises(TypeError):
            team_de_test.add_channel_on_db(membre={"test": "123"})
        with self.assertRaises(TypeError):
            team_de_test.add_channel_on_db(membre=True)

    def test_add_member(self):
        team_de_test = Team(
            identifier="123456",
            name="test",
            group_names=["test1", "test2"],
            admin_team=["Vincent"],
            channels=["channel1", "channel2", "channel3"],
            icon_path=None,
            participants=["Vincent", "UserTest1", "Alice"]
        )
        with self.assertRaises(TypeError):
            team_de_test.add_member(membre=123)
        with self.assertRaises(TypeError):
            team_de_test.add_member(membre=["Vincent", "Alice"])
        with self.assertRaises(TypeError):
            team_de_test.add_member(membre={"test": "123"})
        with self.assertRaises(TypeError):
            team_de_test.add_member(membre=True)
        team_de_test.add_member("user_des_tests")
        self.assertIn("user_des_tests", team_de_test.participants)

    def test_add_group(self):
        team_de_test = Team(
            identifier="123456",
            name="test",
            group_names=["test1", "test2"],
            admin_team=["Vincent"],
            channels=["channel1", "channel2", "channel3"],
            icon_path=None,
            participants=["Vincent", "UserTest1", "Alice"]
        )
        with self.assertRaises(TypeError):
            team_de_test.add_group(membre=123)
        with self.assertRaises(TypeError):
            team_de_test.add_group(membre=["Vincent", "Alice"])
        with self.assertRaises(TypeError):
            team_de_test.add_group(membre={"test": "123"})
        with self.assertRaises(TypeError):
            team_de_test.add_group(membre=True)

    def test_is_team_member(self):
        team_de_test = Team(
            identifier="123456",
            name="test",
            group_names=["test1", "test2"],
            admin_team=["Vincent"],
            channels=["channel1", "channel2", "channel3"],
            icon_path=None,
            participants=["Vincent", "UserTest1", "Alice"]
        )
        with self.assertRaises(TypeError):
            team_de_test.is_member_team(membre=123)
        with self.assertRaises(TypeError):
            team_de_test.is_member_team(membre=1.023)
        with self.assertRaises(TypeError):
            team_de_test.is_member_team(membre=["Vincent", "Alice"])
        with self.assertRaises(TypeError):
            team_de_test.is_member_team(membre={"test": "123"})
        with self.assertRaises(TypeError):
            team_de_test.is_member_team(membre=True)
        with self.assertRaises(TypeError):
            team_de_test.is_member_team(membre=None)

        self.assertIsNotNone(team_de_test.participants)
        self.assertEqual(team_de_test.is_member_team("Vincent"), True)
        self.assertEqual(team_de_test.is_member_team("Olivier"), False)

        team_de_test2 = Team(
            identifier="123456",
            name="test",
            group_names=["test1", "test2"],
            admin_team=[],
            channels=["channel1", "channel2", "channel3"],
            icon_path=None,
            participants=None
        )
        self.assertIsNone(team_de_test2.participants)
        self.assertEqual(team_de_test.is_member_team("Vincent"), False)

    def test_is_team_admin(self):
        team_de_test = Team(
            identifier="123456",
            name="test",
            group_names=["test1", "test2"],
            admin_team=["Vincent"],
            channels=["channel1", "channel2", "channel3"],
            icon_path=None,
            participants=["Vincent", "UserTest1", "Alice"]
        )
        with self.assertRaises(TypeError):
            team_de_test.is_admin_team(membre=123)
        with self.assertRaises(TypeError):
            team_de_test.is_admin_team(membre=["Vincent"])
        with self.assertRaises(TypeError):
            team_de_test.is_admin_team(membre={"test": "123"})
        with self.assertRaises(TypeError):
            team_de_test.is_admin_team(membre=True)

        self.assertIsNotNone(team_de_test.admin_team)
        self.assertEqual(team_de_test.is_admin_team("Vincent"), True)
        self.assertEqual(team_de_test.is_admin_team("Olivier"), False)

