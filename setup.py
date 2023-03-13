__menu = {
    'uri': __package__,
    'name': 'MAKE_YAML',
    'list': [
        {
            'uri': 'main',
            'name': 'Main',
            'list': [
                {"uri": "setting", "name": "설정"},
                {"uri": "main", "name": "코드"},
            ],
        },
        {
        'uri': 'manual',
        'name': '매뉴얼',
        'list': [
            {'uri':'README.md', 'name':'README.md'}
        ]
        },
        {
            'uri': 'log',
            'name': '로그',
        },
    ]
}


setting = {
    'filepath' : __file__,
    'use_db': True,
    'use_default_setting': True,
    'home_module': 'main',
    'menu': __menu,
    'setting_menu': None,
    'default_route': 'normal',
}

DEFINE_DEV = False

from plugin import *

P = create_plugin_instance(setting)
from .mod_main import ModuleMain
P.set_module_list([ModuleMain])
# try:
#     if DEFINE_DEV and os.path.exists(os.path.join(os.path.dirname(__file__), 'mod_main.py')):
#         from .mod_main import ModuleMain
#     else:
#         from support import SupportSC
#         ModuleMain = SupportSC.load_module_P(P, 'mod_main').ModuleMain

#     P.set_module_list([ModuleMain])
# except Exception as e:
#     P.logger.error(f'Exception:{str(e)}')
#     P.logger.error(traceback.format_exc())


