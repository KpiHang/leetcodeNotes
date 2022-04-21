import json
import os,re,sys
import requests

# 不足：正则，文件操作；

# 剑指Offer预处理自动化类；
class JZOfferAuto:
    """
    JZOffer Auto: 剑指(JZ)Offer预处理自动化;
    """
    def __init__(self, qURL) -> None:
        self.qURL = qURL
        self.qTitle = '' # 问题题目：剑指 Offer 30. 包含min函数的栈
        self.qMD = '' # 该问题的md文件名：剑指Offer30-包含min函数的栈.md
        self.difficulty = ''
        self.qNumber = 0
        # 待插入行的下标
        self.index = -1

    # 应用爬虫，获取此题名称，难度等信息；
    def getQInfo(self):
        """
        QInfo: Question Infor, 问题信息；
        """
        header = {
                "accept-language": "zh-CN",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44",
                "x-definition-name": "question",
                "x-operation-name": "questionData",
                "x-timezone": "Asia/Shanghai",
            }

        # 提取"bao-han-minhan-shu-de-zhan-lcof"，防止URL最后少一个"/";
        if "-" in self.qURL.split("/")[-1]:
            variables = {"titleSlug": self.qURL.split("/")[-1]}
        else:
            variables = {"titleSlug": self.qURL.split("/")[-2]}
        # Leetcode-CN采用的GraphQL查询方式；
        query = "query questionData($titleSlug: String) {\n  question(titleSlug: $titleSlug) {\n    questionFrontendId\n    translatedTitle\n    difficulty\n  }\n}\n"
        response = requests.post(url="https://leetcode-cn.com/graphql/", json={'query': query, 'variables': variables}, headers=header)
        # response.json() {'data': {'question': {'questionFrontendId': '剑指 Offer 30', 'translatedTitle': '包含min函数的栈', 'difficulty': 'Easy'}}}

        info = response.json()["data"]["question"]
        # 剑指 Offer 30. 包含min函数的栈
        self.qTitle = info.get('questionFrontendId') + ". " + info.get('translatedTitle') 
        questionFrontendId = info.get('questionFrontendId')
        self.qMD = ''.join(questionFrontendId.split(" ")) + "-" + info.get('translatedTitle') + ".md"

        # Easy: 简单；Medium: 中等；Hard: 困难
        difficulty = info.get('difficulty')
        diffiDict = {"Easy": "简单", "Medium": "中等", "Hard": "困难"}
        self.difficulty = diffiDict.get(difficulty)  # 简单

        # 题号整型提取； 剑指 Offer 30
        self.qNumber = int(questionFrontendId.split(" ")[-1])

        # print(self.qTitle) # 剑指 Offer 30. 包含min函数的栈
        # print(self.qMD) # 剑指Offer30-包含min函数的栈.md
        # print(self.difficulty) # 简单
        # print(self.qNumber) # 30


    def initMD(self):
        """
        初试化，对应的markdown文件；
        """
        # 判断文件是否已经存在；
        filename = "./docs/notes/剑指Offer/" + self.qMD
        if os.path.isfile(filename):
            print(self.qMD + ": 该文件已经存在")
            exit(0)

        with open(filename, 'w') as f:
            str = "# [{}]({})".format(self.qTitle, self.qURL)
            f.write(str)
            print("--- 已创建完成并写入一级标题 docs/notes/剑指Offer/{}".format(filename))
    
    def modifySidebar(self):
        """
        修改_sidebar.md，现将该文件按行以列表的形式读到内存中，在内存中添加对应行，在写到改文件中；
        """
        sidebarMD = "./docs/_sidebar.md"
        with open(sidebarMD, 'r') as f:
            sidebarLines = f.readlines()
        
        # 待插入行的下标
        self.index = -1
        for index,sidebarLine in enumerate(sidebarLines):
            # 匹配到对应行了，进行题号大小比较，小数在前，大数在后；
            if sidebarLine.startswith("  - [剑指 Offer "):
                # 提取文件当中记录的题号；
                curNumber = int(re.findall(r'\d+', sidebarLine)[0])
                if self.qNumber < curNumber: 
                    self.index = index
                    break
                elif self.qNumber == curNumber: 
                    print("_sidebar.md: 题号重复，ERROR！")
                    exit()
                else: # 此题号，比当前号大；
                    # 根据下一行情况来确定位置；
                    if sidebarLines[index+1].startswith("  - [剑指 Offer "):
                        nextNumber = int(re.findall(r'\d+', sidebarLines[index+1])[0])
                        if curNumber < self.qNumber < nextNumber:
                            self.index = index+1
                            break
                        else: continue
                    else: 
                        self.index = index+1
                        break
        #   - [剑指 Offer 09. 用两个栈实现队列](notes/剑指Offer/剑指Offer09-用两个栈实现队列.md)
        insertData = "  - [{}](notes/剑指Offer/{})\n".format(self.qTitle, self.qMD)
        sidebarLines.insert(self.index, insertData)

        # 修改好的，写入文件；
        with open(sidebarMD, 'w') as fwrite:
            fwrite.writelines(sidebarLines)
            print("--- 写入_sidebar.md已完成；")

    def modify解题目录(self):
        """
        修改解题目录.md，现将该文件按行以列表的形式读到内存中，在内存中添加对应行，在写到改文件中；
        """
        解题目录MD = "./docs/解题目录.md"
        with open(解题目录MD, 'r') as f:
            jtLines = f.readlines()
        
        # 待插入行的下标
        self.index = -1
        for index,jtLine in enumerate(jtLines):
            # 匹配到对应行了，进行题号大小比较，小数在前，大数在后；
            if jtLine.startswith("| [剑指 Offer "):
                # 提取文件当中记录的题号；
                curNumber = int(re.findall(r'\d+', jtLine)[0])
                if self.qNumber < curNumber: 
                    self.index = index
                    break
                elif self.qNumber == curNumber: 
                    print("解题目录.md: 题号重复，ERROR！")
                    exit()
                else: # 此题号，比当前号大；
                    # 根据下一行情况来确定位置；
                    if jtLines[index+1].startswith("| [剑指 Offer "):
                        nextNumber = int(re.findall(r'\d+', jtLines[index+1])[0])
                        if curNumber < self.qNumber < nextNumber:
                            self.index = index+1
                            break
                        else: continue
                    else: 
                        self.index = index+1
                        break
        #| [剑指 Offer 09. 用两个栈实现队列](notes/剑指Offer/剑指Offer09-用两个栈实现队列.md)| Python   | 简单 |
        insertData = "| [{}](notes/剑指Offer/{})| Python   | {} |\n".format(self.qTitle, self.qMD, self.difficulty)
        jtLines.insert(self.index, insertData)

        # 修改好的，写入文件；
        with open(解题目录MD, 'w') as fwrite:
            fwrite.writelines(jtLines)
            print("--- 写入解题目录.md已完成；")

if __name__ == "__main__":
    # 使用方式：
    # python offerauto.py https://leetcode-cn.com/problems/bao-han-minhan-shu-de-zhan-lcof/
    qUrl = sys.argv[1]
    offerauto = JZOfferAuto(qUrl)
    offerauto.getQInfo()
    offerauto.initMD() 
    offerauto.modifySidebar()
    offerauto.modify解题目录()