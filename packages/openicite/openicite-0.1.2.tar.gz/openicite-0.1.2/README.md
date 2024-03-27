## Home Page
https://github.com/opendoicom/openicite/


## Dependencies
- **requests**



## Useage

**Installation**
```bash
pip install requests openicite
```

**Example**
```python
from openicite import Openicite

icite = Openicite()

# get_icite
pmid = 23333
data = icite.get_icite(pmid)
print(data)
    
# get_icites
pmid_list = [str(pmid) for pmid in range(2024)]  # 示例: 生成一个超过1000个PMID的列表
field_list = ['pmid', 'year', 'title', 'apt', 'relative_citation_ratio', 'cited_by_clin']
data = icite.get_icites(pmid_list=pmid_list, field_list=field_list)
print(data)
```



## Refs
> [iCite | API | NIH Office of Portfolio Analysis](https://icite.od.nih.gov/api)
