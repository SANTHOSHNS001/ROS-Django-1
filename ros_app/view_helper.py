from .models import *

def get_user_projects(user):
    """
    Returns a dictionary containing projects where the user is either
    a Project Manager or a Document Manager.
    """
    #Get the projjects assigned to the user
    

    return {
        "pm_projects": pm_projects,
        "dm_projects": dm_projects
    }
