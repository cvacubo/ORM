from sqlalchemy.orm import joinedload
import transaction
from orm.models import DBSession, AppUser, AppUserBalance
from orm.models import Parent, Child

OK_RESPONSE = 'OK'

def my_view(request):
    dbsession = DBSession()
    root = dbsession.query(Parent).filter(Parent.name == u'Alexander').first()
    return {'root': root.name, 'project':'ORM'}


def get_parents(dbsession):

    #print "\n Get parent and child\n--------------------------------------------"
    parents = dbsession.query(Parent).all()

    #for parent in parents:
    #    print "\n Parent name is %s" % parent.name
    #    for child in parent.children:
    #        print "\tChild name is %s" % child.name

    #print "==============================================================="
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


    #print "\n 3. Check if parent has children"
    parents = dbsession.query(Parent).all()

    info = {}
    ret_info = []

    for parent in parents:
        if is_has_child(parent):
            #print "\n Parent %s has children" % parent.name

            info['children'] = "yes"

            #for child in parent.children:
            #    print "\tchild.id = %s, child.name = %s" % (str(child.id), str(child.name))
        else:
            #print "\n Parent %s hasn't children" % parent.name

            info['children'] = "no"

        info['parent'] = parent.name
        ret_info.append(info)
        info = {}


    return ret_info

def view_all_parents(request):

    dbsession = DBSession()

    #parents_and_childs = dbsession.query(Parent).filter_by(name == 'Alexander', id == 1).all()
    parents_and_childs = dbsession.query(Parent).filter(Parent.id == 1).filter(Parent.name == 'Alexander').scalar()

    print parents_and_childs.__dict__

    #return OK_RESPONSE
    return parents_and_childs if parents_and_childs is not None else "NONE"


def view_balance(request):

    dbsession = DBSession()

    user_id = 1
    #user = dbsession.query(AppUserBalance).filter(AppUserBalance.id == user_id).scalar()
    #print user.app_user.__dict__

    user = dbsession.query(AppUserBalance).options(joinedload(AppUserBalance.app_user)).filter(AppUserBalance.app_user_id == user_id).scalar()

    if not user:
        app_user = AppUser(1, 'artem.com')
        user = AppUserBalance(app_user, 0)
        dbsession.add(user)
        dbsession.flush()

    vbalance = user.balance + 1000

    if vbalance < 0:
        print "ZERO"

    user.balance = vbalance
    #print user.name
    #print user.balance

    print user.__dict__
    print vbalance

    return "YES"
