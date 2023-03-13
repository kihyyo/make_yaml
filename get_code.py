import re, difflib, requests, os, traceback
from urllib.parse import unquote, quote
from support_site import SiteUtil
import tmdbsimple as tmdb
from .setup import P
logger = P.logger

try:
    import tmdbsimple as tmdb
except:
    try:
        os.system("pip install tmdbsimple")
        import tmdbsimple as tmdb
    except Exception as e: 
        logger.error(f"Exception:{str(e)}")
        logger.error(traceback.format_exc())
try:
    from justwatch import JustWatch
except:
    try:
        os.system("pip install justwatch")
        from justwatch import JustWatch
    except Exception as e: 
        logger.error(f"Exception:{str(e)}")
        logger.error(traceback.format_exc())

class OTTCODE(object):

    def __init__(self, title, year=False):
        self.title = title
        self.year = year
        self.headers =  {
        'accept': 'application/json; charset=utf-8',
        'content-type': 'application/json; charset=UTF-8',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57',
        'x-bamsdk-platform': 'windows',
        'x-bamsdk-version': '3.10',
        }
        self.match_score = float(P.ModelSetting.get_int('match_score')/100)
        # self.get_ott_code()
        

    def remove_special_char(self, text):
        return re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》：]', '', text)
    
    def similar(self, seq1, seq2):
        return difflib.SequenceMatcher(a=self.remove_special_char(seq1.lower()), b=self.remove_special_char(seq2.lower())).ratio()

    def tmdb_search(self, title):
        tmdb.API_KEY = 'f090bb54758cabf231fb605d3e3e0468'
        year = self.year
        tmdb_search = tmdb.Search().tv(query=title, language='ko', include_adult=True)
        en_tmdb_search = tmdb.Search().tv(query=title, language='en', include_adult=True)
        tmdb_code = ''
        if tmdb_search['results'] != []:
            if not year:
                score_list = []
                for t in tmdb_search['results']:
                    try:
                        score_list.append(max(self.similar(t['name'], title), self.similar(t['original_name'], title), self.similar(en_tmdb_search['results'][tmdb_search['results'].index(t)]['name'], title))) 
                    except:
                        score_list.append(max(self.similar(t['name'], title), self.similar(t['original_name'], title))) 
                if max(score_list) > self.match_score :
                    tmdb_code = tmdb_search['results'][score_list.index(max(score_list))]['id']
                else:
                    logger.debug('TDMB 유효한 매칭 점수 없음')
                    return []
            else:
                for t in tmdb_search['results']:
                    try:
                        tmdb_year = int(t['first_air_date'].split('-')[0])
                    except:
                        tmdb_year = 1900
                    try:
                        if abs(tmdb_year - int(year)) < 2 and (self.similar(t['name'], title) > self.match_score or self.similar(t['original_name'], title) > self.match_score or self.similar(en_tmdb_search['results'][tmdb_search['results'].index(t)]['name'], title) > self.match_score):#abs(int(tmdb_search['results'][score.index(max(score))]['first_air_date'].split('-')[0]) - int(year)) < 2 :
                            tmdb_code = t['id']
                            break
                        else:
                            continue
                    except:
                        if abs(tmdb_year - int(year)) < 2 and (self.similar(t['name'], title) > self.match_score or self.similar(t['original_name'], title) > self.match_score):
                            tmdb_code = t['id']
                            break
                        else:
                            continue
            self.tmdb_code = tmdb_code
            if tmdb_code != '':
                tmdb_info = tmdb.TV(tmdb_code).info(language='ko')
                self.title = tmdb_info['name']
                en_tmdb_info = tmdb.TV(tmdb_code).info(language='en')
                self.en_title = en_tmdb_info['name']
                streaming_site = [tmdb_info['homepage']]
                return streaming_site
            else:
                logger.debug('TMDB 연도와 일치 정보 없음')
                return []
        else:
            self.tmdb_code = ''
            logger.debug('TMDB 시리즈 검색 실패')
        
    def justwatch_search(self):
        year = self.year
        country_list = ['KR', 'AU']
        streaming_site_list = []
        for country in country_list:
            if country == 'KR':
                title = self.title
            else:
                title = self.en_title
            just_watch = JustWatch(country=country)
            results = just_watch.search_for_item(query =f'{title}')
            if results['items'] != []:
                if not year:
                    score_list = []
                    for content in results['items']:
                        if content['object_type'] == 'show':
                            score_list.append(self.similar(title, content['title']))
                        else:
                            score_list.append(float(0))
                    if max(score_list) > self.match_score :
                        try:
                            streaming_site = results['items'][score_list.index(max(score_list))]['offers'][0]['urls']['standard_web']
                            streaming_site = self.justwatchurl(streaming_site)
                            streaming_site_list.append(streaming_site)
                        except:
                            pass
                else:
                    for content in results['items']:
                        if content['object_type'] == 'show' and self.similar(title, content['title']) > self.match_score and abs(int(content['original_release_year']) - int(year)) < 2:
                            try:
                                streaming_site = content['offers'][0]['urls']['standard_web'] 
                                streaming_site = self.justwatchurl(streaming_site)
                                streaming_site_list.append(streaming_site)
                            except:
                                pass
        return list(set(streaming_site_list)) 
    
    def justwatchurl(self, streaming_site):
        if 'disneyplus' in streaming_site:
            streaming_site = unquote(streaming_site[streaming_site.find('?u=') + len('?u=') : streaming_site.find('&sub')])
        elif 'primevideo' in streaming_site:
            headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",}
            response = requests.get(streaming_site, headers=headers, allow_redirects=True)
            streaming_site = unquote(response.url)
        else:
            streaming_site = streaming_site
        return streaming_site
                
    def kino_search(self, title, year=False):
        title = self.title
        url = f'https://api.kinolights.com/v1/search?keyword={quote(title)}'
        res = requests.get(url, headers=self.headers).json()
        year = self.year
        if res['tv_shows'] != []:
            kin_code = ''
            if not year:
                score_list = []
                for t in res['tv_shows']:
                    if SiteUtil.is_include_hangul(title):
                        search_title = t['TitleKr'].split('시즌')[0].split('파트')[0].strip()
                    else:
                        # title = self.title
                        search_title = t['TitleEn'].strip()
                    if len(t['TitleKr'].split('시즌')) != 1 :
                        if t['TitleKr'].split('시즌')[1].strip() == str(1) :
                            score_list.append(self.similar(title, search_title) + float(0.1))
                        else:
                            score_list.append(self.similar(title, search_title))
                    elif len(t['TitleKr'].split('파트')) != 1:
                        if t['TitleKr'].split('파트')[1].strip() == str(1):
                            score_list.append(self.similar(title, search_title) + float(0.1))
                        else:
                            score_list.append(self.similar(title, search_title))
                    else:
                        score_list.append(self.similar(title, search_title))
                if max(score_list) > self.match_score :
                    kin_code = res['tv_shows'][score_list.index(max(score_list))]['Idx']
                else:
                    logger.debug('키노 유효한 매칭 점수 없음')
                    return []
            else:
                for t in res['tv_shows']:
                    search_title = t['TitleKr'].split('시즌')[0].split('파트')[0].strip()
                    if abs(int(t['ProductionYear']) - int(year)) < 2 and self.similar(search_title, title) > self.match_score:
                        kin_code = t['Idx']
                        break
                    else:
                        continue
            if kin_code != '':
                url = f'https://api.kinolights.com/v1/movie/{kin_code}/prices'
                res = requests.get(url, headers=self.headers).json()
                try:
                    streaming_site_list = []
                    for streaming_site in res['data']:
                        streaming_site = unquote(streaming_site['URL']).split('#')[0]
                        streaming_site_list.append(streaming_site)
                    return streaming_site_list
                except:
                    logger.debug('키노 세부 정보 없음')
                    return []
            else:
                logger.debug('키노 연도와 매칭 점수 없음')
                return []
        else:
            logger.debug('키노 시리즈 검색 실패')
            return []

    def get_ott_code(self):
        tmdb_result = self.tmdb_search(self.title)
        logger.debug(self.tmdb_code)
        if self.tmdb_code != '':
            just_result = self.justwatch_search()
            kino_result = self.kino_search(self.title)
            streaming_site_list = list(set(tmdb_result+kino_result+just_result))
            return streaming_site_list
        else:
            return []
