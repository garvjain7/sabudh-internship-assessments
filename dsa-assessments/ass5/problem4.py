class MinStack:
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append((val, min(val, self.stack[-1][1]) if self.stack else val))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]


ops = input().split()
args = input().split()
s = None
res = []
for op, a in zip(ops, args):
    if op == "MinStack":
        s = MinStack()
        res.append(None)
    elif op == "push":
        s.push(int(a))
        res.append(None)
    elif op == "pop":
        s.pop()
        res.append(None)
    elif op == "top":
        res.append(s.top())
    else:
        res.append(s.getMin())
print(res)