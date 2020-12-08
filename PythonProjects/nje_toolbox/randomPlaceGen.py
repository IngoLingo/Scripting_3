import maya.cmds as cmds
import random

class RandomPlacementUI():
    def __init__(self):
        self.my_window = "njeRandomPlacementWindow"

    def create(self):
        self.delete()

        self.my_window = cmds.window(self.my_window, title="Random Placement Window", widthHeight=(300, 400))

        self.col_layout = cmds.rowColumnLayout(parent=self.my_window, numberOfColumns=2, columnWidth=[(1, 100), (2, 100)])

        cmds.text(label='Number of Dupes')
        self.numberOfObjs_field = cmds.intField(parent=self.col_layout, minValue=1, value=1)

        cmds.text(label='X Range')
        self.xRange_field = cmds.intField(parent=self.col_layout, minValue=-1, maxValue=10, value=0)
        cmds.text(label='Y Range')
        self.yRange_field = cmds.intField(parent=self.col_layout, minValue=-1, maxValue=10, value=0)
        cmds.text(label='Z Range')
        self.zRange_field = cmds.intField(parent=self.col_layout, minValue=-1, maxValue=10, value=0)


        cmds.button(parent=self.col_layout, label="Run", c=lambda *args: self.RandomPlacement())

        cmds.showWindow(self.my_window)

    def delete(self):
        if cmds.window(self.my_window, exists=True):
            cmds.deleteUI(self.my_window)

    def RandomPlacement(self):
        selectionsToDuplicat = cmds.ls(selection=True)
        # For / in loop selecting each uniqe object
        for selected in selectionsToDuplicat:
            print selected
            numberOfObjs_value = cmds.intField(self.numberOfObjs_field, q=True, value=True)
            x_value = cmds.intField(self.xRange_field, q=True, value=True)
            y_value = cmds.intField(self.yRange_field, q=True, value=True)
            z_value = cmds.intField(self.zRange_field, q=True, value=True)
            # For loop duplicating each uniqe object
            for value in range(numberOfObjs_value):
                print value
                cmds.duplicate(selected)
                randX = random.randrange(x_value*-1, x_value)
                randY = random.randrange(y_value*-1, y_value)
                randZ = random.randrange(z_value*-1, z_value)

                cmds.xform(selected, translation=(randX, randY, randZ))
                print value


#my_window = RandomPlacementUI()
#my_window.create()

#RandomPlacement(50, -10, 10, -10, 10, -10, 10);
