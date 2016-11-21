# EasySeminar

如何高效听完讲座？

生成可以直接导入Google Calendar、Outlook等日历软件的iCal格式的讲座信息文件，帮助你快速听完8（16）次讲座。

导入结果如下图

![calendar](http://7xkunb.com1.z0.glb.clouddn.com/public/16-11-19/48941389.jpg)

## 使用

直接运行即可。貌似需要python3。

将生成的`test.ics`导入你喜欢的日历应用里去。

也可以用[我的vps上的](http://vps.mickir.me:8000/test.ics)，在日历应用中选择添加来自http的ics文件

## 自服务

如果你想要自己搞一个，或者本大四狗毕业了不能继续提供服务了，可以按以下步骤进行。

* 准备一台能持续运行的Linux电脑。
* 安装crontab。
* `git clone`
* `chmod +x EasySeminar.py`
* 运行一下EasySeminar.py测试一下
* `vi /etc/crontab` 添加配置`0 12 * * * root cd /path/to/EasySeminar/ && ./EasySeminar.py > EasySeminar.log`
* `service cron restart`
* `cd /path/to/EasySeminar/ && (python -m SimpleHTTPServer &)`
* 现在你就可以用`http://youip:8000/test.ics`了

