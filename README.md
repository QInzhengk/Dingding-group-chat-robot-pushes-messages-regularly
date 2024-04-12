# 钉钉群聊机器人定时推送消息

![GitHub repo size](https://img.shields.io/github/repo-size/QInzhengk/galaxy?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/QInzhengk/galaxy?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/QInzhengk/galaxy?style=for-the-badge)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/QInzhengk/galaxy?style=for-the-badge)
![Bitbucket  issues](https://img.shields.io/github/issues-closed/QInzhengk/galaxy?style=for-the-badge)

## 📒 简介

> :smiley: 通过GitHub Actions给顶顶群聊定时推送消息（Python）。

## 🤝 [博客](https://github.com/qzkq/qzkq.github.io)

[galaxy](https://qzkq.github.io/)

## 实例2、通过GitHub Actions给钉钉群聊机器人定时推送消息（Python）
### 1、钉钉步骤
打开钉钉，点击+发起群聊（如你有公司，需要有两个不是公司的好友才能创建普通群），创建完成后，打开群聊中的设置，智能群助手。
进入到机器人管理页面，点击添加机器人，进入机器人选择页面，这里选择自定义机器人。
![在这里插入图片描述](https://img-blog.csdnimg.cn/16042ba005e94ae480a83dd9c65ea220.png)
需要给机器人修改头像和名称，在安全设置里面，建议最好把自定义关键字也勾选上，比如我这里设置的是：早上好，然后其他的可以默认，点击完成后在新的页面有一个webhook（Webhook不要泄露在网上）
![在这里插入图片描述](https://img-blog.csdnimg.cn/d03d721b6c20482d8b6517af8ec284a3.png)
获取到Webhook地址后，用户可以向这个地址发起HTTP POST 请求，即可实现给该钉钉群发送消息。

钉钉群聊机器人最新规定：

> 发起POST请求时，必须将字符集编码设置成UTF-8。
> 每个机器人每分钟最多发送20条。消息发送太频繁会严重影响群成员的使用体验，大量发消息的场景 (譬如系统监控报警)可以将这些信息进行整合，通过markdown消息以摘要的形式发送到群里。

目前支持发送的消息有5种，分别是：文本 (text)、链接 (link)、markdown、ActionCard、FeedCard。个人使用中比较常用的有两种：分别是文本和链接，企业使用的时候，对于ActionCard类型的也比较常用。

具体需要根据自己的场景进行选择，以便能达到最好的展示样式。

自定义机器人发送消息时，可以通过手机号码指定“被@人列表”。在“被@人列表”里面的人员收到该消息时，会有@消息提醒。免打扰会话仍然通知提醒，首屏出现“有人@你”

#### 文本TEXT

文本型的消息类型，具体代码如下：

```
{
    "at": {
        "atMobiles":[
            "180xxxxxx"
        ],
        "atUserIds":[
            "user123"
        ],
        "isAtAll": false
    },
    "text": {
        "content":"测试"
    },
    "msgtype":"text"
}

```

上述中涉及的参数类型分别如下：

| **参数**  | **参数类型** | **是否必填** | **说明**                                                     |
| --------- | ------------ | ------------ | ------------------------------------------------------------ |
| msgtype   | String       | 是           | 消息类型，此时固定为：text。                                 |
| content   | String       | 是           | 消息内容。                                                   |
| atMobiles | Array        | 否           | 被@人的手机号。**注意** 在content里添加@人的手机号，且只有在群内的成员才可被@，非群内成员手机号会被脱敏。 |
| atUserIds | Array        | 否           | 被@人的用户userid。**注意** 在content里添加@人的userid。     |
| isAtAll   | Boolean      | 否           | 是否@所有人。                                                |

#### 链接LINK

链接型的消息类型，具体代码如下：

```
{
    "msgtype": "link", 
    "link": {
        "text": "测试", 
        "title": "测试", 
        "picUrl": "", 
        "messageUrl": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI"
    }
}
```

上述中涉及的参数类型分别如下：

| **参数**   | **参数类型** | 是否必填 | **说明**                                                     |
| ---------- | ------------ | -------- | ------------------------------------------------------------ |
| msgtype    | String       | 是       | 消息类型，此时固定为：link。                                 |
| title      | String       | 是       | 消息标题。                                                   |
| text       | String       | 是       | 消息内容。如果太长只会部分展示。                             |
| messageUrl | String       | 是       | 点击消息跳转的URL，打开方式如下：移动端，在钉钉客户端内打开PC端默认侧边栏打开希望在外部浏览器打开，请参考[消息链接说明](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az) |
| picUrl     | String       | 否       | 图片URL。                                                    |

#### markdown类型

markdown的消息类型，具体代码如下：

```json
{
     "msgtype": "markdown",
     "markdown": {
         "title":"测试",
         "text": "#### 杭州天气 @150XXXXXXXX \n > 9度，西北风1级，空气良89，相对温度73%\n > ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n > ###### 10点20分发布 [天气](https://www.dingtalk.com) \n"
     },
      "at": {
          "atMobiles": [
              "188XXXXXXXX"
          ],
          "atUserIds": [
              "user123"
          ],
          "isAtAll": false
      }
 }
```

上述中涉及的参数类型分别如下：

| **参数**  | **类型** | 是否必填 | **说明**                                                     |
| --------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype   | String   | 是       | 消息类型，此时固定为：markdown。                             |
| title     | String   | 是       | 首屏会话透出的展示内容。                                     |
| text      | String   | 是       | markdown格式的消息。                                         |
| atMobiles | Array    | 否       | 被@人的手机号。**注意** 在text内容里要有@人的手机号，只有在群内的成员才可被@，非群内成员手机号会被脱敏。 |
| atUserIds | Array    | 否       | 被@人的用户userid。**注意** 在content里添加@人的userid。     |
| isAtAll   | Boolean  | 否       | 是否@所有人。                                                |



#### 整体跳转ActionCard类型

整体跳转ActionCard的消息类型，具体代码如下：

```
{
    "actionCard": {
        "title": "测试", 
        "text": "测试", 
        "btnOrientation": "0", 
        "singleTitle" : "测试",
        "singleURL" : "https://www.dingtalk.com/"
    }, 
    "msgtype": "actionCard"
}
```

上述中涉及的参数类型分别如下：

| **参数**       | **类型** | **是否必填** | **说明**                                                     |
| -------------- | -------- | ------------ | ------------------------------------------------------------ |
| msgtype        | String   | 是           | 消息类型，此时固定为：actionCard。                           |
| title          | String   | 是           | 首屏会话透出的展示内容。                                     |
| text           | String   | 是           | markdown格式的消息。                                         |
| singleTitle    | String   | 是           | 单个按钮的标题。**注意** 设置此项和singleURL后，btns无效。   |
| singleURL      | String   | 是           | 点击消息跳转的URL，打开方式如下：移动端，在钉钉客户端内打开PC端默认侧边栏打开希望在外部浏览器打开，请参考[消息链接说明](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az) |
| btnOrientation | String   | 否           | 0：按钮竖直排列1：按钮横向排列                               |


#### 独立跳转ActionCard类型

独立跳转ActionCard的消息类型，具体代码如下：

```
{
    "msgtype": "actionCard",
    "actionCard": {
        "title": "测试", 
        "text": "测试", 
        "btnOrientation": "0", 
        "btns": [
            {
                "title": "内容不错", 
                "actionURL": "https://www.dingtalk.com/"
            }, 
            {
                "title": "不感兴趣", 
                "actionURL": "https://www.dingtalk.com/"
            }
        ]
    }
}
```

上述中涉及的参数类型分别如下：

| **参数**       | **类型** | 是否必填 | 说明                                                         |
| -------------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype        | String   | 是       | 此消息类型为固定actionCard。                                 |
| title          | String   | 是       | 首屏会话透出的展示内容。                                     |
| text           | String   | 是       | markdown格式的消息。                                         |
| btns           | Array    | 是       | 按钮。                                                       |
| title          | String   | 是       | 按钮标题。                                                   |
| actionURL      | String   | 是       | 点击按钮触发的URL，打开方式如下：移动端，在钉钉客户端内打开PC端默认侧边栏打开希望在外部浏览器打开，请参考[消息链接说明](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az) |
| btnOrientation | String   | 否       | 0：按钮竖直排列1：按钮横向排列                               |

#### FeedCard类型

FeedCard的消息类型，具体代码如下：

```
{
    "msgtype":"feedCard",
    "feedCard": {
        "links": [
            {
                "title": "测试1", 
                "messageURL": "https://www.dingtalk.com/", 
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            },
            {
                "title": "测试2", 
                "messageURL": "https://www.dingtalk.com/", 
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            }
        ]
    }
}
```

上述中涉及的参数类型分别如下：

| **参数**   | **类型** | 是否必填 | **说明**                                                     |
| ---------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype    | String   | 是       | 此消息类型为固定feedCard。                                   |
| title      | String   | 是       | 单条信息文本。                                               |
| messageURL | String   | 是       | 点击单条信息到跳转链接。**说明** PC端跳转目标页面的方式，参考[消息链接在PC端侧边栏或者外部浏览器打开](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az)。 |
| picURL     | String   | 是       | 单条信息后面图片的URL。                                      |


### 2、Github步骤
这里和第一个实例类似，不再重复介绍。
代码地址：[https://github.com/QInzhengk/galaxy](https://github.com/QInzhengk/galaxy)
![在这里插入图片描述](https://img-blog.csdnimg.cn/1d1ac2ec331a46d08c4473e152101732.png)
## ☕  鸣谢

感谢以下参考的帮助：

- [https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html](https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)
- [https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions](https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions)
- [https://github.com/datawhalechi](https://github.com/datawhalechi)
- [https://blog.csdn.net/qq_45832050/article/details/126789897](https://blog.csdn.net/qq_45832050/article/details/126789897)
- [https://blog.csdn.net/qq_45832050/article/details/122755904](https://blog.csdn.net/qq_45832050/article/details/122755904)
- [后续更新完将会完善这一部分，有问题可以点击Issues提问；均为互联网资料，侵权删]()
