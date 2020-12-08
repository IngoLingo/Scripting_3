import maya.cmds as cmds

class Toolbox_UI():
    def __init__(self):
        self.my_window = "nje_mytools_ui"

    def create(self):
        self.delete()

        self.my_window = cmds.window(self.my_window, title="NJE Toolbox", widthHeight=(200, 200))

        self.col_layout = cmds.columnLayout(parent=self.my_window)

        cmds.button(parent=self.col_layout, label="Renamer UI", c=lambda *args: self.call_renamerUI())
        cmds.button(parent=self.col_layout, label="Random Place Generator", c=lambda *args: self.call_randomPlaceGenUI())
        cmds.button(parent=self.col_layout, label="NJE Rig Assist Tool", c=lambda *args: self.call_njeRigAssist())

        cmds.showWindow(self.my_window)

    def delete(self):
        if cmds.window(self.my_window, exists=True):
            cmds.deleteUI(self.my_window)

    def call_renamerUI(self):
        import renamer
        reload(renamer)
        renamerUI_instance = renamer.SequentialRenamerUI()
        renamerUI_instance.create()

    def call_randomPlaceGenUI(self):
        import randomPlaceGen
        reload(randomPlaceGen)
        randomPGUI_instance = randomPlaceGen.RandomPlacementUI()
        randomPGUI_instance.create()

    def call_njeRigAssist(self):
        import nje_rigAssistTool
        reload(nje_rigAssistTool)
        rigAssist_instance = nje_rigAssistTool.RigAssistUI()
        rigAssist_instance.create()