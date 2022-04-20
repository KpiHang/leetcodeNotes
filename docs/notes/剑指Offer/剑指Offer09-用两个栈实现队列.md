# [剑指 Offer 09. 用两个栈实现队列](https://leetcode-cn.com/problems/yong-liang-ge-zhan-shi-xian-dui-lie-lcof/)



## Python用两个栈实现队列

实现方式解析：[《剑指Offer》09-用两个栈实现队列 - 分享技术成长历程～ - 博客园 (cnblogs.com)](https://www.cnblogs.com/kphang/p/15828445.html)

### LeetCode 232题

```python
class CQueue:

    def __init__(self):
        self.inList = list()
        self.outList = list()

    def appendTail(self, value: int) -> None:
        self.inList.append(value)

    def deleteHead(self) -> int:
        # python 中取非是not
        if not self.outList and not self.inList: return -1 # 输入栈空，输出栈也空
        if not self.outList and self.inList: # 输出栈空，输入栈不空；
            # 使用reversed() 函数，reversed函数会生成一份倒序列表的拷贝，但是不会改变原列表
            for i in reversed(self.inList): # 
                self.inList.pop() # 输入栈 弹出向输出栈，输入栈的不能保留呀!
                self.outList.append(i)

        if self.outList: return self.outList.pop()


# Your CQueue object will be instantiated and called as such:
# obj = CQueue()
# obj.appendTail(value)
# param_2 = obj.deleteHead()
```

下面这种方法更好一些！

```python
 def deleteHead(self) -> int:
        # python 中取非是not
        if not self.outList and not self.inList: return -1 # 输入栈空，输出栈也空
        if not self.outList and self.inList: # 输出栈空，输入栈不空；
            while self.inList: self.outList.append(self.inList.pop())

        if self.outList: return self.outList.pop()
```



### 剑指Offer 09题

就在上面的基础上，加了判空empty()，以及查看队头元素peek()；

```python
class MyQueue:

    def __init__(self):
        self.inList = list()
        self.outList = list()

    def push(self, x: int) -> None:
        self.inList.append(x)

    def pop(self) -> int:
        # python 中取非是not
        if not self.outList and not self.inList: return -1 # 输入栈空，输出栈也空
        if not self.outList and self.inList: # 输出栈空，输入栈不空；
            # 使用reversed() 函数，reversed函数会生成一份倒序列表的拷贝，但是不会改变原列表
            for i in reversed(self.inList): # 
                self.inList.pop() # 输入栈 弹出向输出栈，输入栈的不能保留呀!
                self.outList.append(i)

        if self.outList: return self.outList.pop()

    def peek(self) -> int:
        # python 中取非是not
        if not self.outList and not self.inList: return -1 # 输入栈空，输出栈也空
        if not self.outList and self.inList: # 输出栈空，输入栈不空；
            # 使用reversed() 函数，reversed函数会生成一份倒序列表的拷贝，但是不会改变原列表
            for i in reversed(self.inList): # 
                self.inList.pop() # 输入栈 弹出向输出栈，输入栈的不能保留呀!
                self.outList.append(i)

        if self.outList: return self.outList[-1]

    def empty(self) -> bool:
        if not self.outList and not self.inList: return True
        else: return False


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()
```

