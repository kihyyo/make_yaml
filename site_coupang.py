import requests
from .setup import P
logger = P.logger

class COUPANG(object):
            
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer' : '',
        }
    
    @classmethod
    def search_info(cls, code):
        i = 1
        url = f"https://discover.coupangstreaming.com/v1/discover/titles/{code}/episodes?platform=WEBCLIENT&season={str(i)}&sort=true&locale=ko"
        r = requests.get(url, headers=cls.headers)
        if r.status_code != 200 :
            logger.debug('쿠팡플레이 검색 실패')
            return []
        else:
            info_list = []
            while True:
                try:
                    url = f"https://discover.coupangstreaming.com/v1/discover/titles/{code}/episodes?platform=WEBCLIENT&season={str(i)}&sort=true&locale=ko"
                    r = requests.get(url, headers=cls.headers).json()
                    info_list.append(r['data'])
                    i = i + 1
                except:
                    break
        return info_list
    

    @classmethod
    def make_data(cls, code):
        info_list = cls.search_info(code)
        if info_list !=[]:
            season_data = []
            url = f"https://discover.coupangstreaming.com/v1/discover/titles/{code}?platform=WEBCLIENT&locale=ko&filterRestrictedContent=false"
            show_info  = requests.get(url).json()
            title = show_info['data']['title']
            summary = show_info['data']['description']
            for episode_info in info_list:
                episode_data = []
                for ep in episode_info:
                    ep_data = {
                        'index' : ep['episode'],
                        'title' : ep['title'],
                        'summary' : ep['description']
                    }
                    episode_data.append(ep_data)
                season_no = episode_info[0]['season']
                season = {
                    'index' : season_no,
                    'episodes' : episode_data
                }
                season_data.append(season)
                show_data = {
                        'primary' : False,
                        'code' : 'KC'+code,
                        'title' : title,
                        'summary' : summary,
                        'seasons' : season_data
                    }
            return show_data
        else:
            return []
