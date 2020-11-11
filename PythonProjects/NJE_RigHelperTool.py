import maya.cmds as cmds

# Naming convention vars
characterName_string = "Baby"

sideOld_string = "L"
sideNew_string = "R"

name_string = "Name"

number_string = "##"# indicate the max number of digits a string can go

nodeGeometry_string = "Geo"
nodeJoint_string = "Jnt"
nodeControl_string = "Ctrl"
nodeCtrlGroup_string = "Grp"

controlTypeRK_string = "RK"
controlTypeFK_string = "FK"
controlTypeIK_string = "IK"

controlSize = 0.25

def BuildRigGroups():
    # check to see if each of these groups exist and create them if not
    global groupFullRig
    groupFullRig = cmds.group(empty=True, name=characterName_string + "_FullRig")
    global groupGeometry
    groupGeometry = cmds.group(empty=True, name=characterName_string + "_Geometry", parent=groupFullRig)
    global groupJoints
    groupJoints = cmds.group(empty=True, name=characterName_string + "_Joints", parent=groupFullRig)
    global groupControls
    groupControls = cmds.group(empty=True, name=characterName_string + "_Controls", parent=groupFullRig)
    global groupFKControls
    groupFKControls = cmds.group(empty=True, name=characterName_string + "_FKControls", parent=groupControls)
    global groupIKControls
    groupIKControls = cmds.group(empty=True, name=characterName_string + "_IKControls", parent=groupControls)

# Functions
#Note: add a discription to each function
def NJE_MakeControl( jointTo, parent, controlSize=controlSize, rotateDir='.rotateY', rotateNum=90):
    newName = jointTo.replace('Jnt', 'Ctrl')
    newControl = cmds.circle(name=newName)
    cmds.setAttr(newControl[0] + rotateDir, rotateNum)
    cmds.xform(newControl[0], scale=(controlSize, controlSize, controlSize))
    newControlGroup = cmds.group(newControl, name=newName + 'Grp')
    cmds.matchTransform(newControlGroup, jointTo)
    cmds.makeIdentity(newControl[0], apply=True)
    cmds.delete(newControl[0], constructionHistory=True)
    cmds.parent(newControlGroup, parent)

    return newControl[0]

def NJE_MasterConstrain(constrainThis, constrainTo):
    cmds.parentConstraint(constrainThis, constrainTo)
    cmds.scaleConstraint(constrainThis, constrainTo)

def NJE_MakeTransformControl(parent, controlSize=10*controlSize, rotateDir='.rotateX', rotateNum=90):
    newName = characterName_string+"_Transform_Ctrl"
    newControl = cmds.circle(name=newName)
    cmds.setAttr(newControl[0] + rotateDir, rotateNum)
    cmds.xform(newControl[0], scale=(controlSize, controlSize, controlSize))
    newControlGroup = cmds.group(newControl, name=newName + 'Grp')
    cmds.makeIdentity(newControl[0], apply=True)
    cmds.delete(newControl[0], constructionHistory=True)
    cmds.parent(newControlGroup, parent)

    return newControl[0]

def NJE_MakePVControl( jointTo, parent, controlSize=controlSize): #Make an IK PV control for the IK joints and orient them properly
    newName = cmds.listRelatives(jointTo, parent=True)[0].replace('Jnt', 'PV_Offset_Grp')
    newPV = cmds.circle(name=newName)
    selectShapeNode = cmds.listRelatives(newPV[0], shapes=True)
    cmds.delete(selectShapeNode)
    newName = cmds.listRelatives(jointTo, parent=True)[0].replace('Jnt', 'PV_Ctrl')
    newControl = cmds.circle(name=newName)
    cmds.xform(newControl[0], scale=(controlSize, controlSize, controlSize))
    #cmds.select(newControl.cv.[0,2,4,6])
    #cmds.scale( newControl.cv.[0,2,4,6], relative = True, pivot = (-9, 0, 0) )
    cmds.parent(newControl, newPV)# Warning: Cannot parent components or objects in the underworld. #
    newControlGroup = cmds.group(newPV, name=newName + 'Grp', parent=parent)
    cmds.matchTransform(newControlGroup, cmds.listRelatives(jointTo, parent=True))
    cmds.xform(newPV[0], translation=(0, -10*controlSize, 0))
    cmds.makeIdentity(newControl[0], apply=True)
    cmds.delete(newControl[0], constructionHistory=True)

    return newName

