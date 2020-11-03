import maya.cmds as cmds

#Variables
selectionGroupRK = cmds.ls( selection=True );
selectionFirstJointInRK = cmds.listRelatives(selectionGroupRK[0], children=True, type='joint')[0];
selectionParentOfGroupRK = cmds.listRelatives(selectionGroupRK[0], parent=True, type='joint')[0];
lastJointForIKFK = 'L_Wrist_Jnt_RK';

stringSideToReplace = 'L_';
stringSideReplaceWith = 'R_';

stringRKToReplace = 'RK';
stringIKReplaceWith = 'IK';
stringFKReplaceWith = 'FK';

#print selectionParentOfGroupRK;

#Mirror Joints
mirroredRKJoint = cmds.mirrorJoint ( selectionFirstJointInRK, mirrorYZ=True, mirrorBehavior=True, searchReplace=[stringSideToReplace, stringSideReplaceWith] );

#Create RK Mirrored group
mirroredRKJointGroup = cmds.group( mirroredRKJoint[0], name='R_Arm_Group_RK', parent=selectionParentOfGroupRK );

#Group RK limb Groups into one RK Group
selectionGroupRK = cmds.group( [selectionGroupRK[0], mirroredRKJointGroup], name='RK_Joints_Group', parent=selectionParentOfGroupRK );

#Create IK Group
selectionGroupIK = cmds.duplicate(selectionGroupRK, name = selectionGroupRK.replace(stringRKToReplace, stringIKReplaceWith), renameChildren=True);
for obj in selectionGroupIK[1:]: #Rename desendents in IK group
    newName = obj.replace(stringRKToReplace, stringIKReplaceWith)[0:-1]
    cmds.rename(obj, newName)

#Create FK Group
selectionGroupFK = cmds.duplicate(selectionGroupRK, name = selectionGroupRK.replace(stringRKToReplace, stringFKReplaceWith), renameChildren=True);
for obj in selectionGroupFK[1:]: #Rename desendents in FK group
    newName = obj.replace(stringRKToReplace, stringFKReplaceWith)[0:-1]
    cmds.rename(obj, newName)

#Replace RK indicator with FK indicator
selectionGroupFK = selectionGroupRK.replace(stringRKToReplace, stringFKReplaceWith);

#Find and delete the childs of the joints in the 'lastJointForIKFK' Var for all of the IK and FK lists
cmds.delete( cmds.listRelatives(lastJointForIKFK.replace(stringRKToReplace, stringIKReplaceWith), children=True) );
cmds.delete( cmds.listRelatives(lastJointForIKFK.replace(stringRKToReplace, stringFKReplaceWith), children=True) );
lastJointForIKFK = lastJointForIKFK.replace(stringSideToReplace, stringSideReplaceWith)
cmds.delete( cmds.listRelatives(lastJointForIKFK.replace(stringRKToReplace, stringIKReplaceWith), children=True) );
cmds.delete( cmds.listRelatives(lastJointForIKFK.replace(stringRKToReplace, stringFKReplaceWith), children=True) );

#Put RK Left and Right group joints into 2 seporate lists
originRKGroup = cmds.listRelatives(cmds.listRelatives(selectionGroupRK, children=True)[0], allDescendents=True, type='joint');
otherRKGroup = cmds.listRelatives(cmds.listRelatives(selectionGroupRK, children=True)[1], allDescendents=True, type='joint');

#Put IK Left and Right group joints into 2 seporate lists
originIKGroup = cmds.listRelatives(cmds.listRelatives(selectionGroupRK.replace(stringRKToReplace, stringIKReplaceWith), children=True)[0], allDescendents=True, type='joint');
otherIKGroup = cmds.listRelatives(cmds.listRelatives(selectionGroupRK.replace(stringRKToReplace, stringIKReplaceWith), children=True)[1], allDescendents=True, type='joint');

