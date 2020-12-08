import maya.cmds as cmds


class RenamerUI():
    def __init__(self):
        self.my_window = 'toolWindow'

    def create(self):
        self.delete()

        self.my_window = cmds.window(self.my_window,
                                     title='coolWindow',
                                     widthHeight=(200, 200))
        self.col_layout = cmds.columnLayout(parent=self.my_window,
                                            adjustableColumn=True)
        self.name_field = cmds.textField(parent=self.col_layout,
                                         placeholderText='Name of new obj')
        cmds.button(parent=self.col_layout, label='sphere', c='createSphere()')
        cmds.button(parent=self.col_layout, label='sphere',
                    c='print cmds.textField(name_field, q=True, text=true')

        cmds.showWindow(self.my_window)

    def delete(self):
        if cmds.window(self.my_window, exists=True):
            cmds.deleteUI(self.my_window)
    #
    # def createSphere(self):
    #     field_val = cmds.textField(self.name_field, q=True, text=True)
    #     cmds.polySphere(name=field_val)


my_window = RenamerUI()
my_window.create()



#Go over List:

#Joints without IK FK
#   Make sure joints are oriented correctly (if not, its supper easy to go back and re-run the script)
#   Need to specify the joint name to the script
#   Watch out for having to manualy put the control group inside the transform group

#Joints With IK FK
#   Names have to be in a spicific order
#   Only use this if you want to mirror and IK/FK a rig