# [剑指 Offer 24. 反转链表](https://leetcode-cn.com/problems/fan-zhuan-lian-biao-lcof/)

> **注意**：本题与主站 206 题相同：https://leetcode-cn.com/problems/reverse-linked-list/

## Python头插法反转链表

```Python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if not head or not head.next: # 空链表，或者只有一个节点的链表
            return head
        head2 = ListNode() # 新头结点；
        p = head
        q = p.next
        while p and q:  # q如果为None，则q.next会ERROR；
            p.next = head2.next
            head2.next = p
            p = q
            q=q.next

        p.next = head2.next
        head2.next = p
        
        return head2.next
```

