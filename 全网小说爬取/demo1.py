from urllib.request import urlopen
from re import findall
import pymysql


class Sql(object):
    conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='noveltest', charset='utf8')


    def addnovel(self, sort, sortname, name, imgurl, description, status, author):
        cur = self.conn.cursor()
        cur.execute("insert into novel(sort, sortname, name, imgurl, description, status, author) values(%s,'%s','%s','%s','%s','%s')"%(sort, sortname, name, imgurl, description, status, author))  # 执行sql语句
        lastrowid = cur.lastrowid
        cur.close()
        self.conn.commit()
        return lastrowid
    def addchapter(self,novelid,title,content):
        cur = self.conn.cursor()
        cur.execute("insert into chapter(novelid, title, content) values(%s,'%s','%s')"%(novelid, title, content))
        cur.close()
        self.conn.commit()

mysql = Sql()


sort_dict = {
    1: '玄幻魔法',
    2: '武侠修真',
    3: '纯爱耽美',
    4: '都市言情',
    5: '职场校园',
    6: '穿越重生',
    7: '历史军事',
    8: '网游动漫',
    9: '恐怖灵异',
    10: '科幻小说',
    11: '美文名著',
    12: '热门推荐'
}


def getNovel(url):
    html = urlopen(url).read().decode('gbk')
    # 获取书名
    reg = r'<meta property="og:novel:book_name" content="(.*?)"/>'
    bookname = findall(reg, html)[0]
    # 获取描述
    reg = r'<meta property="og:description" content="([\s\S]*?)"/>'
    description = findall(reg, html)[0]
    # 获取图片
    reg = r'<meta property="og:image" content="(.*?)"/'
    image = findall(reg, html)[0]
    # 获取作者
    reg = r'<meta property="og:novel:author" content="(.*?)"/'
    author = findall(reg, html)[0]

    # 获取状态
    reg = r'<meta property="og:novel:status" content="(.*?)"/'
    status = findall(reg, html)[0]

    # 获取章节地址
    reg = r'<a href="(.*?)" class="reader"'
    chapterurl = findall(reg, html)

    print(bookname, image, description, author, status, chapterurl)
    mysql.addnovel(sort_id,sort_name,bookname,image,description,status,author)


def getList(sort_id, sort_name):
    html = urlopen("http://www.quanshuwang.com/list/%s_1.html" % sort_id).read().decode('gbk')
    reg = r'<a target="_blank" href="([\s\S]*?)" class="l mr10">'
    urlList = findall(reg, html)
    for url in urlList:
        getNovel(url)
        break


for sort_id, sort_name in sort_dict.items():
    getList(sort_id, sort_name)
    break