#Put FK Left and Right group joints into 2 seporate lists
originFKGroup = cmds.listRelatives(cmds.listRelatives(selectionGroupRK.replace(stringRKToReplace, stringFKReplaceWith), children=True)[0], allDescendents=True, type='joint');
otherFKGroup = cmds.listRelatives(cmds.listRelatives(selectionGroupRK.replace(stringRKToReplace, stringFKReplaceWith), children=True)[1], allDescendents=True, type='joint');

#Maybe add colors
#Make _Controls master group to put all controls in
parentControl = cmds.group( empty = True, name = 'FK_Control_Group' );
masterControlGroup = parentControl;

#Make a colord control (and groups) for each FK joint and orient them properly
n = 0;
originFKGroup.reverse(); #reverses the order of the group
for obj in originFKGroup:
    newName = originFKGroup[n].replace('Jnt', 'Ctrl');
    newControl = cmds.circle( name = newName );
    cmds.setAttr( newControl[0]+'.rotateY', 90 );
    newControlGroup = cmds.group(newControl, name = newName + 'Grp', parent = parentControl);
    cmds.matchTransform(newControlGroup, originFKGroup[n]);
    cmds.makeIdentity(newControl[0], apply = True);
    parentControl = newControl[0];
    n += 1;

parentControl = masterControlGroup;
n = 0;
otherFKGroup.reverse(); #reverses the order of the group
for obj in otherFKGroup:
    newName = otherFKGroup[n].replace('Jnt', 'Ctrl');
    newControl = cmds.circle( name = newName );
    cmds.setAttr( newControl[0]+'.rotateY', 90 );
    newControlGroup = cmds.group(newControl, name = newName + 'Grp', parent = parentControl);
    cmds.matchTransform(newControlGroup, otherFKGroup[n]);
    cmds.makeIdentity(newControl[0], apply = True);
    parentControl = newControl[0];
    n += 1;

#Make a colord control (and groups) for the begining and the end of the IK joints and orient them properly
# Original Side
parentControl = cmds.group( empty = True, name = 'IK_Control_Group' );
masterControlGroup = parentControl;

newName = originIKGroup[-1].replace('Jnt', 'Ctrl');
newControl = cmds.circle(name=newName);
cmds.setAttr(newControl[0] + '.rotateY', 90);
newControlGroup = cmds.group(newControl, name=newName + 'Grp', parent=parentControl);
cmds.matchTransform(newControlGroup, originIKGroup[0]);
cmds.makeIdentity(newControl[0], apply=True);

newName = originIKGroup[-1].replace('Jnt', 'Base_Ctrl');
newControl = cmds.circle(name=newName);
cmds.setAttr(newControl[0] + '.rotateY', 90);
newControlGroup = cmds.group(newControl, name=newName + 'Grp', parent=parentControl);
cmds.matchTransform(newControlGroup, originIKGroup[-1]);
cmds.makeIdentity(newControl[0], apply=True);
# Other side
newName = otherIKGroup[-1].replace('Jnt', 'Ctrl');
newControl = cmds.circle(name=newName);
cmds.setAttr(newControl[0] + '.rotateY', 90);
newControlGroup = cmds.group(newControl, name=newName + 'Grp', parent=parentControl);
cmds.matchTransform(newControlGroup, otherIKGroup[0]);
cmds.makeIdentity(newControl[0], apply=True);

newName = otherIKGroup[-1].replace('Jnt', 'Base_Ctrl');
newControl = cmds.circle(name=newName);
cmds.setAttr(newControl[0] + '.rotateY', 90);
newControlGroup = cmds.group(newControl, name=newName + 'Grp', parent=parentControl);
cmds.matchTransform(newControlGroup, otherIKGroup[-1]);
cmds.makeIdentity(newControl[0], apply=True);

