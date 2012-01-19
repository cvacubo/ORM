from orm.models import Parent, Child

def make_parent_with_child(parent_name, child_name):
    child = Child(child_name)
    parent = Parent(parent_name)

    parent.children.append(child)

    return parent

def make_parent(parent_name):
    return Parent(parent_name)