from .api_requests import *
import importlib


def load_modules(scripting_option):
    if scripting_option:
        from . import parametric_study
        from . import constellation
        from . import deployment
        from . import simulation
        from . import gridfs
        from . import formation_flying
        from . import inspection
    else:
        print('SCRIPTING NOT ACTIVATED, CONTACT THE SUPPORT TEAM')
