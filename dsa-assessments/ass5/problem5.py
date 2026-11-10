from collections import deque


class MyStack:
    def __init__(self):
        self.q1 = deque()
        self.q2 = deque()

    def push(self, x):
        self.q2.append(x)
        while self.q1:
            self.q2.append(self.q1.popleft())
        self.q1, self.q2 = self.q2, self.q1

    def pop(self):
        return self.q1.popleft()

    def top(self):
        return self.q1[0]

    def empty(self):
        return not self.q1


ops = input().split()
args = input().split()
s = None
res = []
for op, a in zip(ops, args):
    if op == "MyStack":
        s = MyStack()
        res.append(None)
    elif op == "push":
        s.push(int(a))
        res.append(None)
    elif op == "pop":
        res.append(s.pop())
    elif op == "top":
        res.append(s.top())
    else:
        res.append(s.empty())
print(res)