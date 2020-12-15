import maya.cmds as cmds

class FreezeDeletUI():
    def __init__(self):
        self.my_window = "freezeDeleteWindow"

    def create(self):
        self.delete()
        self.my_window = cmds.window(self.my_window, title="Freeze / Delete Window", widthHeight=(400, 400))

        self.col_layout = cmds.columnLayout(parent=self.my_window)
        #Build text fields
        cmds.text(parent=self.col_layout, align="left", label='Instructions:\n Select object(s) to Freeze Transformations and/or Delete History.\n')

        self.col_layout = cmds.rowColumnLayout(parent=self.my_window, numberOfColumns=2, columnWidth=[(1, 150), (2, 100)])
        cmds.text(label='Freeze Orientation')
        cmds.button(parent=self.col_layout, label="Run", c=lambda *args: self.freezeO())
        cmds.text(label='Delete History')
        cmds.button(parent=self.col_layout, label="Run", c=lambda *args: self.deleteH())
        cmds.text(label='Freeze O & Delete H')
        cmds.button(parent=self.col_layout, label="Run", c=lambda *args: (self.freezeO(), self.deleteH()))

        cmds.showWindow(self.my_window)

    def delete(self):
        if cmds.window(self.my_window, exists=True):
            cmds.deleteUI(self.my_window)

    def freezeO(self):
        sels = cmds.ls(sl=True)
        for s in sels:
            cmds.makeIdentity(s, apply=True)

    def deleteH(self):
        sels = cmds.ls(sl=True)
        for s in sels:
            cmds.delete(s, constructionHistory=True)

class ParentGroupUI():
    def __init__(self):
        self.my_window = "parentGroupWindow"

    def create(self):
        self.delete()
        self.my_window = cmds.window(self.my_window, title="Parent Group Window", widthHeight=(400, 400))

        self.col_layout = cmds.columnLayout(parent=self.my_window)
        #Build text fields
        cmds.text(parent=self.col_layout, align="left", label='Instructions:\n Select object(s) you want to make parent group(s) for.\n')

        self.col_layout = cmds.rowColumnLayout(parent=self.my_window, numberOfColumns=2, columnWidth=[(1, 150), (2, 100)])

        cmds.text(label='Parent Group Selected')
        cmds.button(parent=self.col_layout, label="Run", c=lambda *args: self.pSelected())
        cmds.text(label='Parent Group Decedents')
        cmds.button(parent=self.col_layout, label="Run", c=lambda *args: self.pDecedents())

        cmds.showWindow(self.my_window)

    def delete(self):
        if cmds.window(self.my_window, exists=True):
            cmds.deleteUI(self.my_window)

    def pSelected(self):
        sels = cmds.ls(sl=True)
        for s in sels:
            sPar = cmds.listRelatives(s, parent=True)
            if sPar==None:
                newControlGroup = cmds.group(empty=True, name=s + 'Grp')
            else:
                newControlGroup = cmds.group(empty=True, name=s + 'Grp', parent=sPar[0])
            cmds.matchTransform(newControlGroup, s)
            cmds.parent(s, newControlGroup)

    def pDecedents(self):
        sels = cmds.ls(sl=True)
        for s in sels:
            newSels = cmds.listRelatives(s, allDescendents=True, type='transform') + [s]
            for ns in newSels:
                sPar = cmds.listRelatives(ns, parent=True)
                if sPar == None:
                    newControlGroup = cmds.group(empty=True, name=ns + 'Grp')
                else:
                    newControlGroup = cmds.group(empty=True, name=ns + 'Grp', parent=sPar[0])
                cmds.matchTransform(newControlGroup, ns)
                cmds.parent(ns, newControlGroup)

class ParentScaleUI():
    def __init__(self):
        self.my_window = "parentScaleWindow"

    def create(self):
        self.delete()
        self.my_window = cmds.window(self.my_window, title="Parent/Scale Constrain Window", widthHeight=(300, 400))

        self.col_layout = cmds.columnLayout(parent=self.my_window)
        #Build text fields
        cmds.text(parent=self.col_layout, align="left", label='Instructions:\n First select object(s) you want Constrain.\n Then select object(s) you want to Constrain to.\n')

        self.col_layout = cmds.rowColumnLayout(parent=self.my_window, numberOfColumns=2, columnWidth=[(1, 100), (2, 100)])

        cmds.text(label='Parent Constrain')
        cmds.button(parent=self.col_layout, label="Run", c=lambda *args: self.parentC())
        cmds.text(label='Scale Constrain')
        cmds.button(parent=self.col_layout, label="Run", c=lambda *args: self.scaleC())
        cmds.text(label='Parent & Scale')
        cmds.button(parent=self.col_layout, label="Run", c=lambda *args: (self.parentC(), self.scaleC()))

        cmds.showWindow(self.my_window)

    def delete(self):
        if cmds.window(self.my_window, exists=True):
            cmds.deleteUI(self.my_window)

    def parentC(self):
        sels = cmds.ls(sl=True)
        conThis = sels[:len(sels)/2]
        conTo = sels[len(sels)/2:]
        for s in range(len(sels)/2):
            cmds.parentConstraint(conThis[s], conTo[s])

    def scaleC(self):
        sels = cmds.ls(sl=True)
        conThis = sels[:len(sels)/2]
        conTo = sels[len(sels)/2:]
        for s in range(len(sels)/2):
            cmds.scaleConstraint(conThis[s], conTo[s])

class RotationAxisUI():
    def __init__(self):
        self.my_window = "rotationAxisWindow"

    def create(self):
        self.delete()
        self.my_window = cmds.window(self.my_window, title="Rotation Axis Window", widthHeight=(300, 400))

        self.col_layout = cmds.columnLayout(parent=self.my_window)
        #Build text fields
        cmds.text(parent=self.col_layout, align="left", label='Instructions:\n Select object(s) you want to toggle axis visability.\n')

        self.col_layout = cmds.rowColumnLayout(parent=self.my_window, numberOfColumns=2, columnWidth=[(1, 100), (2, 100)])

        cmds.text(label='Toggle Axis')
        cmds.text(label='')
        cmds.button(parent=self.col_layout, label="ON", c=lambda *args: self.tAxis())
        cmds.button(parent=self.col_layout, label="OFF", c=lambda *args: self.tAxis(False))

        cmds.showWindow(self.my_window)

    def delete(self):
        if cmds.window(self.my_window, exists=True):
            cmds.deleteUI(self.my_window)

    def tAxis(self, b=True):
        sels = cmds.ls(sl=True)
        for s in sels:
            cmds.setAttr(s+".displayLocalAxis", b, keyable=b)
            cmds.setAttr(s+".jointOrientX", keyable=b)
            cmds.setAttr(s+".jointOrientY", keyable=b)
            cmds.setAttr(s+".jointOrientZ", keyable=b)