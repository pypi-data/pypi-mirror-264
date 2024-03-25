# Beautider

Module for creating progress bars.

## Examples

### Example in Lib

You can see an example of how to use the library using this code: 

```
from beautider import *

load = Loader().example()
```

You should see the following:

![img](https://github.com/bolgaro4ka/beautider/blob/b4603c18ed53a1edd0a5b09893928e52d46c2bc9/img/img.png?raw=true)

### Another example

```
import time
from beautider import *

load = Loader(description='I load nothing')

while True:
    for _ in range(1, 101):
        load.update(1)
        time.sleep(0.1)
        load.pr_load()
    for _ in range(1, 101):
        load.update(-1)
        time.sleep(0.1)
        load.pr_load()
```
![img](https://github.com/bolgaro4ka/beautider/blob/b4603c18ed53a1edd0a5b09893928e52d46c2bc9/img/img_1.png?raw=true)
![img](https://github.com/bolgaro4ka/beautider/blob/b4603c18ed53a1edd0a5b09893928e52d46c2bc9/img/img_2.png?raw=true)
## Args

 - size - The larger this value, the smaller the bar progress. (if your max_value very large, then the size value should be set larger.)
 - colors - Use of colours (True/False)
 - description - Description next to progress bar
 - complete_symbol - Symbols that are responsible for the filled part of the progress bar
 - uncomplete_symbol - Symbols that are responsible for the unfilled part of the progress bar
 - borders - Borders of progress bar (for example: ```'[]'```, ```'{}'```, ```'--'```, ```'[}'```)
 - units - Units of measurement (default %)
 - max_value - Progress bar ends here
 - min_value - Progress bar started from here
 - show_of - Shows text "```x``` in ```max_value``` ```units```"
 - show_speed - Shows speed

## Developer
By bolgaro4ka. [Link](https://github.com/bolgaro4ka)