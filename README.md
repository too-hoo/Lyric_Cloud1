# 数据可视化：给毛不易的云歌词做云词展示

**遇到的情况：**

- 1、网易云音乐也有反爬虫的措施，使用的歌单的链接不能是：https://music.163.com/#/playlist?id=753776811，中间有个#号隔开，其实是其在页面嵌入了一个iframe框架，我们会抓取不到任何的内容，使用的链接应该是https://music.163.com/playlist?id=753776811，同时页面中的Xpath提取元素的时候尽量使用id来定位，因为页面的id是不能重复的，只要页面存在对应的id，就一定能够抓取到对应的内容
- 2、在审查元素的时候需要在Network里面审查，寻找对应的列表，这里如果在Element里面审查的话，会抓取不到对应的内容，其使用了iframe框架动态加载的，或者加入我想要抓取歌曲的名称，网易云好像是会债中间插入一个随机的一段中文例如：
`“像我这”<div class="soil">亶靜耋</div>“样的人”`，很难处理。

## 给毛不易的歌词制作词云总结

1、词云的可视化中，前期的数据准备在整个过程中占了很大的一部分。可以使用Python作为数据采集工具和Python爬虫和Xpath解析。

2、WordCloud词云是一个很好的Python工具，可以将复杂的文本通过云词的方式呈现。需要注意的是当需要使用中文字体的时候，比如黑体SimHei，就可以将WordCloud中的font_path属性设置为SimHei.ttf,也可以使用其他的字体做云词展示，例如使用艺术字体wc.ttf。

3、Python词云
- 词云
    - 概念：词云也叫做文字云，它帮助我们对文本中的出现的高频的词进行统计，过滤掉低频的常用的词，将文本中的重要的关键词进行可视化呈现
    - 工具：wordcloud
        - 构造函数WordCloud()
            - background_color:设置背景颜色，默认是white
            - mask：设置背景图片
            - font_path:设置字体，中文的情况需要设置中文的字体，否则显示乱码
            - max_words:设置最大的字数
            - stopwords：设置停用词
            - max_font_size:设置字体的最大值
            - width：设置画布的宽度
            - height：设置画布的高度
            - random_state:设置多少种随机的状态，即多少种颜色
        - 功能函数
            - generate(text):生成词云，传入的参数text代表你要分析的文本。
- 毛不易词云展示
    - 项目流程
        - 准备阶段：Python爬虫，获取每一首歌的歌词，所有的歌词文本
        - 词云分析：创建词云模型，通过歌词生成词云，词云可视化
    - Python爬虫：获取HTML，使用requests.request时候，需要设置headers
    - Xpath解析：获取歌曲连接，歌曲名称
    - 停用词设置：去掉歌曲中的常用词。

![](wordcloud.jpg)