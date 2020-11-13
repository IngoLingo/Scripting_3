import maya.cmds as cmds
my_string = "Name_###_Node"

def FindArrayGroups(lookIn, find):
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

def SequentialRenamer(objList, nameString, renaming):
    """
    Renames all selected objects in a sequential order
    :param objList: objects in a list
    :param nameString: Name Format to rename objectList with
    :param renaming: Look for and replace this character in the nameString
    :return:
    """
    numRenameList = FindArrayGroups(nameString, renaming)
    numCount = 1
    for obj in objList:
        newName = my_string
        for num in numRenameList:
            toReplace = ""
            for n in range(num):
                toReplace += renaming
            repalceWith = str(numCount).zfill(num)
            newName = newName.replace(toReplace, repalceWith)

        cmds.rename(obj, newName)
        numCount += 1

SequentialRenamer(cmds.ls(selection=True), my_string, "#")

##





