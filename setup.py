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

from plugin import *

P = create_plugin_instance(setting)
from .setup import P
from . import ModuleMain
P.set_module_list([ModuleMain])