def NJE_MirrorAndRig(baseJointList):
    for joint in baseJointList:
        oldJoint = joint
        newJoint = cmds.mirrorJoint(joint, mirrorYZ=True, mirrorBehavior=True, searchReplace=[sideOld_string, sideNew_string])[0]
        allJoint = [oldJoint] + [newJoint]

        # Make a group for RK FK and IK, for their Joints and Controls
        groupRK = cmds.group(empty=True, parent=cmds.listRelatives(joint, parent=True)[0], name=joint.replace(nodeJoint_string, "Group").replace(sideOld_string+"_",""))
        groupFK = cmds.group(empty=True, parent=cmds.listRelatives(joint, parent=True)[0], name=joint.replace(nodeJoint_string, "Group").replace(sideOld_string+"_","").replace(controlTypeRK_string, controlTypeFK_string))
        groupIK = cmds.group(empty=True, parent=cmds.listRelatives(joint, parent=True)[0], name=joint.replace(nodeJoint_string, "Group").replace(sideOld_string+"_","").replace(controlTypeRK_string, controlTypeIK_string))

        FKControlGroup = cmds.group(empty=True, name=groupFK.replace("Group", "Controls"), parent=groupFKControls)
        IKControlGroup = cmds.group(empty=True, name=groupIK.replace("Group", "Controls"), parent=groupIKControls)

        # Build all the FK and IK joints & Controls from the RK joints
        ikHandleGroup=[]
        for jointRK in allJoint:
            # Work on FK joints
            jointFK = cmds.duplicate(jointRK, name=jointRK.replace(controlTypeRK_string, controlTypeFK_string), renameChildren=True) #Duplicate and rename joint and create a control
            parentControl = NJE_MakeControl(jointFK[0], FKControlGroup)
            NJE_MasterConstrain(parentControl, jointFK)

            for oldName in jointFK[1:]: #Renameing all joint desendents and createing controls
                if controlTypeRK_string in oldName:
                    newName = oldName.replace(controlTypeRK_string, controlTypeFK_string)[0:-1]
                    cmds.rename(oldName, newName)
                    parentControl = NJE_MakeControl(newName, parentControl)
                    NJE_MasterConstrain(parentControl, newName)
                else:
                    #print oldName
                    cmds.delete(oldName) #Delete joint without the controlTypeRK_string
                    break
            cmds.parent(jointFK[0], groupFK)


            # Work on IK joints
            # Note: IK end joints are oriented to the world (not pv control)
            jointIK = cmds.duplicate(jointRK, name=jointRK.replace(controlTypeRK_string, controlTypeIK_string), renameChildren=True) #Duplicate and rename joint
            ikBase = NJE_MakeControl(jointIK[0], IKControlGroup)
            #cmds.makeIdentity(cmds.listRelatives(ikBase, parent=True), apply=True)
            for oldName in jointIK[1:]: #Renameing all joint desendents
                if controlTypeRK_string in oldName:
                    newName = oldName.replace(controlTypeRK_string, controlTypeIK_string)[0:-1]
                    cmds.rename(oldName, newName)
                else:
                    ikControl = NJE_MakeControl(newName, IKControlGroup)
                    #cmds.makeIdentity(cmds.listRelatives(ikControl, parent=True), apply=True)
                    ikHandle = cmds.ikHandle(name=newName+"_Handle", sj=jointIK[0], ee=newName)
                    ikHandleGroup += [ikHandle[0]]
                    cmds.parent(ikHandle[0], ikControl)
                    cmds.hide(ikHandle)
                    cmds.delete(oldName) #Delete joint without the controlTypeRK_string
                    break
            cmds.parent(jointIK[0], groupIK)
            cmds.parentConstraint(ikBase, jointIK[0])
        # Make PV controls (note: may need to fix up)
        print ikHandleGroup
        pvControl = NJE_MakePVControl(newName, IKControlGroup, -controlSize)
        print pvControl
        print ikHandleGroup[1]
        cmds.poleVectorConstraint(pvControl, ikHandleGroup[1])
        pvControl = NJE_MakePVControl(newName.replace(sideNew_string, sideOld_string), IKControlGroup)
        print pvControl
        print ikHandleGroup[0]
        cmds.poleVectorConstraint(pvControl, ikHandleGroup[0])

        cmds.parent(allJoint, groupRK)

