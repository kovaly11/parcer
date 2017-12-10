import urllib.request
import bs4
import re
import sys 

URL = sys.argv[1]
deep=int(sys.argv[2])
all_emails=[]
all_urls=[[URL]]

def start_url(url):
    res=re.match(r'[http://, https://]+[^/]+/', url)
    return res.group(0)

def find_emails(site):
    """
    function find_emails return emails, which we take in site
    site is http.client.HTTPResponse object 
    """
    regex=re.compile(r"[\w,\.,\_,\%,\+,\-]+@[\w,\.]*")
    emails=[]
    for a in site:
        emails.extend(regex.findall(str(a.decode('utf-8'))))
    all_emails.extend(emails)
    return set(emails)

def good_url(a, start_url):
    """
    Delate parameters and ancors in url
    """
    for i in range(len(a)):
        par=a[i].find('?')
        if par!=-1:
             a[i]=a[i][:par]
        anc=a[i].find('#')
        if anc!=-1:
             a[i]=a[i][:anc]
        if a[i]!='' and a[i][0]=='/':
            a[i]=str(start_url)+a[i][1:i]
        #print(a[i])    
    return list(set(a))

def find_url(site, start_url):
    """
    find all new urls on site
    """
    urls=[]
    soup = bs4.BeautifulSoup(site, 'html.parser')
    page_urls=soup.find_all('a', href=True)
    for i in page_urls:
        urls.append(str(i.get("href")))
    return good_url(urls, start_url)


for i in range(1,deep+1):
    all_urls.append([])

for i in range(deep):
    all_urls[i]=list(set(all_urls[i]))
    for j in all_urls[i]:
        try:
            site=urllib.request.urlopen(j)
        except ValueError:
            print(j+ " can not open for search")
            continue
        all_urls[i+1].extend(find_url(site, start_url(j)))
        print('On page '+j+' we find emails: ',find_emails(urllib.request.urlopen(j)))
        #print(all_urls)

print('All emails:', set(all_emails))
