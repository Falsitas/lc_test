def is_admin(user):
    return user.groups.filter(name='admin').exists()

def is_aplha(user):
    return user.groups.filter(name='ALPHA').exists()

def is_beta(user):
    return user.groups.filter(name='BETA').exists()