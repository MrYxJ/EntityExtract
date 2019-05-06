# EntityExtract

-  'OpenLaw判决书.xlsx' 数据读入在 ```self.all_items```，是一个由```Dict```组成的```List```,```xlsx```第一列属性就是```Dict```键值。
-  ```__init__(self)```函数里```self.analys_pos()```定义了每部分抽取在```xlsx```哪一列。
-  需要编写各个部分抽取函数，每部分然后可以用```test_task```单独进行输出测试，例如```extract_ajxz()``` 。
-  最后调用```test_total()```，数据保存格式和之前做的抽取一样。
