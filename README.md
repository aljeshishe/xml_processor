### Description
    Application does following:
    1. creates 50 zip archives with 100 xml files each
    2. Processes all archives and creates 2 reports

### How to run
```
    pip install -r requirements.txt
    pytest 
    python main.py
```

### What could be done better 
    1. Write unittest
    2. In case xml files are larger it makes sence
        to avoid loading whole xml structure to memory 
        to avoid using xpath
