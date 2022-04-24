import json
import os,re,sys
import requests

class LeetCodeAuto():
    """
    普通力扣题目自动化预处理；
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

        # print(self.qTitle) # 138. 复制带随机指针的链表
        # print(self.qMD) # 138-复制带随机指针的链表.md
        # print(self.difficulty) # 中等
        # print(self.qNumber) # 138


    def initMD(self):
        """
        初试化，对应的markdown文件；
        """
        # 判断文件是否已经存在；
        filename = "./docs/notes/" + self.qMD
        if os.path.isfile(filename):
            print(self.qMD + ": 该文件已经存在")
            exit(0)

        with open(filename, 'w') as f:
            str = "# [{}]({})".format(self.qTitle, self.qURL)
            f.write(str)
            print("--- 已创建完成并写入一级标题 docs/notes/{}".format(self.qMD))
    
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
            if "剑指" in sidebarLine: continue # 跳过剑指offer的表格；

            # 匹配到对应行了，进行题号大小比较，小数在前，大数在后；
            # "  - [0001. 两数之和](notes/1-两数之和.md)   " 
            pattern = re.compile(r'  - \[(\d{4}). ')
            
            if len(pattern.findall(sidebarLine)) != 0:
                # 提取文件当中记录的题号； "  - [0001. 两数之和](notes/1-两数之和.md)   "
                curNumber = int(pattern.findall(sidebarLine)[0])
                if self.qNumber < curNumber: 
                    self.index = index
                    break
                elif self.qNumber == curNumber: 
                    print("_sidebar.md: 题号重复，ERROR！")
                    exit()
                else: # 此题号，比当前号大；
                    # 根据下一行情况来确定位置；
                    if "  - [" in sidebarLines[index+1]:
                        nextNumber = int(pattern.findall(sidebarLines[index+1])[0])
                        if curNumber < self.qNumber < nextNumber:
                            self.index = index+1
                            break
                        else: continue
                    else: 
                        self.index = index+1
                        break
        # "  - [0001. 两数之和](notes/1-两数之和.md)   " 
        # 先将题号变为 四位数 
        self.qTitle_CN = self.qTitle.split(' ')[1] # 两数之和
        self.qSeq = '{:0>4}'.format(self.qNumber) # 将123 变为 0123的效果！！！
        insertData = "  - [{}. {}](notes/{})\n".format(self.qSeq,self.qTitle_CN, self.qMD) 
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

            pattern = re.compile(r'\| \[(\d{4}). ')

            # 匹配到对应行了，进行题号大小比较，小数在前，大数在后；
            if len(pattern.findall(jtLine)) != 0:

                # 提取文件当中记录的题号；
                curNumber = int(pattern.findall(jtLine)[0])
                if self.qNumber < curNumber: 
                    self.index = index
                    break
                elif self.qNumber == curNumber: 
                    print("解题目录.md: 题号重复，ERROR！")
                    exit()
                else: # 此题号，比当前号大；
                    # 根据下一行情况来确定位置；
                    if "| [" in jtLines[index+1]:
                        nextNumber = int(pattern.findall(jtLines[index+1])[0])
                        if curNumber < self.qNumber < nextNumber:
                            self.index = index+1
                            break
                        else: continue
                    else: 
                        self.index = index+1
                        break
        #| [0232. 用栈实现队列](notes/232-用栈实现队列)           | Python   | 简单 |
        # 先将题号变为 四位数 
        self.qTitle_CN = self.qTitle.split(' ')[1] # 两数之和
        self.qSeq = '{:0>4}'.format(self.qNumber) # 将123 变为 0123的效果！！！
        insertData = "| [{}. {}](notes/{})| Python   | {} |\n".format(self.qSeq, self.qTitle_CN ,self.qMD, self.difficulty)
        jtLines.insert(self.index, insertData)

        # 修改好的，写入文件；
        with open(解题目录MD, 'w') as fwrite:
            fwrite.writelines(jtLines)
            print("--- 写入解题目录.md已完成；")

# if __name__ == "__main__":
#     # 使用方式：
#     # python lcauto.py https://leetcode-cn.com/problems/bao-han-minhan-shu-de-zhan-lcof/

#     qUrl = sys.argv[1]
#     offerauto = LeetCodeAuto(qUrl)
#     offerauto.getQInfo()
#     offerauto.initMD() 
#     offerauto.modifySidebar()
#     offerauto.modify解题目录()
