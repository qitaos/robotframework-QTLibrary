# -*- coding: cp936 -*-

from datetime import date
import re
import os
import time
import socket
import urlparse
import random
import string
try:
    import subprocess
except ImportError:
    subprocess = None  # subprocess not available on Python/Jython < 2.5

__version__ = '0.1'


class _ElementKeywords():

    def __init__(self):
        self._counter = 0
        pass

    def count(self):
        """<p>中文测试</p>
        """
        self._counter += 1
        return self._counter

    def clear_counter(self):
        """clear counter has only a short documentation"""
        self._counter = 0
    def gen_nums(self,counts):
        """Get random number string.
        Example:
        | @{a}= | gen nums | 4 |
        It will return 4 random number. like '2624','1456'.
        """

        li = string.digits
        s = ''
        for n in range(0,int(counts)) :
            s += li[random.randint(0,len(li)-1)]
        return s
    def gen_chars(self,counts,upper='M'):
        """Get random character string.
        upper=U, will get all upper chars.
        upper=L, will get all lower chars.
        upper=M, will get mixed upper and lower chars.
        Example:
        | @{a}= | gen chars | 4 | U |
        It will return 4 random number. like 'ABCS','FDWW'.
        """
        s = ''
        #print string.ascii_letters
        if upper.upper() == 'U':
            li = string.ascii_uppercase
            lenli = len(li)
            for n in range(0,int(counts)):
                s += li[random.randint(0,lenli-1)]
        elif upper.upper() == 'L':
            li = string.ascii_lowercase
            lenli = len(li)
            for n in range(0,int(counts)):
                s += li[random.randint(0,lenli-1)]
        elif upper.upper() == 'M':
            li = string.ascii_letters
            lenli = len(li)
            for n in range(0,int(counts)):
                s += li[random.randint(0,lenli-1)]
        else :
            pass
        return s
    def gen_birthday(self,maxAge=55,minAge=21,sep=''):
        """Get random birthday.
        Example:
        | @{a}= | gen birthday | 4 | 0 | - |
        It will return random age in 0-4 years old birthday.
        like '20100302','20120123'.
        If sep is not null, such as '-', it will return '2010-03-02'
        """
        now = date.today()
        #print now
        birth = now.year - int(minAge)
        #print birth
        mon      = ['1','2','3','4','5','6','7','8','9','10','11','12']
        mon_days = ['31','28','31','30','31','30','31','31','30','31','30','31']
        s =''
        age = int(maxAge)-int(minAge)
        #print 'age'+str(age)
        y = str(birth - random.randint(1,age))
        #print 'y'+str(y)
        index1 = random.randint(0,11)
        #print 'index1:'+str(index1)
        m = str(mon[index1])
        m = m.zfill(2)
        maxDay = int(mon_days[index1])
        d = str(random.randint(1,maxDay))
        d = d.zfill(2)
        s = y + sep + m + sep + d
        return s
    def gen_idcard(self,idcard='',maxAge=55,minAge=21):
        """Get idcard No.
        Example:
        | @{a}= | gen idcard | 123 |
        It will return random idcard.
        like '111110198101010231','111110198402010231'.
        If the lenth of idcard in (15,17,18),
            it will return 18-idcard No
        Else
            it will return random 18-idcard No (21<age<55)
        """
        idlen=len(idcard)
        ic=str(idcard)
        if idlen==17 :
            pass
        elif idlen==15 :
            ic=ic[0:6]+'19'+ic[6:15]
        elif idlen==18 :
            pass
        else :
            ic=self.gen_nums(6)+self.gen_birthday(int(maxAge),int(minAge),'')+self.gen_nums(3)
            #print ic
        ic = ic[0:17]
        lid = list(ic)
        temp = 0
        for nn in range(2,19):
            #print 'nn:'+str(nn)
            a=int(lid[18-nn])
            w= (2**(nn-1)) % 11
            #print 'w:'+str(w)
            temp+=a*w
            #print temp
        temp = (12-temp % 11) % 11 
        if temp >=0 and temp <=9 :
            ic+=str(temp)
        elif temp ==10 :
            ic+='X'
        return ic

    #定义验证函数
    def verify_idcard(self,idcard):
        """verify 18-idcard.
        Example:
        | @{a}= | verify birthday | 111110198101010231 |
        It will return true or false for the idcard.
        """
        #print idcard
        #权重数组
        iW = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1];
        #身份证号码中可能的字符
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x']
        #使用正则表达式检测
        icre = re.compile('^[1-9][0-9]{16}[x0-9]$', re.IGNORECASE);
        m = icre.match(idcard);
        if m:
            pass; 
        else:
            #不是合法的身份证号码，直接退出
            return unicode('不是合法的身份证号码','gbk');
 
        S = 0;
        for i in range(0,17):
            S += int(idcard[i]) * iW[i];
 
        chk_val = (12 - (S % 11)) % 11;
        return idcard[17].lower() == values[chk_val];

    def _lapd_str(self,strings,lens,char):
        tlen=len(strings)
        s = ''
        if tlen<lens :
            for n in range(1,lens-tlen):
                s+=char
            s+=strings
        else :
            s=strings
        return s

    def _Unicode(self):
        val = random.randint(0x4E00, 0x9FBF)
        return unichr(val)

    def gen_name(self,num=3):
        """gen_name gen chinese name.
        Example:
        | @{a}= | gen name | 3 |
        It will return chinese name.
        """        
        #姓氏列表
        li_name =[u'赵',u'钱',u'孙',u'李',u'周',u'吴',u'郑',u'王',u'冯',u'陈',u'褚',u'蒋',
									u'沈',u'韩',u'杨',u'尤',u'许',u'何',u'吕',u'施',u'张',u'孔',u'曹',u'严',
									u'朱',u'秦',u'华',u'金',u'魏',u'陶',u'姜',u'戚',u'谢',u'邹',u'喻',u'柏',
									u'水',u'窦',u'章',u'云',u'苏',u'潘',u'葛',u'奚',u'范',u'彭',u'郎',u'鲁',
									u'韦',u'昌',u'马',u'苗',u'凤',u'花',u'方',u'俞',u'任',u'袁',u'柳',u'酆',
									u'鲍',u'史',u'唐',u'费',u'廉',u'岑',u'薛',u'雷',u'贺',u'倪',u'汤',u'滕',
									u'殷',u'罗',u'毕',u'郝',u'邬',u'安',u'常',u'乐',u'于',u'时',u'傅',u'皮',
									u'卞',u'齐',u'康',u'伍',u'余',u'元',u'卜',u'顾',u'孟',u'平',u'黄',u'和',
									u'穆',u'萧',u'尹',u'姚',u'邵',u'堪',u'汪',u'祁',u'毛',u'禹',u'狄',u'米',
									u'贝',u'明',u'臧',u'计',u'伏',u'成',u'戴',u'谈',u'宋',u'茅',u'庞',u'熊',
									u'纪',u'舒',u'屈',u'项',u'祝',u'董',u'梁',u'杜',u'阮',u'蓝',u'闵',u'席',
									u'季',u'麻',u'强',u'贾',u'路',u'娄',u'危',u'江',u'童',u'颜',u'郭',u'梅',
									u'盛',u'林',u'刁',u'钟',u'徐',u'邱',u'骆',u'高',u'夏',u'蔡',u'田',u'樊',
									u'胡',u'凌',u'霍',u'虞',u'万',u'支',u'柯',u'咎',u'管',u'卢',u'莫',u'经',
									u'房',u'裘',u'缪',u'干',u'解',u'应',u'宗',u'丁',u'宣',u'贲',u'邓',u'郁',
									u'单',u'杭',u'洪',u'包',u'诸',u'左',u'石',u'崔',u'吉',u'钮',u'龚',u'惠',
									u'程',u'嵇',u'邢',u'滑',u'裴',u'陆',u'荣',u'翁',u'荀',u'羊',u'於',u'甄',
									u'魏',u'家',u'封',u'芮',u'羿',u'储',u'靳',u'汲',u'邴',u'糜',u'松',u'井',
									u'段',u'富',u'巫',u'乌',u'焦',u'巴',u'弓',u'牧',u'隗',u'山',u'谷',u'车',
									u'侯',u'宓',u'蓬',u'全',u'郗',u'班',u'仰',u'秋',u'仲',u'伊',u'宫',u'宁',
									u'仇',u'栾',u'暴',u'甘',u'钭',u'厉',u'戎',u'祖',u'武',u'符',u'刘',u'景',
									u'詹',u'束',u'龙',u'卫',u'叶',u'幸',u'司',u'韶',u'郜',u'黎',u'蓟',u'薄',
									u'印',u'宿',u'白',u'怀',u'蒲',u'台',u'从',u'鄂',u'索',u'咸',u'籍',u'赖',
									u'卓',u'蔺',u'屠',u'蒙',u'池',u'乔',u'阴',u'郁',u'胥',u'能',u'苍',u'双',
									u'闻',u'莘',u'党',u'翟',u'谭',u'贡',u'劳',u'逄',u'姬',u'申',u'扶',u'堵',
									u'冉',u'宰',u'郦',u'雍',u'却',u'璩',u'桑',u'桂',u'濮',u'牛',u'寿',u'通',
									u'边',u'扈',u'燕',u'冀',u'郏',u'浦',u'尚',u'农',u'温',u'别',u'庄',u'晏',
									u'柴',u'瞿',u'阎',u'充',u'慕',u'连',u'茹',u'习',u'宦',u'艾',u'鱼',u'容',
									u'向',u'古',u'易',u'慎',u'戈',u'廖',u'庚',u'终',u'暨',u'居',u'衡',u'步',
									u'都',u'耿',u'满',u'弘',u'匡',u'国',u'文',u'寇',u'广',u'禄',u'阙',u'东',
									u'殴',u'殳',u'沃',u'利',u'蔚',u'越',u'夔',u'隆',u'冷',u'訾',u'辛',u'阚',
									u'师',u'巩',u'厍',u'聂',u'晁',u'勾',u'敖',u'融',u'那',u'简',u'饶',u'空',
									u'曾',u'毋',u'沙',u'乜',u'养',u'鞠',u'须',u'丰',u'巢',u'关',u'蒯',u'相',
									u'查',u'后',u'荆',u'红',u'游',u'竺',u'权',u'逯',u'盖',u'後',u'桓',u'公',
									u'万',u'俟',u'司马',u'上官',u'欧阳',u'夏侯',u'诸葛',u'闻人',u'东方',u'赫连',u'皇甫',u'尉迟',
									u'公羊',u'澹台',u'公',u'冶',u'宗',u'政',u'濮',u'阳',u'淳于',u'单于',u'太叔',u'申',
									u'屠',u'公孙',u'仲孙',u'轩辕',u'令狐',u'钟离',u'宇文',u'长孙',u'慕容',u'鲜于',u'闾丘',u'司徒',
									u'司空',u'亓官',u'司寇',u'仉督',u'子车',u'颛孙',u'端木',u'巫',u'马',u'公西',u'漆雕',u'乐正',
									u'壤驷',u'公良',u'拓夹',u'谷宰',u'父谷',u'粱',u'晋',u'楚',u'闫',u'法',u'汝',
									u'鄢',u'涂',u'钦',u'段',u'干',u'百里',u'东郭',u'南门',u'呼延',u'归海',u'羊舌',u'微生',
									u'岳',u'帅',u'缑亢',u'况',u'后',u'有琴',u'梁',u'丘',u'左丘',u'东门',u'西门',u'商',
									u'牟',u'佘',u'佴伯',u'赏',u'南宫',u'墨哈',u'谯笪',u'年',u'爱',u'阳',u'佟']
        ln = len(li_name)
        last_name= li_name[random.randint(0,ln-1)]
        #print last_name
        first_name =''
        for n in range(0,int(num)-len(last_name)):
            first_name += self._GB2312()
            #print first_name
        return last_name + first_name

    #@随机生成汉字
    def _GB2312(self):
        
        str1 = self._hex()
        #print 'str1:'+str1
        #print str1.decode('hex')
        try :
            str2 =str1.decode('hex').decode('gb2312')
        except UnicodeDecodeError:
            #出现错误的时候重新生成一个汉字
            str1 = self._hex()
            try :
                str2 =str1.decode('hex').decode('gb2312')
                #print '22222' + str2
            except UnicodeDecodeError:
                #万一RP很差还是报错，那就指定一个汉字算了
                str2 = u'安'
        return str2
    
    def _hex(self):
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        if body == 0xF :
            tail = random.randint(0, 0xE)
        else :
            tail = random.randint(0, 0xF)
        val = ( head << 8 ) | (body << 4) | tail
        str1 = "%x" % val
        return str1

if __name__ == "__main__":
    #这是一个测试用的脚本，可以直接运行该文件验证新增的函数
    #u=_ElementKeywords().Unicode()
    #print u
    #x=_ElementKeywords()._GB2312()
    #print x
    for n in range(0,100):
        na=_ElementKeywords().gen_name(4)
        print na
    """a=_ElementKeywords().gen_birthday('23','21','-')
    print 'a:'+a
    b=_ElementKeywords().gen_idcard('')
    print 'b:'+b
    c=_ElementKeywords().verify_idcard(b)
    print 'c:'+str(c)
    d=_ElementKeywords().gen_nums(5)
    print 'd:'+d
    e=_ElementKeywords().gen_chars(6)
    print 'e:'+e"""

