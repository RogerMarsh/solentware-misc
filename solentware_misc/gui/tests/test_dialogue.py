# test_dialogue.py
# Copyright 2021 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""dialogue tests.

Several tests are commented out because they would force user interaction.

There are still a few tests which generate <can't invoke "event" command>
reports which do not cause the test to fail.  These are associated with
temporary display of widgets.

Running the dialogue module displays a widget which allows all the
dialogues to be invoked by user action.
"""

import unittest
import tkinter
import sys

from .. import dialogue


class _Dialogue(unittest.TestCase):
    def setUp(self):
        class Parent:
            root = tkinter.Tk()

            def get_widget(self):
                return self.root

        self.Parent = Parent

    def tearDown(self):
        # Replacing this statement with 'pass' stops the
        # "can't invoke "event" command:  application has been destroyed"
        # reports being made, but the widgets remain visible until the
        # test run is completed.
        self.Parent.root.destroy()
        # pass


class DialogueInit(_Dialogue):
    def test_001___init___001(self):
        if sys.version_info.major == 3 and sys.version_info.minor < 10:
            init = "__init__"
        else:
            init = "Dialogue.__init__"
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    init,
                    r"\(\) takes from 1 to 11 positional ",
                    "arguments but 12 were given",
                )
            ),
            dialogue.Dialogue,
            *(
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ),
        )

    def test_001___init___002(self):
        self.assertIsInstance(
            dialogue.Dialogue(
                self.Parent(),
                None,
                text=None,
                action_titles=None,
                buttons=("button",),
                side=tkinter.BOTTOM,
                scroll=True,
                body=None,
                geometry=False,
                cnf=dict(),
                anykey=None,
            ),
            dialogue.Dialogue,
        )

    def test_001___init___003_geometry_True(self):
        # Widgets are made visible briefly.  A
        # "can't invoke "event" command:  application has been destroyed"
        # report is made.
        self.assertIsInstance(
            dialogue.Dialogue(
                parent=self.Parent(),
                title=None,
                text=None,
                action_titles=None,
                buttons=("button",),
                side=tkinter.BOTTOM,
                scroll=True,
                body=None,
                geometry=True,
                cnf=dict(),
                anykey=None,
            ),
            dialogue.Dialogue,
        )


class Dialogue(_Dialogue):
    def setUp(self):
        super().setUp()
        self.dialogue = dialogue.Dialogue(
            self.Parent(),
            None,
            text=None,
            action_titles=None,
            buttons=("button",),
            side=tkinter.BOTTOM,
            scroll=True,
            body=None,
            geometry=False,
            cnf=dict(),
        )

    def test_001_append_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"append\(\) missing 1 required positional argument: ",
                    "'text'",
                )
            ),
            self.dialogue.append,
        )

    def test_001_append_002(self):
        self.assertEqual(self.dialogue.append("text"), None)

    def test_002__create_widget_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_create_widget\(\) missing 10 required positional ",
                    "arguments: 'parent', 'title', 'text', 'action_titles', ",
                    "'buttons', 'side', 'scroll', 'body', 'cnf', and 'kargs'",
                )
            ),
            self.dialogue._create_widget,
        )

    def test_002__create_widget_002(self):
        self.assertEqual(
            self.dialogue._create_widget(
                self.Parent(),
                "Title",
                "Body text",
                {"ok": "Ok", "cancel": "Cancel"},
                (
                    "ok",
                    "cancel",
                ),
                tkinter.BOTTOM,
                True,
                None,
                dict(),
                dict(),
            ),
            None,
        )

    def test_002__create_widget_003_body_tkinter_Text(self):
        self.assertEqual(
            self.dialogue._create_widget(
                self.Parent(),
                "Title",
                "Body text",
                {"ok": "Ok", "cancel": "Cancel"},
                (
                    "ok",
                    "cancel",
                ),
                tkinter.BOTTOM,
                True,
                tkinter.Text,
                dict(),
                dict(),
            ),
            None,
        )

    def test_002__create_widget_004_scroll_False(self):
        self.assertEqual(
            self.dialogue._create_widget(
                self.Parent(),
                "Title",
                "Body text",
                {"ok": "Ok", "cancel": "Cancel"},
                (
                    "ok",
                    "cancel",
                ),
                tkinter.BOTTOM,
                False,
                None,
                dict(),
                dict(),
            ),
            None,
        )

    def test_002__create_widget_005_side_tkinter_TOP(self):
        self.assertEqual(
            self.dialogue._create_widget(
                self.Parent(),
                "Title",
                "Body text",
                {"ok": "Ok", "cancel": "Cancel"},
                (
                    "ok",
                    "cancel",
                ),
                tkinter.TOP,
                True,
                None,
                dict(),
                dict(),
            ),
            None,
        )

    def test_002__create_widget_006_side_tkinter_RIGHT(self):
        self.assertEqual(
            self.dialogue._create_widget(
                self.Parent(),
                "Title",
                "Body text",
                {"ok": "Ok", "cancel": "Cancel"},
                (
                    "ok",
                    "cancel",
                ),
                tkinter.RIGHT,
                True,
                None,
                dict(),
                dict(),
            ),
            None,
        )

    def test_002__create_widget_007_side_tkinter_LEFT(self):
        self.assertEqual(
            self.dialogue._create_widget(
                self.Parent(),
                "Title",
                "Body text",
                {"ok": "Ok", "cancel": "Cancel"},
                (
                    "ok",
                    "cancel",
                ),
                tkinter.LEFT,
                True,
                None,
                dict(),
                dict(),
            ),
            None,
        )

    def test_002__create_widget_008_side_None(self):
        self.assertEqual(
            self.dialogue._create_widget(
                self.Parent(),
                "Title",
                "Body text",
                {"ok": "Ok", "cancel": "Cancel"},
                (
                    "ok",
                    "cancel",
                ),
                None,
                True,
                None,
                dict(),
                dict(),
            ),
            None,
        )

    def test_003_button_on_attr_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"button_on_attr\(\) missing 1 required positional ",
                    "argument: 'action'",
                )
            ),
            self.dialogue.button_on_attr,
        )

    def test_003_button_on_attr_002(self):
        self.assertEqual(self.dialogue.action, None)
        self.assertEqual(self.dialogue.button_on_attr("action")(), None)
        self.assertEqual(self.dialogue.action, "action")

    def test_004__set_geometry_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_set_geometry\(\) missing 1 required positional ",
                    "argument: 'master'",
                )
            ),
            self.dialogue._set_geometry,
        )

    def test_004__set_geometry_002(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"_set_geometry\(\) got an unexpected keyword ",
                    "argument 'badkey'",
                )
            ),
            self.dialogue._set_geometry,
            *(None,),
            **dict(relx=0.5, rely=0.3, badkey=None),
        )

    def test_004__set_geometry_003(self):
        # Widgets are made visible briefly.  A sequence of
        # "can't invoke "event" command:  application has been destroyed"
        # reports are made.
        self.assertEqual(
            self.dialogue._set_geometry(
                self.dialogue.root, relx=0.8, rely=0.7
            ),
            None,
        )

    def test_005_widget_transient_001(self):
        self.assertEqual(self.dialogue.widget_transient(), None)

    def test_006_wm_delete_window_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"wm_delete_window\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.dialogue.wm_delete_window,
            *(None,),
        )

    def test_006_wm_delete_window_002(self):
        self.assertEqual(self.dialogue.wm_delete_window(), None)

    def test_007_focus_set_001(self):
        self.assertEqual(self.dialogue.focus_set(), None)


class ModalDialogueGo(_Dialogue):
    def setUp(self):
        super().setUp()
        self.dialogue = dialogue.ModalDialogueGo(
            parent=self.Parent(),
            title=None,
            text=None,
            action_titles=None,
            buttons=("button",),
            side=tkinter.BOTTOM,
            scroll=True,
            body=None,
            cnf=dict(),
        )

    def test_001_go_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"go\(\) takes 1 positional argument ",
                    "but 2 were given",
                )
            ),
            self.dialogue.go,
            *(None,),
        )

    def test_001_go_002(self):
        # The test run blocks here until the dialogue is dismissed by
        # clicking a button.
        self.assertEqual(self.dialogue.go(), self.dialogue.action)

    def test_002_button_on_attr_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"button_on_attr\(\) missing 1 required positional ",
                    "argument: 'action'",
                )
            ),
            self.dialogue.button_on_attr,
        )

    def test_002_button_on_attr_002(self):
        self.assertEqual(self.dialogue.button_on_attr("action")(), None)

    def test_003_widget_transient_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"widget_transient\(\) missing 2 required positional ",
                    "arguments: 'widget' and 'master'",
                )
            ),
            self.dialogue.widget_transient,
        )

    def test_003_widget_transient_002(self):
        self.assertEqual(
            self.dialogue.widget_transient(
                self.dialogue.root, self.dialogue.parent.root
            ),
            None,
        )


class ModalDialogue(_Dialogue):
    def setUp(self):
        super().setUp()
        self.dialogue = dialogue.ModalDialogue(
            parent=self.Parent(),
            title=None,
            text=None,
            action_titles=None,
            buttons=("button",),
            side=tkinter.BOTTOM,
            scroll=True,
            body=None,
            cnf=dict(),
        )

    def test_001_widget_transient_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"widget_transient\(\) missing 2 required positional ",
                    "arguments: 'widget' and 'master'",
                )
            ),
            self.dialogue.widget_transient,
        )

    def test_001_widget_transient_002(self):
        self.assertRaisesRegex(
            tkinter.TclError,
            'bad window path name ".!toplevel"',
            self.dialogue.widget_transient,
            *(self.dialogue.root, self.dialogue.parent.root),
        )


class ModalConfirm(_Dialogue):
    def test_001___init___001(self):
        self.assertIsInstance(
            dialogue.ModalConfirm(
                parent=self.Parent(),
                title=None,
                text=None,
                action_titles=None,
                buttons=("button",),
                side=tkinter.BOTTOM,
                scroll=True,
                body=None,
                cnf=dict(),
            ),
            dialogue.ModalConfirm,
        )


class ModalConfirmGo(_Dialogue):
    def test_001___init___001(self):
        self.assertIsInstance(
            dialogue.ModalConfirmGo(
                parent=self.Parent(),
                title=None,
                text=None,
                action_titles=None,
                buttons=("button",),
                side=tkinter.BOTTOM,
                scroll=True,
                body=None,
                cnf=dict(),
            ),
            dialogue.ModalConfirmGo,
        )


class ShowModalConfirm(_Dialogue):
    def test_001_show_modal_confirm_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"show_modal_confirm\(\) missing 2 required positional ",
                    "arguments: 'parent' and 'title'",
                )
            ),
            dialogue.show_modal_confirm,
        )

    def test_001_show_modal_confirm_002(self):
        self.assertIsInstance(
            dialogue.show_modal_confirm(
                parent=self.Parent(),
                title=None,
                text=None,
                action_titles=None,
                buttons=("button",),
                side=tkinter.BOTTOM,
                scroll=True,
                body=None,
                cnf=dict(),
            ),
            dialogue.ModalConfirmGo,
        )


class ModalInformation(_Dialogue):
    def test_001___init___001(self):
        self.assertIsInstance(
            dialogue.ModalInformation(
                parent=self.Parent(),
                title=None,
                text=None,
                action_titles=None,
                buttons=("button",),
                side=tkinter.BOTTOM,
                scroll=True,
                body=None,
                cnf=dict(),
            ),
            dialogue.ModalInformation,
        )


class ModalInformationGo(_Dialogue):
    def test_001___init___001(self):
        self.assertIsInstance(
            dialogue.ModalInformationGo(
                parent=self.Parent(),
                title=None,
                text=None,
                action_titles=None,
                buttons=("button",),
                side=tkinter.BOTTOM,
                scroll=True,
                body=None,
                cnf=dict(),
            ),
            dialogue.ModalInformationGo,
        )


class ShowModalInformation(_Dialogue):
    def test_001_show_modal_information_001(self):
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"show_modal_information\(\) missing 2 required ",
                    "positional arguments: 'parent' and 'title'",
                )
            ),
            dialogue.show_modal_information,
        )

    def test_001_show_modal_information_002(self):
        self.assertIsInstance(
            dialogue.show_modal_information(
                self.Parent(),
                None,
                text=None,
                action_titles=None,
                buttons=("button",),
                side=tkinter.BOTTOM,
                scroll=True,
                body=None,
                cnf=dict(),
            ),
            dialogue.ModalInformationGo,
        )


class ModalEntry(_Dialogue):
    def test_001___init___001(self):
        self.assertIsInstance(
            dialogue.ModalEntry(
                parent=self.Parent(),
                title=None,
                text=None,
                action_titles=None,
                buttons="ignored, always set to buttons attribute",
                side=tkinter.BOTTOM,
                scroll="ignored, always set to False",
                body=None,
                cnf=dict(),
            ),
            dialogue.ModalEntry,
        )


class ModalEntryGo(_Dialogue):
    def test_001___init___001(self):
        self.assertIsInstance(
            dialogue.ModalEntryGo(
                parent=self.Parent(),
                title=None,
                text=None,
                action_titles=None,
                buttons="ignored, always set to buttons attribute",
                side=tkinter.BOTTOM,
                scroll="ignored, always set to False",
                body=None,
                cnf=dict(),
            ),
            dialogue.ModalEntryGo,
        )


class ModalEntryApply(_Dialogue):
    def test_001___init___001(self):
        self.assertIsInstance(
            dialogue.ModalEntryApply(
                parent=self.Parent(),
                title=None,
                text=None,
                action_titles=None,
                buttons="ignored, always set to buttons attribute",
                side=tkinter.BOTTOM,
                scroll="ignored, always set to False",
                body=None,
                cnf=dict(),
            ),
            dialogue.ModalEntryApply,
        )


class ModalEntryApplyGo(_Dialogue):
    def test_001___init___001(self):
        self.assertIsInstance(
            dialogue.ModalEntryApplyGo(
                parent=self.Parent(),
                title=None,
                text=None,
                action_titles=None,
                buttons="ignored, always set to buttons attribute",
                side=tkinter.BOTTOM,
                scroll="ignored, always set to False",
                body=None,
                cnf=dict(),
            ),
            dialogue.ModalEntryApplyGo,
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(DialogueInit))
    runner().run(loader(Dialogue))
    runner().run(loader(ModalDialogueGo))
    runner().run(loader(ModalDialogue))
    runner().run(loader(ModalConfirm))
    runner().run(loader(ModalConfirmGo))
    runner().run(loader(ShowModalConfirm))
    runner().run(loader(ModalInformation))
    runner().run(loader(ModalInformationGo))
    runner().run(loader(ShowModalInformation))
    runner().run(loader(ModalEntry))
    runner().run(loader(ModalEntryGo))
    runner().run(loader(ModalEntryApply))
    runner().run(loader(ModalEntryApplyGo))
