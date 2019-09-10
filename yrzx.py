import requests
import os
import time
import re
import threading
from bs4 import BeautifulSoup

def download_page(url):
    headers = {'referer':'https://www.36mh.com/manhua/yirenzhixia/',"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    return r.text

def get_list(html,n):
    soup=BeautifulSoup(html,'html.parser')
    chapter_list=soup.find('ul',id='chapter-list-4').find_all('li')
    for i in chapter_list[n:]:
        index=chapter_list.index(i)
        a_tag=i.find('a')
        link='https://www.36mh.com'+a_tag.get('href')
        textall=a_tag.get_text()
        reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
        texta=re.sub(reg,'',textall)
        text=str(index)+'_'+texta
        get_pic(link,text)

def get_pic(link,text):
    html=download_page(link)
    soup=BeautifulSoup(html,'html.parser')
    ts=soup.select("body  script")
    t_list=re.findall('chapterImages = \[(.*)\]',str(ts))[0]
    pic_list=t_list.split(',')
    t_path='https://img001.yayxcc.com/'+re.findall('var chapterPath = "(.*)";var chapterPrice',str(ts))[0]
    for i in range(len(pic_list)):
        pic_i=t_path+pic_list[i].strip('"')
        print(pic_i)
        headers = {'referer':'https://www.36mh.com/manhua/yirenzhixia/',"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
        r=requests.get(pic_i,headers=headers)
        create_dir('pic/{}'.format(text))
        with open('pic/{}/{}_{}.png'.format(text,text,i+1),'wb') as f:
            f.write(r.content)
            time.sleep(1)            
    
def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

def execute(url,n):
    page_html = download_page(url)
    get_list(page_html,n)
    
def main(): 
    create_dir('pic')
    url='https://www.36mh.com/manhua/yirenzhixia/'
    count=0
    for fn in os.listdir('pic'):
        count+=1
    execute(url,count)
    print ('DONE')

if __name__ == '__main__':
    main()

