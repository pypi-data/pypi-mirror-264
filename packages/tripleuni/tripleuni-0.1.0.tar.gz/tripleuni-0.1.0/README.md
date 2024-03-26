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
postList = client.getPostList(page=1)
```

