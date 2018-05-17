from glob import glob
import sys
import yaml

DEPENDENCY_KEY = 'dependencies'
INDENT = " *"

#### ROLE class
class Role:
    name = ""
    path = ""

    def __init__(self, givenPath):
        self.name = truncate_to_role(givenPath).split('/')[1]
        self.path = givenPath

def truncate_to_role(path):
    idx = path.index('role')
    return path[idx:]

def print_dependencies(role, name_to_role, indent):
    indent += INDENT
    file = open(role.path,"r")
    meta = yaml.save_load(file)
    for dependency in meta[DEPENDENCY_KEY]:
        name = dependency['name']
        childRole = name_to_role[name]
        print indent + childRole.name
        print_dependencies(childRole,name_to_role,indent)

############ start main script ############

# allow user to specify dir. if none use working dir
meta_path = ""
if (len(sys.argv) > 1):
    meta_path = str(sys.argv[1]) + "/"
meta_path = meta_path + "roles/*/meta/main.yml"

print("playbook path: " + meta_path + "\n")
print("Dependencies:")

# get all roles and paths
name_to_role = {}
for path in glob(meta_path):
    role = Role(path)
    name_to_role[role.name] = role

# build dependency tree
for role in name_to_role.values():
    print "------------------"
    print role.name_to_role
    print_dependencies(role, name_to_role,"")
    print "------------------"
    print "|"
