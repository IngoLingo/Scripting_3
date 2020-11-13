import maya.cmds as cmds

name_string = 'Cube_###_Obj'

char_list = list(name_string)

sels = cmds.ls(sl=True)

# returns the number of '#'
hash_num = name_string.count('#')

# returns ('Cube_', '###', '_Obj')
parts = name_string.partition('#' * hash_num)

# returns the first instances index 5
piece = name_string.find("#")
print 'piece starts as ', piece

# returns last index location of # 7
index_num = (piece + hash_num)
print 'index number: ', index_num

hash_list = []
end_hash = index_num - 1

for i in range(piece, end_hash, 1):
    hash = char_list.pop(i)
    hash_list.extend(hash)
    print 'i is', i, 'popped characters ', hash

new_name_string = ''.join(char_list)
print new_name_string

replace_num_string = '1'
replace_num_int = 1
replace_index = (name_string[piece : index_num])
print 'replace index ', replace_index

final_name_string = ""
if parts[1]:
    print 'Characters are sequential'
    for s in sels:
        new_num = replace_num_string.zfill(hash_num)
        print 'the new num is', new_num
        final_name_string = new_name_string.replace('#', new_num)
        print 'the new name is ', final_name_string
        print 'the replace num is ', type(replace_num_int)
        replace_num_int += 1
        print 'the replace num is ', replace_num_int
        replace_num_string = str(replace_num_int)
        cmds.rename(final_name_string)
        replace_num = str(replace_num)
else:
    cmds.error('Characters are not sequential. Input another string.')