import requests,re,time,ast
from Loger import Loger
loger=Loger()
def GetContent(url):
    headers={'Accept':'text/html','X-Requested-With': 'XMLHttpRequest','X-PJAX': 'true','X-PJAX-Container': '#js-pjax-container','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36','Referer': 'https://github.com/search?utf8=%E2%9C%93&q=language%3Apython+xiaomi.com&type=Code','Accept-Language': 'zh-CN,zh;q=0.9','Cookie': '_ga=GA1.2.1637819931.1523064159; _octo=GH1.1.1623410569.1523064160; user_session=X5ODyZQfPOyCVA94iR38dlOhqHVdHdvz1CeCc78aDSPGNUM7; __Host-user_session_same_site=X5ODyZQfPOyCVA94iR38dlOhqHVdHdvz1CeCc78aDSPGNUM7; logged_in=yes; dotcom_user=testwc; tz=Asia%2FShanghai; _gat=1; _gh_sess=SzIwRXRSdnNmQXJXSlFJUE54ZkUwOEVhNU1jUWI3VUU5THd6WFMybWVZOGpyUlA5dDl1ZzJ2Z21oOHNiWndoaDE3MzVIMS8zOGkvRFNMeGNrcVhoSC9HaFJUUVE0RHFXMnordzVsVnRyamdHa3Q2bVJLQy9NMm1uSHR1eUN6L3MwdmZQV3UrR0FHM1hjRlE4eDhiUXR3PT0tLU5FU2JYT2V6RllnTDQwTnZjaFlZYnc9PQ%3D%3D--9f6769faeedae141bc83440b00a9b29809eb265a'}
    content=requests.get(url,headers=headers,timeout=30).text
    return content

def First_Test(keyword):
    url="https://github.com/search?o=desc&q="+keyword+"&s=indexed&type=Code"
    content=GetContent(url)
    temp=re.findall(".*code results",content)
    if temp!=[]:
        keyworddictfile=open("keywordnumkey.txt","r")
        dictcontent=keyworddictfile.readlines()
        keyworddictfile.close()
        keyworddict=ast.literal_eval(dictcontent[0])
        if keyword not in keyworddict:
            keyworddict[keyword]=temp[0].strip()
            keyworddictfile = open("keywordnumkey.txt", "w")
            keyworddictfile.writelines(str(keyworddict))
            keyworddictfile.close()
            print keyword
            print url
            return True
        if keyworddict[keyword].strip()==temp[0].strip():
            return False
        else:
            print "old keyword:"+keyword+"num:"+keyworddict[keyword]
            print "old keyword:" + keyword + "num:" + temp[0].strip()
            keyworddict[keyword]=temp[0].strip()
            keyworddictfile = open("keywordnumkey.txt", "w")
            keyworddictfile.writelines(str(keyworddict))
            keyworddictfile.close()
            print url
            return True
    else:
        return False

if __name__=="__main__":
    whitelist=loger.ReadToList("WhiteRepositories.txt")
    keword_list=loger.ReadToList("keyword.txt")
    #test num if old=new not test
    for keyword in keword_list:
        try:
            print keyword
            print First_Test(keyword)
        except:
            continue



