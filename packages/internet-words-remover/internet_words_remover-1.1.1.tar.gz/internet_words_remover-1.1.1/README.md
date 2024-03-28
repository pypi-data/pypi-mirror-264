# Internet Words Remover

Internet Words Remover is a Python module that replaces common internet slang and abbreviations with their full forms. It can be used to clean text data containing informal language commonly used in chats, social media, and online communication.

## Installation

You can install Internet Words Remover using pip:

```bash
pip install internet_words_remover
```

## How to Use

```python
from internet_words_remover import words_remover
text="OMG! It works! Osm"
cleaned=words_remover(text)
print(cleaned)
```
**Output**
```
oh my god It works! Awesome
```
### Tokenization
If you are intrested to get tokens of your give string then use follow code.

```python
from internet_words_remover import words_remover
text="OMG! It works! Osm"
cleaned=words_remover(text,is_token=True)
print(cleaned)
```
**Output**
```
['oh', 'my', 'god', 'It', 'works!', 'Awesome']
```

### Bonus
**It also works on pandas series**
```python
from internet_words_remover import words_remover
import pandas as pd 
data={
    'Name':['Qadeer'],
    'Message':['Hi gm TIL something new. PTL']
}
df=pd.DataFrame(data)
df['Message'].apply(words_remover,is_token=True)

```
**Output**
```
['Hi', 'good', 'morning', 'today', 'I', 'learned', 'something', 'new.', 'praise', 'the', 'lord']
```

#### Catch me on
[Github](https://github.com/mrqadeer)
[LinkedIn](https://www.linkedin.com/in/mr-qadeer-3499a4205/)
#### Thanks
##### Keep Learning and Exploring!