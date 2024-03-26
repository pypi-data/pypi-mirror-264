# tripleuni
A python library for tripleuni.
## Installation
```bash
pip install tripleuni
```

## Usage
### Login
you need to login to use the library
#### login in terminal
```python
from tripleuni import TripleClient
client = TripleClient()
client.sendVerification("your email address")
client.verifyCode("your verification code")
```
#### login by token
```python
from tripleuni import TripleClient
client = TripleClient("your token")
```

### Some examples
```python
# get post list
postList = client.getPostList(page=1)

# comment a post
client.commentMsg(1234, "hello", real_name='false')

# send chat message to post owner
client.sendChatMsgToPost(1234, "hello", real_name='false')
```

## For Maintainers

### Build
```bash
py -m pip install --upgrade build
py -m build
```

```bash
py -m pip install --upgrade twine
twine upload dist/*
```

