에러를 알려주는걸 뭔말인지 못알아듯네 
Dojo한테 간다 안녕


Heedongui-MacBookPro:gurukorea yanggeek$ python3 dartapi.py
Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/pandas/core/indexes/base.py", line 2657, in get_loc
    return self._engine.get_loc(key)
  File "pandas/_libs/index.pyx", line 108, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index.pyx", line 132, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/hashtable_class_helper.pxi", line 1601, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas/_libs/hashtable_class_helper.pxi", line 1608, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: '28기분기_3개월'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "dartapi.py", line 54, in <module>
    sheet.loc[sheet["temp"]=="(","28기분기_3개월"]=sheet["28기분기_3개월"].str.replace("(","-")
  File "/usr/local/lib/python3.7/site-packages/pandas/core/frame.py", line 2927, in __getitem__
    indexer = self.columns.get_loc(key)
  File "/usr/local/lib/python3.7/site-packages/pandas/core/indexes/base.py", line 2659, in get_loc
    return self._engine.get_loc(self._maybe_cast_indexer(key))
  File "pandas/_libs/index.pyx", line 108, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index.pyx", line 132, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/hashtable_class_helper.pxi", line 1601, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas/_libs/hashtable_class_helper.pxi", line 1608, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: '28기분기_3개월'
Heedongui-MacBookPro:gurukorea yanggeek$ 
