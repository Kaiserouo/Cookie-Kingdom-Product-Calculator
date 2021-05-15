# Cookie Kingdom Value Calculator

可以根據自己需求計算產品數據的程式。例如：
+ 搜尋一個產品的材料能產出的最佳價值
  + e.g. 咕咕鐘的舊材料配方最佳價值為25888金幣：
    + 直接賣掉：15959金幣。
    + 賣掉8餅乾粉4果醬：23288金幣。
    + 賣掉8餅乾粉8麵包24豆豆：25888金幣。
+ 計算一產品所需基本材料
  + e.g. 別緻的優格花環要`瑞士卷木柴:192 豆豆果凍:30 方糖:0 餅乾粉:64 果凍莓:72 香醇牛奶:0 棉花糖羊毛:0`。非常厲害的配方。
+ 單純輸出排版
  + 因為全部都變成python class的形式，要怎麼輸出隨便你。
  + 因為官方常改數據，這個格式應該算比較好更動的了。配上程式可以把複雜計算自動化。

前兩項的code在`main.py`可以找到，在main區塊改掉就可以在兩模式互換了。範例輸出為`value_table.txt`和`base_ingr.txt`

基本上各種事項都能完成。不過目前是用command line排版就是了。

極大部分資料來源是[薑餅人王國資訊(line)](https://timeline.line.me/user/_dc_QO8G7ggGbjbSHCYc76i_gegvzmatkCww5Ogc?utm_medium=windows&utm_source=desktop&utm_campaign=OA_Profile)和[HoyfSam1](https://forum.gamer.com.tw/C.php?bsn=70199&snA=1367&tnum=6&bPage=2)。處理薑餅人王國資訊(line)的程式在`deprecated/`裡面；驗證跟HoyfSam1的excel的相異處的程式在`check_excel.py`。

## How to Use
直接跑`main.py`：
```
$ python main.py
```
需求python版本 > 3.7。
## How to Change Output

### `products.txt`
裡面寫滿所有產品的時間(秒)、許願樹價值、花費時間/材料等等。

格式固定，基本材料和複合材料語法不同，會忽略開頭為`#`或是空白的行。基本上就照抄其他行的格式即可。

在程式內有`encode()`和`decode()`可以自動把`List[Union[Base, Component]]`跟此格式互換。不過通常只會用到`decode()`把此檔案讀入程式。

### Output
這個程式的主要邏輯就是：
+ 做好所有產品的class：`Base`或`Compound`，分別對應基本材料和複合產品。
+ 建產品的DAG，且每個`Node`裡面都會塞一個`Base`或`Compound`。如果用舊配方的椪糖果醬就是：
![](images/jam.png)
+ 對DAG用topological sort的順序做事。
+ 用存在`Node`的資訊輸出成成果。

所以需要定義兩個函數：`apply_func`和`print_output`。
+ `apply_func(node)`：會根據topological sort的順序呼叫。代表對任一個產品，在他的`Node`被呼叫`apply_func`的時候，可以保證他的每一種材料全部被叫過一次`apply_func`了。每一種產品只會被call一次。
+ `print_output(nodes)`：用`apply_func`存在各`Node`的資訊輸出成成果。

簡單的例子可以參考`main.py`的`calBaseComponent`和`printBaseComponent`。