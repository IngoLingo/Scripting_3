import maya.cmds as cmds

class RenamerUI():
    def __init__(self):
        self.my_window = "njeTestWindow"

    def create(self):
        self.delete()

        self.my_window = cmds.window(self.my_window, title="Test Window", widthHeight=(200, 200))

        self.col_layout = cmds.columnLayout(parent=self.my_window)

        self.name_field = cmds.textField(parent=self.col_layout, placeholderText="Name of New Object...")

        self.size_slider = cmds.intSlider(parent=self.col_layout, minValue=0.001, maxValue=20)

        cmds.button(parent=self.col_layout, label="Sphere", c=lambda *args: self.createSphere())

        cmds.showWindow(self.my_window)

    def delete(self):
        if cmds.window(self.my_window, exists=True):
            cmds.deleteUI(self.my_window)

    def createSphere(self):
        field_value = cmds.textField(self.name_field, q=True, text=True)
        size_value = cmds.intSlider(self.size_slider, q=True, value=True)
        cmds.polySphere(name=field_value, r=size_value)


my_window = RenamerUI()
my_window.create()