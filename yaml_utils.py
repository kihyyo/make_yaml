import re, difflib, requests, os, traceback, yaml
from urllib.parse import unquote, quote
import tmdbsimple as tmdb
from .setup import P
logger = P.logger
DEFIㅆNE_DEV = False
if os.path.exists(os.path.join(os.path.dirname(__file__), 'mod_basic.py')):
    DEFINE_DEV = True
try:
    if DEFINE_DEV:
        from .get_code import OTTCODE
        from .site_wavve import WAVVE
        from .site_tving import TVING
        from .site_netflix import NF
        from .site_disney import DSNP
        from .site_coupang import COUPANG
        from .site_appletv import ATVP
        from .site_prime import AMZN
        from .site_ebs import EBS
    else:
        from support import SupportSC
        OTTCODE = SupportSC.load_module_P(P, 'get_code').OTTCODE
        WAVVE = SupportSC.load_module_P(P, 'site_wavve').WAVVE
        TVING = SupportSC.load_module_P(P, 'site_tving').TVING
        NF = SupportSC.load_module_P(P, 'site_netflix').NF
        DSNP = SupportSC.load_module_P(P, 'site_disney').DSNP
        COUPANG = SupportSC.load_module_P(P, 'site_coupang').COUPANG
        ATVP = SupportSC.load_module_P(P, 'site_appletv').ATVP
        AMZN = SupportSC.load_module_P(P, 'site_prime').AMZN
        EBS = SupportSC.load_module_P(P, 'site_ebs').EBS
        
except Exception as e:
    P.logger.error(f'Exception:{str(e)}')
    P.logger.error(traceback.format_exc()) 
    
class YAMLUTILS(object):

    @classmethod
    def make_yaml(cls, show_data, target_path=None):
            target_path = P.ModelSetting.get('manual_target')
            tmp = re.sub('[\\/:*?\"<>|]', '', show_data['title']).replace('  ', ' ').replace('[]', '').strip()
            with open(os.path.join(target_path, tmp+'.yaml'), 'w', encoding="utf-8") as outfile:
                if P.ModelSetting.get_bool('delete_title'):
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
            'coupang' : r'coupangplay\.com\/titles\/(?P<code>[^/]+)$', 'nf' :r'netflix\.com\/(kr\/title|title)\/(?P<code>[^/]+)$', 'dsnp' : r'disneyplus.com/series/.*?/(?P<code>[^?]+)',
            'atvp' : r'apple.com/.*?(?P<code>umc.cmc.[a-zA-Z0-9]+)$', 'amzn' : r'primevideo\.com/detail/(?P<code>[A-Z0-9]+)'
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

    @classmethod
    def auto_target(cls, path):
        target_list = os.listdir(path)
        for folder in target_list:
            file = cls.get_file(os.path.join(path, folder))
            if file != None and cls.get_release(file) != None:
                release = str(cls.get_release(file))
                match = re.compile(r'^(.+) \((\d{4})\)$')
                if match:
                    title, year = match.match(folder).groups()
                    ottcode = OTTCODE(title.strip(), year.strip())
                    try:
                        cls.make_yaml(cls.get_data(cls.code_sort(release, ottcode.get_ott_code())), P.ModelSetting.get('manual_target'))
                    except:
                        logger.debug('%s 오류', folder)
                        pass


    @classmethod
    def get_file(cls, folder_path):
        if os.path.isdir(folder_path) and not os.path.isfile(os.path.join(folder_path, 'show.yaml')):
            for (path, dir, files) in os.walk(folder_path.strip()): 
                for file in files:
                    if os.path.splitext(file)[1] in ['.mkv', '.mp4', '.avi', '.flv']:
                        return file
                    else:
                        continue
        else:
            return None

    @classmethod
    def get_release(cls, file):
        if '.NF.' in file:
            return 'NF'
        elif '.DSNP.' in file:
            return 'DSNP'
        elif '.ATVP.' in file:
            return 'ATVP'
        else:
            return None
