#script to create a new offline version of geeksforgeeks.org website that can be
#even rendered by a mobile application

from lxml.html import parse , tostring 
from lxml.html.clean import Cleaner,clean_html
import codecs, sys
import os
import shutil


from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('scrapper', 'templates'))
reload(sys)
sys.setdefaultencoding('utf-8')


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        shutil.rmtree(directory)
        try:
            os.makedirs(directory)
        except:
            print "Directory  creation problem , please re-run the script"
            exit()


def writemenu(urls,filename):
    template = env.get_template('menu.html')
    #print content
    import datetime
    date = str(datetime.datetime.now())
    data = template.render(urls=urls,date=date)

    f = open(filename,'w')
    f.write(data)
    f.flush()
    f.close()

def writeindex(articles,filename):
    template = env.get_template('index.html')
    #print content
    data = template.render(articles=articles)
    f = open(filename,'w')
    f.write(data)
    f.flush()
    f.close()



def writepage(content,filename):
    template = env.get_template('page.html')
    #print content
    data = template.render(data=content)
    f = open(filename,'w')
    f.write(data)
    f.flush()
    f.close()

#get contents from a geeksforgeeks forum post
def getcontent(url):
    doc = parse(url).getroot()
    
    data = doc.cssselect('html body div#wrapper div#content div#post.post')[0]
    #removing facebooking and other bookmarking links
    try:
        child = data.cssselect('div#post-content.post-content span.martiniboy_social_list')[0];
        child.drop_tree()
        #removing facebooking comments
        child = data.cssselect('div#post-content.post-content div.yarpp-related')[0]
        child.drop_tree()
        #removing related items
        
        child = data.cssselect('html body div#wrapper div#content div#post.post div.comments-main')[0];
        child.drop_tree()
    except:
        pass
    
    

    
    return tostring(data)

#list of urls to process and directory to save the files to 
urls = [
{"url":"http://www.geeksforgeeks.org/category/articles/page/",'dir':'articles','pages':2,'name':'General Articles'},
{"url":"http://www.geeksforgeeks.org/category/c-programs/page/",'dir':'html','pages':6,'name':'Interview/Misc Questions'},
{"url":"http://www.geeksforgeeks.org/category/gfact/page/",'dir':'gfacts','pages':2,'name':'Gfacts'},
{"url":"http://www.geeksforgeeks.org/category/multiple-choice-question/page/",'dir':'mcq','pages':4,'name':'MCQ'},
{"url":"http://www.geeksforgeeks.org/category/linked-list/page/",'dir':'linkedlist','pages':3,'name':'Linked List'},
{"url":"http://www.geeksforgeeks.org/category/c-puzzles/page/",'dir':'puzzles','pages':5,'name':'C/C++ puzzles'},
{"url":"http://www.geeksforgeeks.org/category/tree/page/",'dir':'trees','pages':3,'name':'Trees'},
{"url":"http://www.geeksforgeeks.org/category/c-arrays/page/",'dir':'arrays','pages':5,'name':'Arrays'},

]
writemenu(urls,"index.html")

for url in urls:
    count = 0
    articles = []
    make_dir(url['dir'])
    print "Currently processing "+url['url']
    for i in range(1,url['pages']):

        pageurl = url['url']+str(i)+'/'
        print "Parsing URLS from "+pageurl
        doc = parse(pageurl).getroot()
        #fetching list of post titles on that page
        for link in doc.cssselect('html body div#wrapper div#content div#post.post div div.post-info div.post-title-info h2.post-title a'):
            try:
            	count = count + 1
                #print '%s: %s' % (link.text_content(), link.get('href'))
                
            except:
                pass
            title = link.text_content()
            filename = str(count)+".html"
            data = getcontent(link.get('href'))
            articles.append({'link':filename,'title':title})
            writepage(clean_html(data),url['dir']+"/"+filename)
            #break
    writeindex(articles,url['dir']+"/home.html")
#print "total is "+str(count)


