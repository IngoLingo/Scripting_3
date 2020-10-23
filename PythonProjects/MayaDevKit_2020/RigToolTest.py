import maya.cmds as cmds

#Variables
selectionGroupRK = cmds.ls( selection=True );
selectionFirstJointInRK = cmds.listRelatives(selectionGroupRK[0], children=True, type='joint')[0];
selectionParentOfGroupRK = cmds.listRelatives(selectionGroupRK[0], parent=True, type='joint')[0];
lastJointForIK_FK = 'L_Wrist_Jnt_RK';

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

selectionGroupFK = selectionGroupRK.replace(stringRKToReplace, stringFKReplaceWith);

#print selectionGroupFK[0:];

#print cmds.listRelatives(selectionGroupFK, allDescendents=True, type='joint')[3:];