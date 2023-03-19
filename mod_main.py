from flask import render_template, jsonify
from plugin import PluginModuleBase
from tool import ToolUtil
from .setup import P
from support_site import SiteUtil
from .yaml_utils import YAMLUTILS
import re, os, traceback, copy
logger = P.logger
DEFINE_DEV = False
if os.path.exists(os.path.join(os.path.dirname(__file__), 'mod_basic.py')):
    DEFINE_DEV = True
try:
    if DEFINE_DEV:
        from .get_code import OTTCODE
    else:
        from support import SupportSC
        OTTCODE = SupportSC.load_module_P(P, 'get_code').OTTCODE

except Exception as e:
    P.logger.error(f'Exception:{str(e)}')
    P.logger.error(traceback.format_exc())

name = 'main'

class ModuleMain(PluginModuleBase):
    
    db_default = {
        f'{name}_db_version' : '1',
        f'ftv_first_order' : 'WAVVE, TVING, COUPANG, NF, DSNP, AMZN, ATVP',
        f'is_primary' : 'false',
        f'match_score' : '95',
        f'extra_season' : 'True',
        f'split_season' : '1',
        f'delete_title' : 'True',
        f'manual_target' : '',
    }
    
    def __init__(self, P):
        super(ModuleMain, self).__init__(P, name=name, first_menu='main')

    def process_menu(self, sub, req):
        arg = P.ModelSetting.to_dict()
        arg["package_name"] = P.package_name
        arg["module_name"] = self.name
        if sub == "setting":
            return render_template(f"{P.package_name}_{self.name}_{sub}.html", arg=arg)
        return render_template(f"{P.package_name}_{self.name}.html", arg=arg, sub=sub)
    
        
    def process_command(self, command, arg1, arg2, arg3, req):
        self.code = ''
        arg1 = arg1.strip()
        if command == 'search_keyword':
            keyword = arg1.split('|')
            if len(keyword) == 1:
                ottcode = OTTCODE(keyword[0].strip())
                ottcode_list = ottcode.get_ott_code()
                user_order = P.ModelSetting.get_list('ftv_first_order', ',')
                self.code = YAMLUTILS.code_sort(user_order, ottcode_list)
            elif len(keyword) == 2:
                ottcode = OTTCODE(keyword[0].strip(), keyword[1].strip())
                ottcode_list = ottcode.get_ott_code()
                user_order = P.ModelSetting.get_list('ftv_first_order', ',')
                self.code = YAMLUTILS.code_sort(user_order, ottcode_list)
            else:
                return jsonify({"msg":"검색어 실패", "ret":"fail"})
        elif command == 'wavve_code':
            self.code = 'KW'+arg1
        elif command == 'tving_code':
            self.code = 'KV'+arg1
        elif command == 'cpang_code':
            self.code = 'KC'+arg1
        elif command == 'nf_code':
            self.code = 'FN'+arg1
        elif command == 'dsnp_code':
            self.code = 'FD'+arg1
        elif command == 'amzn_code':
            self.code = 'FP'+arg1
        elif command == 'atvp_code':
            self.code = 'FA'+arg1
        elif command == 'ebskids_code':
            self.code = 'KE'+arg1
        if self.code != '' and self.code != None :
            site = self.code[:2]
            site_name_dict = {
                'KW' : '웨이브', 'KV' : '티빙', 'KC' : '쿠팡 플레이', 'FN' : '넷플릭스', 'FD' : '디즈니 플러스', 'FP' : '프라임 비디오', 'FA' : '애플TV', 'KE' : 'EBS',
            }
            show_data = YAMLUTILS.get_data(self.code)
            if arg2 == 'test':
                return jsonify({'ret':'success', 'json': show_data})
            elif show_data !=[]:
                if SiteUtil.is_include_hangul(show_data['seasons'][-1]['episodes'][-1]['title']) or SiteUtil.is_include_hangul(show_data['seasons'][-1]['episodes'][-1]['summary']) :
                    if P.ModelSetting.get_bool('is_primary'):
                        self.tmdb_code = 'FT'+str(ottcode.tmdb_search()) 
                        show_data = YAMLUTILS.tmdb_data(self.tmdb_code, show_data)
                        
                    if P.ModelSetting.get_int('split_season') == 1:   
                        YAMLUTILS.make_yaml(show_data)
                        return jsonify({"msg":f"{site_name_dict[site]} 코드 실행", "ret":"success"})
                    else:
                        season_data = []
                        split_season = P.ModelSetting.get_int('split_season')
                        for k in range(len(show_data['seasons'])):
                            i = int(show_data['seasons'][k]['index'])
                            for j in range(split_season):
                                episode_data = copy.deepcopy(show_data['seasons'][k]['episodes'])
                                season_no = int(int(j)*100 + i )                                  
                                season = {
                                    'index' : season_no,
                                    'episodes' : episode_data
                                }
                                season_data.append(season)
                        show_data['seasons'] = season_data
                        YAMLUTILS.make_yaml(show_data)
                        return jsonify({"msg":f"{site_name_dict[site]} 코드 실행", "ret":"success"})
                else:
                    return jsonify({"msg":f"{site_name_dict[site]} 한글 메타데이터 아님", "ret":"success"})
            else:
                return jsonify({"msg":"검색 실패", "ret":"success"})
        else:
            return jsonify({"msg":"검색 실패", "ret":"success"})
    
