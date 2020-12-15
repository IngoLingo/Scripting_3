import maya.cmds as cmds
#my_string = "Name_###_Node"

class SequentialRenamerUI():
    def __init__(self):
        self.my_window = "njeSequentialRenamerWindow"

    def create(self):
        self.delete()

        self.my_window = cmds.window(self.my_window, title="Sequential Renamer Window", widthHeight=(400, 400))

        self.col_layout = cmds.columnLayout(parent=self.my_window)

        #Build text fields
        cmds.text(parent=self.col_layout, align="left", label='Instructions:\n Select object(s) to rename and give a name that has # for the number seuence.\n')
        self.name_field = cmds.textField(parent=self.col_layout, placeholderText="Name for Object Sequence...")
        #self.replace_field = cmds.textField(parent=self.col_layout, placeholderText="Character to Replace...")


        cmds.button(parent=self.col_layout, label="Run", c=lambda *args: self.SequentialRenamer(cmds.ls(selection=True)))

        cmds.showWindow(self.my_window)

    def delete(self):
        if cmds.window(self.my_window, exists=True):
            cmds.deleteUI(self.my_window)

    def FindArrayGroups(self, lookIn, find):
        """Finds objects that are grouped together and puts the number in each group in a list
            Example: FindArrayGroups("Name##_###_#_Node##", "#")
                :returns: [2, 3, 1, 2]
        """
        numList = []
        numLength = 0
        for x in lookIn:
            if x == find:
                numLength += 1
            else :
                if numLength > 0:
                    if numList.count(numLength) == 0:
                        numList.append(numLength)
                    numLength = 0

        if numLength > 0:
            if numList.count(numLength) == 0:
                numList.append(numLength)

        numList.sort(reverse=True)
        #print numList
        return numList

    #FindArrayGroups(my_string, "#")

    def SequentialRenamer(self, objList):
        """
        Renames all selected objects in a sequential order
        :param objList: objects in a list
        :param nameString: Name Format to rename objectList with
        :param renaming: Look for and replace this character in the nameString
        :return:
        """
        nameString = cmds.textField(self.name_field, q=True, text=True)
        renaming = "#"#cmds.textField(self.replace_field, q=True, text=True)

        numRenameList = self.FindArrayGroups(nameString, renaming)
        numCount = 1
        for obj in objList:
            newName = nameString
            for num in numRenameList:
                toReplace = ""
                for n in range(num):
                    toReplace += renaming
                repalceWith = str(numCount).zfill(num)
                newName = newName.replace(toReplace, repalceWith)
            cmds.rename(obj, newName)
            print newName
            numCount += 1

#SequentialRenamer(cmds.ls(selection=True), my_string, "#")
#my_window = SequentialRenamerUI()
#my_window.create()





