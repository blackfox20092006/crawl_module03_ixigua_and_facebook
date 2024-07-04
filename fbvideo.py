def crawl_fb(id, token):
    videos = []
    #user or pro5
    url = 'https://graph.facebook.com/{}/videos?type=uploaded&access_token={}'.format(str(id), token)
    res = requests.get(url)
    try:
        if res.json()['data'] == []:
            return 'NoData'
        else:
            for i in res.json()['data']:
                title = i["description"]
                time = i["updated_time"]
                try:
                    comments = i["comments"]["data"]  # list
                except:
                    pass
                watch_link = 'https://www.facebook.com/watch/?v=' + i["id"]
                source_link = i["source"]
                nguoi_dang = i["from"]["name"]
                videos.append(
                    {
                        "tieude": title,
                        "nguoidang": nguoi_dang,
                        "thoigian": time,
                        "binhluan": comments,
                        "linkwatch": watch_link,
                        "linktai": source_link
                    }
                )
            return videos
    except:
        return 'Error'
#id page, user thì lên web id.traodoisub.com lấy
#token thì xài view-source:https://www.facebook.com/dialog/oauth?client_id=124024574287414&redirect_uri=https://www.instagram.com/accounts/signup/&&scope=email&response_type=token
#xong sau đó copy phần accesstoken
#data trả về có 3 dạng, 1 là ko có video, 2 là có data, 3 là lỗi do token bị sai....