def NJE_Rig(baseJointList, RKJointList):
    parent = groupControls
    parent = NJE_MakeTransformControl(parent)
    parentCOG = parent

    # Make controls for non-RK joints then constrain
    for joint in baseJointList:
        if "COG" in joint:
            parent = NJE_MakeControl(joint, parent, 8*controlSize)
            NJE_MasterConstrain(parent, joint)
            parentCOG = parent
        else:
            parent = cmds.listRelatives(joint, parent=True)[0].replace(nodeJoint_string, nodeControl_string)
            ctrl = NJE_MakeControl(joint, parent)
            NJE_MasterConstrain(ctrl, joint)
            #print parent.replace(nodeControl_string, nodeJoint_string)
            #print parent

    # Make controls for joints at the end of RK joints then constrain
    for joint in RKJointList:
        parent = cmds.listRelatives(joint, parent=True)[0].replace(nodeJoint_string, nodeControl_string)
        jointList = cmds.listRelatives(joint, allDescendents=True)
        jointList.reverse()
        parent = parentCOG
        for jnt in jointList:
            if controlTypeRK_string not in jnt:
                # Note: Need to make digets auto control
                parent = NJE_MakeControl(jnt, parent)
                NJE_MasterConstrain(parent, jnt)

    cmds.parent(groupFKControls, parentCOG)
    cmds.parent(groupIKControls, parentCOG)
    #print parent
    #print parentCOG

def NJE_SortJointAndRig(selectionCOG):
    COG = selectionCOG
    BuildRigGroups()
    cmds.parent(COG, groupJoints)

    # Create vars to find RK joints
    allJoints = cmds.listRelatives(COG, allDescendents=True)
    allJoints.reverse()
    RKJoints = []

    # Find and Rig base RK joints
    count=0
    for jnt in allJoints:
        if controlTypeRK_string in jnt and count == 0:
            count=1
            RKJoints += [jnt]
        if controlTypeRK_string not in jnt:
            count=0
    NJE_MirrorAndRig(RKJoints)

    # Reset vars to find all non RK FK and IK joints
    allJoints = cmds.listRelatives(COG, allDescendents=True, type='joint')
    allJoints.reverse()
    notRKJoints = selectionCOG
    #RKJoints = []

    # Find and Rig all non RK joints
    count=0
    for jnt in allJoints:
        if (controlTypeRK_string in jnt) and (count == 0):
            count=1
            RKJoints += [jnt]
        if (controlTypeRK_string not in jnt) and (controlTypeFK_string not in jnt) and (controlTypeIK_string not in jnt) \
                and (sideOld_string not in jnt) and (sideNew_string not in jnt):
            count=0
            notRKJoints += [jnt]
    #print RKJoints
    NJE_Rig(notRKJoints, RKJoints)

NJE_SortJointAndRig(cmds.ls(selection=True))



#print cmds.ls(selection=True)
#NJE_MirrorAndRig(cmds.ls(selection=True))






# CONTROLS
#parentControl = cmds.group( empty = True, name = 'IK_Control_Group' )
#masterControlGroup = parentControl

#NJE_MakeControl( "L_Arm_01_Jnt_RK", parentControl)


#def NJE_AutoControls():




