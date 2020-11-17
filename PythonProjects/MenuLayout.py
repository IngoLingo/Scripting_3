import maya.cmds as cmds

my_window = "njeTestWindow"

if cmds.window(my_window, exists=True):
    cmds.deleteUI(my_window)

my_window = cmds.window(my_window, title="Test Window", widthHeight=(200, 200))

col_layout = cmds.columnLayout(parent=my_window)

name_field = cmds.textField(parent=col_layout, placeholderText="Name of New Object...")

cmds.button(parent=col_layout, label="Sphere", c='createSphere()')
cmds.button(parent=col_layout, label= "Print Field",
            c='print cmds.textField(name_field, q=True, text=True)')


cmds.showWindow(my_window)

def createSphere():
    field_value = cmds.textField(name_field, q=True, text=True)
    cmds.polySphere(name=field_value)