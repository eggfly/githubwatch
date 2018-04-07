import requests,re,time,ast
from Loger import Loger
loger=Loger()
def GetContent(url):
    headers={'Accept':'text/html','X-Requested-With': 'XMLHttpRequest','X-PJAX': 'true','X-PJAX-Container': '#js-pjax-container','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36','Referer': 'https://github.com/search?utf8=%E2%9C%93&q=language%3Apython+xiaomi.com&type=Code','Accept-Language': 'zh-CN,zh;q=0.9','Cookie': '_ga=GA1.2.1637819931.1523064159; _octo=GH1.1.1623410569.1523064160; user_session=X5ODyZQfPOyCVA94iR38dlOhqHVdHdvz1CeCc78aDSPGNUM7; __Host-user_session_same_site=X5ODyZQfPOyCVA94iR38dlOhqHVdHdvz1CeCc78aDSPGNUM7; logged_in=yes; dotcom_user=testwc; tz=Asia%2FShanghai; _gat=1; _gh_sess=SzIwRXRSdnNmQXJXSlFJUE54ZkUwOEVhNU1jUWI3VUU5THd6WFMybWVZOGpyUlA5dDl1ZzJ2Z21oOHNiWndoaDE3MzVIMS8zOGkvRFNMeGNrcVhoSC9HaFJUUVE0RHFXMnordzVsVnRyamdHa3Q2bVJLQy9NMm1uSHR1eUN6L3MwdmZQV3UrR0FHM1hjRlE4eDhiUXR3PT0tLU5FU2JYT2V6RllnTDQwTnZjaFlZYnc9PQ%3D%3D--9f6769faeedae141bc83440b00a9b29809eb265a'}
    content=requests.get(url,headers=headers,timeout=10).text
    return content

def Get_Project(keyword):
    RepositoriesList = []
    i=1
    while True:
        time.sleep(2)
        print i
        url="https://github.com/search?o=desc&p="+str(i)+"&q="+keyword+"&s=indexed&type=Code"
        content=""
        try:
            content=GetContent(url)
        except:
            continue
        relist=re.findall(r'text-bold\" href=\"/.*\">',content)
        if relist!=[]:
            for line in relist:
                repositoriesurl="https://github.com/"+line[18:len(line)-2]
                if repositoriesurl not in whitelist:
                    RepositoriesList.append(repositoriesurl)
                    whitelist.append(repositoriesurl)
                    loger.LogWrite("WhiteRepositories.txt",repositoriesurl)
            i+=1
        else:
            break
    return RepositoriesList

def Get_Sensitive(url):
    sensitive_word_list=loger.ReadToList("sensitiveword.txt")
    for word in sensitive_word_list:
        serarchurl=url+"/search?utf8=?&q="+word+"&type="
        content=GetContent(serarchurl)
        codelist=re.findall(url.replace("https://github.com","")+".*#L",content)
        if codelist!=[]:
            loger.LogWrite("sensitivegithub.txt",serarchurl)
            return serarchurl

def First_Test(keyword):
    url="https://github.com/search?q="+keyword+"&type=Code"
    content=GetContent(url)
    temp=re.findall(r".*code results",content)
    if temp!=[]:
        keyworddictfile=open("keywordnumkey.txt","r")
        dictcontent=keyworddictfile.readlines()
        keyworddictfile.close()
        print dictcontent
        keyworddict=ast.literal_eval(dictcontent[0])
        if keyword not in keyworddict:
            keyworddict[keyword]=temp[0].strip()
            keyworddictfile = open("keywordnumkey.txt", "w")
            keyworddictfile.writelines(str(keyworddict))
            keyworddictfile.close()
            print "nokey"+keyword
            return True

        if keyworddict[keyword].strip()==temp[0].strip():
            print "false"
            return False
        else:
            keyworddict[keyword]=temp[0].strip()
            keyworddictfile = open("keywordnumkey.txt", "w")
            keyworddictfile.writelines(str(keyworddict))
            keyworddictfile.close()
            print "true"
            return True
    else:
        return False

if __name__=="__main__":
    whitelist=loger.ReadToList("WhiteRepositories.txt")
    keword_list=loger.ReadToList("keyword.txt")
    #test num if old=new not test
    for keyword in keword_list:
        if First_Test(keyword):
            project_list=Get_Project(keyword)
            for project in project_list:
                time.sleep(2)
                try:
                    Get_Sensitive(project)
                except:
                    continue


    #Get_Project('language:python xiaomi.com')


