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

#To Do Next:
#Make _Controls master group to put all controls in
parentControl = cmds.group( empty = True, name = 'FK_Control_Group' );
masterControlGroup = parentControl;

#Make a colord control (and groups) for each FK joint and orient them properly
n = 0;
originFKGroup.reverse(); #reverses the order of the group
for obj in originFKGroup:
    newName = originFKGroup[n].replace(stringFKReplaceWith, '').replace('Jnt', 'Ctrl');
    newControl = cmds.circle( name = newName );
    # Add rotate circle control
    newControlGroup = cmds.group(newControl, name = newName + 'Grp', parent = parentControl);
    cmds.matchTransform(newControlGroup, originFKGroup[n]);
    #Add freaze transforms
    parentControl = newControl[0];
    n += 1;

parentControl = masterControlGroup;
n = 0;
otherFKGroup.reverse(); #reverses the order of the group
for obj in otherFKGroup:
    newName = otherFKGroup[n].replace(stringFKReplaceWith, '').replace('Jnt', 'Ctrl');
    newControl = cmds.circle( name = newName );
    #Add rotate circle control
    newControlGroup = cmds.group(newControl, name = newName + 'Grp', parent = parentControl);
    cmds.matchTransform(newControlGroup, otherFKGroup[n]);
    #Add freaze transforms
    parentControl = newControl[0];
    n += 1;

#Make a colord control (and groups) for the begining and the end of the IK joints and orient them properly
#Make an IK PV control for the IK joints and orient them properly
#Make a colord control (and groups) for each RK joint after the 'lastJointForIKFK' Var and orient them properly

#Bind the RK to the IK and FK joints correctly
#Bind each control to the correct joint

#Remind user to bind joints to the mesh.



