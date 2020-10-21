import maya.cmds as cmds

#Pick how may body segments here!
snowManSegments = 53;
allObjects = [];

#Build the body
i = 0;
while i < snowManSegments:
    selectedGeo = cmds.polySphere(name='SnowBall_Geo',
                                  subdivisionsHeight=16,
                                  subdivisionsAxis=16);
    cmds.move(0, (1.5 * i) + 1, 0, selectedGeo);
    allObjects.append(selectedGeo);

    selectedGeo = cmds.polySphere(name='Button_Geo',
                                  subdivisionsHeight=16,
                                  subdivisionsAxis=16);
    cmds.move(0.95, (1.5 * i) + 1, 0, selectedGeo);
    cmds.scale(0.1, 0.1, 0.1, selectedGeo);
    allObjects.append(selectedGeo);
    i += 1;

#Build the Head
selectedGeo = cmds.polySphere(name='SnowHead_Geo',
                              subdivisionsHeight=16,
                              subdivisionsAxis=16);
cmds.move(0, (1.5 * snowManSegments) + 1, 0, selectedGeo);
allObjects.append(selectedGeo);

selectedGeo = cmds.polyCone(name='SnowManNose_Geo',
                              subdivisionsAxis=16);
cmds.move(0.95, (1.5 * snowManSegments) + 1, 0, selectedGeo);
cmds.scale(0.5, 1, 0.5, selectedGeo);
cmds.rotate(0, 0, -90, selectedGeo);
allObjects.append(selectedGeo);


#Build the Hat
selectedGeo = cmds.polyCylinder(name='SnowManHat_Geo',
                                subdivisionsAxis=16,
                              subdivisionsHeight=6);
cmds.move(0, (1.5 * snowManSegments) + 2.5, 0, selectedGeo);
#cmds.select(add=selectedGeo.f[0:19]);
allObjects.append(selectedGeo);

selectedGeo = cmds.polyCylinder(name='SnowManHatBrim_Geo',
                                subdivisionsAxis=16);
cmds.scale(1.5, 0.2, 1.5, selectedGeo);
cmds.move(0, (1.5 * snowManSegments) + 1.5, 0, selectedGeo);
allObjects.append(selectedGeo);

#Group all objects together
#cmds.group(allObjects, name='Snoman_Geo_Group');
print allObjects;