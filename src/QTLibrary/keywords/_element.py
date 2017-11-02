#encoding=utf-8

import datetime
from datetime import date
import re
import os
#import time
#import socket
#import urlparse
import random
from random import choice
import string
import codecs
from .keywordgroup import KeywordGroup
import sys

class _ElementKeywords(KeywordGroup):

    def __init__(self):
        self._counter = 0
        pass
    # Public, element lookups

    def count(self):
        """for counting. Init countNum is 0.
        When you call this method it will add 1 by itself.
        Example:
        | @{a}= | count |
        """
        self._counter += 1
        self._debug('self._counter += 1')
        return self._counter

    def clear_counter(self):
        """clear counter has only a short documentation
        Example:
        | @{a}= | clear counter |
        """
        self._counter = 0
        self._debug('self._counter = 0')

    def gen_nums(self, counts):
        """Get random number string.
        Example:
        | @{a}= | gen nums | 4 |
        It will return 4 random number. like '2624','1456'.
        """
        s = self._gen_nums(counts)
        self._debug('Get random number string: %s' % s)
        return s

    def gen_chars(self, counts, upper='M'):
        """Get random character string.
        upper=U, will get all upper chars.
        upper=L, will get all lower chars.
        upper=M, will get mixed upper and lower chars.
        Example:
        | @{a}= | gen chars | 4 | U |
        It will return 4 random string. like 'ABCS','FDWW'.
        """
        s = self._gen_chars(counts, upper)
        self._debug('Get random character string: %s' % s)
        return s

    def gen_birthday(self, maxAge=55, minAge=21, sep=''):
        """Get random birthday.
        Example:
        | @{a}= | gen birthday | 4 | 0 | - |
        It will return random age in 0-4 years old birthday.
        like '20100302','20120123'.
        If sep is not null, such as '-', it will return '2010-03-02'
        """
        s = self._gen_birthday(maxAge, minAge, sep)
        self._debug('Get random birthday: %s' % s)
        return s

    def gen_idcard(self, idcard='', maxAge=55, minAge=21):
        """随机生成身份证号.
        Example:
        | @{a}= | gen idcard | 123 |
        关键字返回值是一个随机的身份证号，根据你的输入参数不同，返回结果也略不同.
        例如： '111110198101010231','111110198402010231'.
        如果你给定了一个身份号，并且长度是(15,17,18)位的,
            会返回一个正确格式的18位身份证号（可以用来格式化成正确身份证号）
        否则
            会返回一个随机的18身份证号(21<年龄<55)
        """
        province= {
        '11':'北京市',
        '12':'天津市',
        '13':'河北省',
        '14':'山西省',
        '15':'内蒙古',
        '21':'辽宁省',
        '22':'吉林省',
        '23':'黑龙江省',
        '31':'上海市',
        '32':'江苏省',
        '33':'浙江省',
        '34':'安徽省',
        '35':'福建省',
        '36':'江西省',
        '37':'山东省',
        '41':'河南省',
        '42':'湖北省',
        '43':'湖南省',
        '44':'广东省',
        '45':'广西省',
        '46':'海南省',
        '50':'重庆市',
        '51':'四川省',
        '52':'贵州省',
        '53':'云南省',
        '54':'西藏自治区',
        '61':'陕西省',
        '62':'甘肃省',
        '63':'青海省',
        '64':'宁夏回族自治区',
        '65':'新疆'
        }

        idlen = len(idcard)
        ic = str(idcard)
        if idlen == 17:
            pass
        elif idlen == 15:
            ic = ic[0:6] + '19' + ic[6:15]
        elif idlen == 18:
            pass
        else:
            ic = choice(province.keys()) + self._gen_nums(4) + self._gen_birthday(int(maxAge),
                 int(minAge)) + self._gen_nums(3)
            #print ic
        ic = ic[0:17]
        ic = self._gen_idcard(ic)
        self._debug('Get random idcard No: %s' % ic)
        return ic

    def gen_orgno(self, orgno='', line=None):
        """Get random Org No.
        Example:
        | @{a}= | gen orgno |  | line |
        It will return random orgno. 8 numbers and '-' and 1 verify-number.
        If you don't need '-', send anything but not none for argument line.
        """
        ic = self._gen_orgno(orgno)
        if line:
            ic = ic.replace('-', '')
        self._debug('Get random Org No: %s' % ic)
        return ic

    def gen_name(self, num=3):
        """随机生成中文姓名，参数是字数.
        Example:
        | @{a}= | gen name | 3 |
        It will return chinese name.
        """
        cust_name = self._gen_name()
        if sys.version_info >= (3,3):
            len_name = len(cust_name.decode('utf-8'))
        else:
            len_name = len(cust_name)
        for n in range(0, int(num) - len_name):
            cust_name += self._to_unicode(self._GB2312())
            #print cust_name
        self._info('gen chinese name: %s' % cust_name)
        if sys.version_info >= (3,3):
            cust_name = cust_name.decode('utf-8')
        
        return cust_name

    #定义验证函数
    def verify_idcard(self, idcard):
        """验证身份证号是否正确.
        Example:
        | @{a}= | verify idcard | 111110198101010231 |
        返回值为: true or false , 表示身份证号验证正确与否.
        """
        #print idcard
        #权重数组
        iW = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
        #身份证号码中可能的字符
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x']
        #使用正则表达式检测
        icre = re.compile('^[1-9][0-9]{16}[x0-9]$', re.IGNORECASE)
        m = icre.match(idcard)
        if m:
            pass
        else:
            #不是合法的身份证号码，直接退出
            msg = self._to_unicode('不是合法的身份证号码')
            self._warn(msg + ':' + idcard)
            return msg

        S = 0
        for i in range(0, 17):
            S += int(idcard[i]) * iW[i]

        chk_val = (12 - (S % 11)) % 11
        self._debug('chk_val: %s' % chk_val)
        return idcard[17].lower() == values[chk_val]

    def verify_orgno(self, orgno):
        """verify orgno.
        Example:
        | @{a}= | verify orgno | 111110198101010231 |
        It will return true or false for the idcard.
        """
        #print idcard
        #权重数组
        lens = len(orgno)
        if orgno.find('-') != -1:
            orglen = 10
        else:
            orglen = 9
        if lens != orglen:
            msg = self._to_unicode('不是合法的组织机构代码')
            self._warn(msg + ':' + orgno)
            return msg
        last = orgno[-1]
        self._debug('last: %s' % last)
        iW = [3, 7, 9, 10, 5, 8, 4, 2]
        #身份证号码中可能的字符
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X']
        #使用正则表达式检测
        #icre = re.compile('^[1-9][0-9]{16}[x0-9]$', re.IGNORECASE);
        #m = icre.match(orgno)
        S = 0
        for i in range(0, 8):
            a = orgno[i].upper()
            if ord('A') <= ord(a) and ord('Z') >= ord(a):
                w = (ord(a) - 55) * iW[i]
            else:
                w = int(a) * iW[i]
            self._debug('w: %s' % w)
            S += w
        chk_val = (11 - (S % 11)) % 11
        self._debug('chk_val: %s' % chk_val)
        return last.upper() == values[chk_val]

    def create_pboc(self, new_name, new_id, filepath):
        """Create Pboc
        You can create a normal credit file by using this keyword.
        Example:
        | Create Pboc | Pingan | 252461196308226269 | ${CURDIR} |
        It will create a credit file in the directory and return the file path
        Then you can upload the file.
        Remember that ${CURDIR} is necessary!! :b
        """

        path_sep = os.sep
        credit_file = filepath + path_sep + 'credit.html'
        #print credit_file
        lines = open(credit_file, "rb").readlines()
        tmp = lines[0].strip()
        cust_name = re.compile(
            'id="custName" type="hidden" value="(.*?)"/>').findall(tmp)[0]
        #print cust_name
        tmp = lines[1].strip()
        cust_id = re.compile(
            'id="custId" type="hidden" value="(.*?)"/>').findall(tmp)[0]
        #print cust_id
        tmp = lines[2].strip()
        credit_id = re.compile(
            'id="credit_id" type="hidden" value="(.*?)"/>').findall(tmp)[0]
        #print credit_id
        new_creditid = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        new_creditid += str(datetime.datetime.now().microsecond)
        new_creditid += str(random.randint(10, 99))
        #Get Customer Name And ID in the Credit File
        new_id = new_id.encode("GBK")
        new_name = new_name.encode("GBK")
        #Convert it into GBK code
        streamWriter = codecs.lookup('utf-8')[-1]
        sys.stdout = open(credit_file, "r")
        sys.stdout = streamWriter(sys.stdout)
        content = sys.stdout.read().replace(cust_name, new_name)
        content = content.replace(cust_id, new_id)
        content = content.replace(credit_id, new_creditid)
        f = open(credit_file, 'w')
        f.write(content)
        #Replace the Name and ID
        f.close()
        sys.stdout.close()
        return credit_file

    # Private

    def _to_unicode(self, unicode_or_str):

        if isinstance(unicode_or_str, str):
            try:
                value = unicode_or_str.decode('utf-8')
            except:
                value = unicode_or_str.encode('utf-8')
        elif isinstance(unicode_or_str, bytes):
            value = unicode_or_str.decode('utf-8')
        else:
            value = unicode_or_str

        return value

    def _gen_nums(self, counts):
        li = string.digits
        s = ''
        for n in range(0, int(counts)):
            s += choice(li)
        return s

    def _gen_chars(self, counts, upper='M'):
        s = ''
        li = ''
        #print string.ascii_letters
        if upper.upper() == 'U':
            li = string.ascii_uppercase
            lenli = len(li)
        elif upper.upper() == 'L':
            li = string.ascii_lowercase
            lenli = len(li)
        elif upper.upper() == 'M':
            li = string.ascii_letters
            lenli = len(li)                
        else:
            pass
            self._warn('wrong upper: %s' % upper.upper())
            return
        for n in range(0, int(counts)):
            s += choice(li)
        return s

    def _gen_birthday(self, maxAge=55, minAge=21, sep=''):
        now = date.today()
        #print now
        birth = now.year - int(minAge)
        #print birth
        mon = ['1', '2', '3', '4', '5', '6', '7', '8', '9',
        '10', '11', '12']
        mon_days = ['31', '28', '31', '30', '31', '30', '31', '31',
        '30', '31', '30', '31']
        s = ''
        age = int(maxAge) - int(minAge)
        #print 'age'+str(age)
        y = str(birth - random.randint(1, age))
        #print 'y'+str(y)
        #index1 = random.randint(0, 11)
        #print 'index1:'+str(index1)
        m = choice(mon)
        m = m.zfill(2)
        maxDay = int(mon_days[int(m)-1])
        d = str(random.randint(1, maxDay))
        d = d.zfill(2)
        s = y + sep + m + sep + d
        return s

    def _gen_idcard(self, idcard):
        idlen = len(idcard)
        ic = str(idcard)
        if idlen != 17:
            msg = self._to_unicode('不是合法的身份证号码: ')
            self._warn(msg + idcard)
            return
            #print ic
        lid = list(ic)
        temp = 0
        for nn in range(2, 19):
            #print 'nn:'+str(nn)
            a = int(lid[18 - nn])
            w = (2 ** (nn - 1)) % 11
            #print 'w:'+str(w)
            temp += a * w
            #print temp
        temp = (12 - temp % 11) % 11
        if temp >= 0 and temp <= 9:
            ic += str(temp)
        elif temp == 10:
            ic += 'X'
        return ic

    def _gen_orgno(self, orgno=''):
        #quanzhong
        iW = [3, 7, 9, 10, 5, 8, 4, 2]
        idlen = len(str(orgno))
        ic = str(orgno)
        if idlen == 8:
            pass
        else:
            st = random.randint(0, 8)
            ic = self._gen_chars(st, 'U') + self._gen_nums(8 - st)
            #print ic
        temp = 0
        for nn in range(0, 8):
            #self._debug('nn', nn)
            a = ic[nn].upper()
            #self._debug('a', a)
            #self._debug('iW', iW[nn])
            if ord('A') <= ord(a) and ord('Z') >= ord(a):
                w = (ord(a) - 55) * iW[nn]
            else:
                w = int(a) * iW[nn]
            #self._debug('w', w)
            temp += w
            #self._debug('temp', temp)
        temp = 11 - temp % 11
        if temp >= 0 and temp <= 9:
            ic += '-' + str(temp)
        elif temp == 10:
            ic += '-' + 'X'
        elif temp == 11:
            ic += '-' + '0'
        return ic

    def _lapd_str(self, strings, lens, char):
        tlen = len(strings)
        s = ''
        if tlen < lens:
            for n in range(1, lens - tlen):
                s += char
            s += strings
        else:
            s = strings
        return s

    def _Unicode(self):
        val = random.randint(0x4E00, 0x9FBF)
        return chr(val)

    def _gen_name(self):
        #姓氏列表
        li_name =['赵','钱','孙','李','周','吴','郑','王','冯','陈','褚','蒋',
'沈','韩','杨','尤','许','何','吕','施','张','孔','曹','严',
'朱','秦','华','金','魏','陶','姜','戚','谢','邹','喻','柏',
'水','窦','章','云','苏','潘','葛','奚','范','彭','郎','鲁',
'韦','昌','马','苗','凤','花','方','俞','任','袁','柳','酆',
'鲍','史','唐','费','廉','岑','薛','雷','贺','倪','汤','滕',
'殷','罗','毕','郝','邬','安','常','乐','于','时','傅','皮',
'卞','齐','康','伍','余','元','卜','顾','孟','平','黄','和',
'穆','萧','尹','姚','邵','堪','汪','祁','毛','禹','狄','米',
'贝','明','臧','计','伏','成','戴','谈','宋','茅','庞','熊',
'纪','舒','屈','项','祝','董','梁','杜','阮','蓝','闵','席',
'季','麻','强','贾','路','娄','危','江','童','颜','郭','梅',
'盛','林','刁','钟','徐','邱','骆','高','夏','蔡','田','樊',
'胡','凌','霍','虞','万','支','柯','咎','管','卢','莫','经',
'房','裘','缪','干','解','应','宗','丁','宣','贲','邓','郁',
'单','杭','洪','包','诸','左','石','崔','吉','钮','龚','惠',
'程','嵇','邢','滑','裴','陆','荣','翁','荀','羊','於','甄',
'魏','家','封','芮','羿','储','靳','汲','邴','糜','松','井',
'段','富','巫','乌','焦','巴','弓','牧','隗','山','谷','车',
'侯','宓','蓬','全','郗','班','仰','秋','仲','伊','宫','宁',
'仇','栾','暴','甘','钭','厉','戎','祖','武','符','刘','景',
'詹','束','龙','卫','叶','幸','司','韶','郜','黎','蓟','薄',
'印','宿','白','怀','蒲','台','从','鄂','索','咸','籍','赖',
'卓','蔺','屠','蒙','池','乔','阴','郁','胥','能','苍','双',
'闻','莘','党','翟','谭','贡','劳','逄','姬','申','扶','堵',
'冉','宰','郦','雍','却','璩','桑','桂','濮','牛','寿','通',
'边','扈','燕','冀','郏','浦','尚','农','温','别','庄','晏',
'柴','瞿','阎','充','慕','连','茹','习','宦','艾','鱼','容',
'向','古','易','慎','戈','廖','庚','终','暨','居','衡','步',
'都','耿','满','弘','匡','国','文','寇','广','禄','阙','东',
'殴','殳','沃','利','蔚','越','夔','隆','冷','訾','辛','阚',
'师','巩','厍','聂','晁','勾','敖','融','那','简','饶','空',
'曾','毋','沙','乜','养','鞠','须','丰','巢','关','蒯','相',
'查','后','荆','红','游','竺','权','逯','盖','後','桓','公',
'万','俟','司马','上官','欧阳','夏侯','诸葛','闻人','东方','赫连','皇甫','尉迟',
'公羊','澹台','公','冶','宗','政','濮','阳','淳于','单于','太叔','申',
'屠','公孙','仲孙','轩辕','令狐','钟离','宇文','长孙','慕容','鲜于','闾丘','司徒',
'司空','亓官','司寇','仉督','子车','颛孙','端木','巫','马','公西','漆雕','乐正',
'壤驷','公良','拓夹','谷宰','父谷','粱','晋','楚','闫','法','汝',
'鄢','涂','钦','段','干','百里','东郭','南门','呼延','归海','羊舌','微生',
'岳','帅','缑亢','况','后','有琴','梁','丘','左丘','东门','西门','商',
'牟','佘','佴伯','赏','南宫','墨哈','谯笪','年','爱','阳','佟']
        #ln = len(li_name)
        last_name = choice(li_name)
        self._debug('gen last_name: %s' % last_name)
        return self._to_unicode(last_name)
    
    #@随机生成汉字
    def _GB2312(self):

        str1 = self._hex()
        try:
            str2 = str1.decode('hex').decode('gb18030')
        except UnicodeDecodeError:
            #出现错误的时候重新生成一个汉字
            str2 = self._GB2312()
        except:
            #print (bytes.fromhex(str1).decode('gb18030'))
            str2 = bytes.fromhex(str1).decode('gb18030')
        return str2

    def _hex(self):
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        if body == 0xF:
            tail = random.randint(0, 0xE)
        else:
            tail = random.randint(0, 0xF)
        val = (head << 8) | (body << 4) | tail
        str1 = "%x" % val
        return str1
