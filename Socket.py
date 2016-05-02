#coding=utf-8
#!/usr/bin/python
#to be continued 20160502 
 
import http.client
import urllib.request
from bs4 import BeautifulSoup
import xlwt

class SocketInfo():
    nID=0
    strName=""
    ratioChicang=""
    ratioZhangDie=""
    nFundNo=0
    def _init_(self):
        nFundNo = 0;

listSocket = []
	
def getSocketOfFund(strFundNo):
    
    global listSocket
    #1，获取数据
    strURL = "http://fund.eastmoney.com/";
    strURL = strURL + strFundNo + ".html";
    with urllib.request.urlopen( strURL ) as url:
        data1 = url.read()

    #2，将返回流保存入文件
    #fileOfStream = open('E:/python/HttpFundInfo.html', 'w')
    #print(data1, file = fileOfStream)
    #fileOfStream.write(str(data1))


    #3，提取有用数据,放入数据结构中
    book = xlwt.Workbook(encoding = 'utf-8',style_compression=0)
    sheet = book.add_sheet(strFundNo,cell_overwrite_ok = True)
    sheet.write(0, 0, "序号");
    sheet.write(0, 1, "股票名称");
    sheet.write(0, 2, "持仓占比");
    sheet.write(0, 3, "涨跌幅");
    sheet.write(0, 4, "购买基金只数");
    soup = BeautifulSoup(data1, "html.parser")
    for row in range(2, 12):
        num = soup('div', id = "gzcc0")[0].contents[row].contents[0].string
        name = soup('div', id = "gzcc0")[0].contents[row].contents[1].string
        chic = soup('div', id = "gzcc0")[0].contents[row].contents[2].string
        zhangfu = soup('div', id = "gzcc0")[0].contents[row].contents[3].string
        
        #查找list当中是否已经存在这个socket
        bfind = False;
        for socket in listSocket:
            if name == socket.strName:
                bfind =True
                socket.nFundNo += 1
                print ("found")
                break
        
        if  bfind == False:
            print (name + " is not found")
            newSocket = SocketInfo()
            newSocket.nID = num;
            newSocket.strName = name;
            newSocket.ratioChicang = chic;
            newSocket.ratioZhangDie = zhangfu;
            newSocket.nFundNo = 1;
            listSocket.append(newSocket)           
            print (len(listSocket))
            
    #4，排序放入文件
    listSocket = sorted(listSocket, key=lambda so:so.ratioZhangDie)

    col = 1;
    for socket in listSocket:
        sheet.write(col, 0, socket.nID)
        sheet.write(col, 1, socket.strName)
        sheet.write(col, 2, socket.ratioChicang)
        sheet.write(col, 3, socket.ratioZhangDie)
        sheet.write(col, 4, socket.nFundNo)
        col += 1
        
    book.save(r'E:/python/fundinfo.xls')
    #fileOfStream.close()
    print(strFundNo + " get ready !")

	
getSocketOfFund("000039")


with urllib.request.urlopen("http://fund.eastmoney.com/data/fundranking.html#tall;c0;r;szzf;pn50;ddesc;qsd20140810;qed20150810;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb") as url:
#with urllib.request.urlopen("http://fund.eastmoney.com/data/fundranking.html") as url: 
 data1 = url.read()
fileOfStream = open('E:/python/HttpRankResult.html', 'w')
print(data1, file = fileOfStream)
fileOfStream.write(str(data1))




