# srcML_change_word

## 介绍

代码变换

## 基本流程

以 for2while 为例

1.将 for.c 使用 scrML变化为for.xml

2.将for.xml通过规则变换，变化为while.xml

3.将while.xml通过scrML还原为while.c


## 第一阶段

单属性变换：只变换一个文件中的一个属性，for ->while


## 第二阶段

多属性变换：多个属性组合，for->while + 指针->数组
