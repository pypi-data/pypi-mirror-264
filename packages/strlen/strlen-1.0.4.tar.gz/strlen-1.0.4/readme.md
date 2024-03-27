---
# This module allows you to compare strings not by ord() values of chars, but by the length of the string - len()
---
## You need to:
1. Install module with `pip install strlen`
2. Write `import strlen` or `from strlen import MyString`
3. Create your string this way:
    * `name = strlen.MyString("text")` 
    * `name = MyString("text")`
---
## Now you can compare these strings, for example: 
```
import strlen

first = strlen.MyString("text")
second = strlen.MyString("very long text")

print(first > second) # False
print(first < second) # True
print(first == second) # False
```