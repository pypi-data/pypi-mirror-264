import concurrent.futures
from requests import get
import re

def video_id(url: str) -> str:
    try:
        match = re.search(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/([\w./?=#&-]+)', url)
        if not match:
            return None
        video_id = re.search(r'\b\d+\b', match.group())
        if not video_id:
            r = get(match.group())
            video_id = re.search(r'\b\d+\b', r.url)
    except:
        return None
    return video_id.group()

def download(url: str) -> dict:
    try:
        images = []
        video = None
        videoid = None
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7', 'cache-control': 'max-age=0', 'cookie': 'ttwid=1%7CPUR2JQUWUQ0JjwQBbaXSeldwC01-XB4iuy5DieZznlc%7C1710698199%7C6188dff9ea8b7e5dc1f7cf7a174b285444f32cbdb743310e3677312ccce60ca3; dy_swidth=1920; dy_sheight=1080; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; passport_csrf_token=6df80a6d9e909b6ee647666a955aaf1b; passport_csrf_token_default=6df80a6d9e909b6ee647666a955aaf1b; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; bd_ticket_guard_client_web_domain=2; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; strategyABtestKey=%221711035419.604%22; odin_tt=465884467365964b39a624b6047691fad44b6f4ee5481174e083a74269230014f2b645c0c71641d0d925eccdc80a766e21f3d50f9d3df43cbdb7fea83860672f3fea3469dc9c6ceb7df012629e0e7150; vdg_s=1; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; __ac_nonce=065fc782f00497ce78c2e; __ac_signature=_02B4Z6wo00f019e75iwAAIDCSyBV45FdvsPXm-KAAJAbQ5ZSruqE6xHpF8Dh3R4HDQ64e1urJjb4IKJpNHF9hR5YVW4gH5Jlwpij4yvQEOQKnNFHfAU4.VIeEdpjmlzy.ZugQNVWOAW.JxE2f6; csrf_session_id=7bab0dc552a9297d2c51f37e9cbdbc94; download_guide=%222%2F20240321%2F0%22; GlobalGuideTimes=%221711044640%7C1%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSy8vNVFvdjhtWUc5VTloRlhna3hjWjUvR2IyZ1VlOTFsWTVERGI3dWxMdDc5UXZLTmg0MHU2anhLYWNnaHE0UTdHWEVweDh4SnRUNlBWcDZMVWFsaFE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; tt_scid=RPrxa6ngXaIAn-q4uEOot06wRIbVydeeLCz4X1pRb5TxCssCTfCjwrPDP4.Fl0KPbc3d; pwa2=%220%7C0%7C2%7C0%22; IsDouyinActive=false; msToken=BeyaJVEf_47I8JLtPoocZTA_PcOPVHVKtncLk7HiAz1mRZdeCEZMwNYnBdkZKHt9N0VrciwWEVDxZqk8kpDzOtCpr-qBqGH_ZuVGXzGNO8GNdTJ-tfX1nSox1S66; msToken=TkrdJAzCr6r6PDTNaAUbmMsKb-wIjbc-e7oz0yX9uwMl-TC9yn4M6ekdBYzRm8-Pm2IZ4F2SYhm5llS5Ubcjv7ezwlE1-hXH2XhjTyjvArTXRO6lRHNrVZY_TpIS', 'sec-ch-ua': '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'}
        resp = get(f'https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={video_id(url)}', headers=headers)
        data = resp.json().get('aweme_detail')
        videoid = data.get('aweme_id')
        imgs = data.get('images')
        
        if imgs:
            images = [image.get('url_list')[0] for image in imgs]
        else:
            video = data.get('video').get('play_addr').get('url_list')[0]
        
        return {
            'url': re.search(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/([\w./?=#&-]+)', url).group(),
            'videoid': videoid,
            'video': video,
            'images': images
        }
    except:
        return {
            'url': re.search(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/([\w./?=#&-]+)', url).group(),
            'videoid': videoid,
            'video': video,
            'images': images
        }


def download_file(url):
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7', 'cache-control': 'max-age=0', 'cookie': 'ttwid=1%7CPUR2JQUWUQ0JjwQBbaXSeldwC01-XB4iuy5DieZznlc%7C1710698199%7C6188dff9ea8b7e5dc1f7cf7a174b285444f32cbdb743310e3677312ccce60ca3; dy_swidth=1920; dy_sheight=1080; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; passport_csrf_token=6df80a6d9e909b6ee647666a955aaf1b; passport_csrf_token_default=6df80a6d9e909b6ee647666a955aaf1b; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; bd_ticket_guard_client_web_domain=2; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; strategyABtestKey=%221711035419.604%22; odin_tt=465884467365964b39a624b6047691fad44b6f4ee5481174e083a74269230014f2b645c0c71641d0d925eccdc80a766e21f3d50f9d3df43cbdb7fea83860672f3fea3469dc9c6ceb7df012629e0e7150; vdg_s=1; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; __ac_nonce=065fc782f00497ce78c2e; __ac_signature=_02B4Z6wo00f019e75iwAAIDCSyBV45FdvsPXm-KAAJAbQ5ZSruqE6xHpF8Dh3R4HDQ64e1urJjb4IKJpNHF9hR5YVW4gH5Jlwpij4yvQEOQKnNFHfAU4.VIeEdpjmlzy.ZugQNVWOAW.JxE2f6; csrf_session_id=7bab0dc552a9297d2c51f37e9cbdbc94; download_guide=%222%2F20240321%2F0%22; GlobalGuideTimes=%221711044640%7C1%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSy8vNVFvdjhtWUc5VTloRlhna3hjWjUvR2IyZ1VlOTFsWTVERGI3dWxMdDc5UXZLTmg0MHU2anhLYWNnaHE0UTdHWEVweDh4SnRUNlBWcDZMVWFsaFE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; tt_scid=RPrxa6ngXaIAn-q4uEOot06wRIbVydeeLCz4X1pRb5TxCssCTfCjwrPDP4.Fl0KPbc3d; pwa2=%220%7C0%7C2%7C0%22; IsDouyinActive=false; msToken=BeyaJVEf_47I8JLtPoocZTA_PcOPVHVKtncLk7HiAz1mRZdeCEZMwNYnBdkZKHt9N0VrciwWEVDxZqk8kpDzOtCpr-qBqGH_ZuVGXzGNO8GNdTJ-tfX1nSox1S66; msToken=TkrdJAzCr6r6PDTNaAUbmMsKb-wIjbc-e7oz0yX9uwMl-TC9yn4M6ekdBYzRm8-Pm2IZ4F2SYhm5llS5Ubcjv7ezwlE1-hXH2XhjTyjvArTXRO6lRHNrVZY_TpIS', 'sec-ch-ua': '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'}
    response = get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    return None

def save(data: dict, filename=None):
    try:
        if filename is None:
            filename = data.get('videoid')
        video = data.get('video')
        images = data.get('images')
        if video:
            with open(f'{filename}.mp4', 'wb') as f:
                f.write(download_file(video))
        if images:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(download_file, image) for image in images]
                for i, future in enumerate(concurrent.futures.as_completed(futures)):
                    image_data = future.result()
                    if image_data:
                        with open(f'{filename} - {i+1}.png', 'wb') as f:
                            f.write(image_data)
        return True
    except:
        return False