#Make an IK PV control for the IK joints and orient them properly
newName = originIKGroup[-1].replace('Jnt', 'PV_Offset_Grp');
newPV = cmds.circle(name=newName);
selectShapeNode = cmds.listRelatives(newPV[0], shapes=True);
cmds.delete(selectShapeNode);
newName = originIKGroup[-1].replace('Jnt', 'PV_Ctrl');
newControl = cmds.circle(name=newName);
#cmds.select(newControl.cv.[0,2,4,6]);
#cmds.scale( newControl.cv.[0,2,4,6], relative = True, pivot = (-9cm, 0, 0) )
cmds.parent(newControl, newPV);
newControlGroup = cmds.group(newPV, name=newName + 'Grp', parent=parentControl);
cmds.matchTransform(newControlGroup, originIKGroup[-2]);
cmds.setAttr(newPV[0] + '.translateY', -10);
cmds.makeIdentity(newControl[0], apply=True);

newName = otherIKGroup[-1].replace('Jnt', 'PV_Offset_Grp');
newPV = cmds.circle(name=newName);
selectShapeNode = cmds.listRelatives(newPV[0], shapes=True);
cmds.delete(selectShapeNode);
newName = otherIKGroup[-1].replace('Jnt', 'PV_Ctrl');
newControl = cmds.circle(name=newName);
#cmds.select(newControl.cv.[0,2,4,6]);
#cmds.scale( newControl.cv.[0,2,4,6], relative = True, pivot = (-9cm, 0, 0) )
cmds.parent(newControl, newPV);
newControlGroup = cmds.group(newPV, name=newName + 'Grp', parent=parentControl);
cmds.matchTransform(newControlGroup, otherIKGroup[-2]);
cmds.setAttr(newPV[0] + '.translateY', 10);
cmds.makeIdentity(newControl[0], apply=True);

#Make a colord control (and groups) for each RK joint after the 'lastJointForIKFK' Var and orient them properly
# Original RK Controls
parentControl = cmds.group( empty = True, name = 'RK_Control_Group' );
masterControlGroup = parentControl;

n = 0;
originRKGroup.reverse(); #reverses the order of the group
controlListForRK = originRKGroup[originRKGroup.index(lastJointForIKFK.replace(stringSideReplaceWith, stringSideToReplace))+1:]

for obj in controlListForRK:
    if cmds.listRelatives(controlListForRK[n], children=True, type='joint') != None:
        newName = controlListForRK[n].replace('Jnt', 'Ctrl');
        newControl = cmds.circle( name = newName );
        cmds.setAttr( newControl[0]+'.rotateY', 90 );
        newControlGroup = cmds.group(newControl, name = newName + 'Grp', parent = parentControl);
        cmds.matchTransform(newControlGroup, controlListForRK[n]);
        cmds.makeIdentity(newControl[0], apply = True);

        if len(cmds.listRelatives(controlListForRK[n], children=True, type='joint')) > 1:
            parentControl = newControl[0];
    n += 1;

# Other RK Controls
parentControl = masterControlGroup;
n = 0;
otherRKGroup.reverse(); #reverses the order of the group
controlListForRK = otherRKGroup[otherRKGroup.index(lastJointForIKFK)+1:]
for obj in controlListForRK:
    if cmds.listRelatives(controlListForRK[n], children=True, type='joint') != None:

        newName = controlListForRK[n].replace('Jnt', 'Ctrl');
        newControl = cmds.circle( name = newName );
        cmds.setAttr( newControl[0]+'.rotateY', 90 );
        newControlGroup = cmds.group(newControl, name = newName + 'Grp', parent = parentControl);
        cmds.matchTransform(newControlGroup, controlListForRK[n]);
        cmds.makeIdentity(newControl[0], apply = True);

        if len(cmds.listRelatives(controlListForRK[n], children=True, type='joint')) > 1:
            parentControl = newControl[0];
    n += 1;

#To Do Next:
#Bind the RK to the IK and FK joints correctly

#Bind each control to the correct joint

#Remind user to bind joints to the mesh.



