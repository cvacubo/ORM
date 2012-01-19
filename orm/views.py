from pyramid.response import Response
import transaction
from orm.models import DBSession
from orm.models import Parent, Child

#def my_view(request):
#    dbsession = DBSession()
#    root = dbsession.query(MyModel).filter(MyModel.name==u'root').first()
#    return {'root':root, 'project':'ORM'}


def get_parents(dbsession):

    print "\n Get parent and child\n--------------------------------------------"
    parents = dbsession.query(Parent).all()

    for parent in parents:
        print "\n Parent name is %s" % parent.name
        for child in parent.children:
            print "\tChild name is %s" % child.name

    print "==============================================================="
    return parents

def add_child(dbsession, parents):
    # Adding another child

    new_child = Child("Arthur")
    parents[0].children.append(new_child)

    dbsession.add(new_child)
    dbsession.flush()
    transaction.commit()

def is_has_child(parent):
    return parent.children

def view_relations(request):

    dbsession = DBSession()

    parents = get_parents(dbsession)
    add_child(dbsession, parents)
    parents = get_parents(dbsession)


    print "\n 3. Check if parent has children"
    parents = dbsession.query(Parent).all()

    info = {}
    ret_info = []

    for parent in parents:
        if is_has_child(parent):
            print "\n Parent %s has children" % parent.name

            info['children'] = "yes"

            for child in parent.children:
                print "\tchild.id = %s, child.name = %s" % (str(child.id), str(child.name))
        else:
            print "\n Parent %s hasn't children" % parent.name

            info['children'] = "no"

        info['parent'] = parent.name
        ret_info.append(info)
        info = {}


    #print ret_info
    return ret_info

    #return Response('OK')