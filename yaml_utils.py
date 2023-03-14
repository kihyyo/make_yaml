import re, difflib, requests, os, traceback, yaml
import tmdbsimple as tmdb
from .setup import P
from urllib.parse import unquote, quote
from support import SupportSC
TVING = SupportSC.load_module_P(P, 'site_tving').TVING
NF = SupportSC.load_module_P(P, 'site_netflix').NF
WAVVE = SupportSC.load_module_P(P, 'site_wavve').WAVVE
DSNP = SupportSC.load_module_P(P, 'site_disney').DSNP
COUPANG = SupportSC.load_module_P(P, 'site_coupang').COUPANG
ATVP = SupportSC.load_module_P(P, 'site_appletv').ATVP
AMZN = SupportSC.load_module_P(P, 'site_prime').AMZN
EBS = SupportSC.load_module_P(P, 'site_ebs').EBS
logger = P.logger

class YAMLUTILS(object):

    @classmethod
    def make_yaml(self, show_data, target_path=None):
            target_path = P.ModelSetting.get('manual_target')
            tmp = re.sub('[\\/:*?\"<>|]', '', show_data['title']).replace('  ', ' ').replace('[]', '').strip()
            with open(os.path.join(target_path, tmp+'.yaml'), 'w', encoding="utf-8") as outfile:
                del show_data['title']
                yaml.dump(show_data, outfile, sort_keys=False, allow_unicode=True)
                
    @classmethod            
    def code_sort(cls, user_order, url_list):
        if type(user_order) != list:
            try:
                user_order = user_order.split(',')
            except Exception as e: 
                logger.error(f"Exception:{str(e)}")
                logger.error(traceback.format_exc())
        regex_set = {
            'wavve' : r'wavve\.com\/player\/(vod\?contentid=|vod\?programid=.*?)(?P<code>[^_]+_[^_]+)$', 'tving': r'tving\.(com\/contents)\/(?P<code>.*?)$', 
            'coupang' : r'coupangplay\.com\/titles\/(?P<code>[^/]+)$', 'nf' :r'netflix\.com\/(kr\/title|title)\/(?P<code>[^/]+)$', 'dsnp' : r'disneyplus.com/.*?(?P<code>[^/]+)$',
            'atvp' : 'apple.com/.*?(?P<code>umc.cmc.[a-zA-Z0-9]+)$', 'amzn' : r'primevideo\.com/detail/(?P<code>[A-Z0-9]+)'
        }
        site_list = ['KW', 'KV', 'KC', 'FN', 'FD', 'FA', 'FP']
        try:
            for order in user_order:
                for url in url_list:
                    match = re.search(regex_set[order.lower()], url)
                    if match:
                        code = site_list[list(regex_set).index(order.lower())]+match.group('code')
                        return code 
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc())
            
            
    @classmethod   
    def get_data(cls, code):
        site = code[:2]
        code = code[2:]
        site_dict = {'KW' : WAVVE, 'KV' : TVING, 'KC' : COUPANG, 'FN' : NF, 'FD' : DSNP, 'FA' : ATVP, 'FP' : AMZN, 'KE' : EBS}
        show_data = site_dict[site].make_data(code)
        return show_data
