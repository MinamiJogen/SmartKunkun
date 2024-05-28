# 简介

此项目旨在创建一个基于微信的机器人，通过调用gpt接口快速且智能的回复问题。

目前支持功能如下：

- [x] **多端部署：** 有多种部署方式可选择且功能完备，目前已支持个人微信，微信公众号和企业微信应用等部署方式
- [x] **基础对话：** 私聊及群聊的消息智能回复，支持多轮会话上下文记忆，支持 GPT-3.5, GPT-4, claude, 文心一言, 讯飞星火
- [x] **语音识别：** 可识别语音消息，通过文字或语音回复，支持 azure, baidu, google, openai(whisper/tts) 等多种语音模型
- [x] **图片生成：** 支持图片生成 和 图生图（如照片修复），可选择 Dall-E, stable diffusion, replicate, midjourney模型
- [x] **丰富插件：** 支持个性化插件扩展，已实现多角色切换、文字冒险、敏感词过滤、聊天记录总结、文档总结和对话等插件
- [X] **Tool工具：** 与操作系统和互联网交互，支持最新信息搜索、数学计算、天气和资讯查询、网页总结，基于 [chatgpt-tool-hub](https://github.com/goldfishh/chatgpt-tool-hub) 实现
- [x] **知识库：** 通过上传知识库文件自定义专属机器人，可作为数字分身、领域知识库、智能客服使用，基于 [LinkAI](https://link-ai.tech/console) 实现

# 快速开始

## 准备

### 1. 账号注册（使用GPT官方接口，目前不使用）

项目默认使用OpenAI接口，需前往 [OpenAI注册页面](https://beta.openai.com/signup) 创建账号，创建完账号则前往 [API管理页面](https://beta.openai.com/account/api-keys) 创建一个 API Key 并保存下来，后面需要在项目中配置这个key。接口需要海外网络访问及绑定信用卡支付。

> 默认对话模型是 openai 的 gpt-3.5-turbo，计费方式是约每 1000tokens (约750个英文单词 或 500汉字，包含请求和回复) 消耗 $0.002，图片生成是Dell E模型，每张消耗 $0.016。

项目同时也支持使用其他接口，可使用 文心、讯飞、GPT-3、GPT-4 等模型，支持 定制化知识库、联网搜索、MJ绘图、文档总结和对话等能力。修改配置即可一键切换，参考 [接入文档](https://link-ai.tech/platform/link-app/wechat)。

### 1. 账号注册（使用LinkAI）

前往[LinkAI官网](https://link-ai.tech/portal)微信扫码登录。

在[控制台](https://link-ai.tech/console/interface)中选择应用接入，创建并保存API。

在[控制台](https://link-ai.tech/console/knowledgeBase)中选择知识库，在此创建/管理知识库。

在[控制台](https://link-ai.tech/console/factory)中选择应用，创建一个知识库应用，保存应用代码。

### 2.运行环境

支持 Linux、MacOS、Windows 系统（可在Linux服务器上长期运行)，同时需安装 `Python`。
> 建议Python版本在 3.7.1~3.9.X 之间，推荐3.8版本，3.10及以上版本在 MacOS 可用，其他系统上不确定能否正常运行。

**(1) 克隆项目代码：**

```bash
git clone https://github.com/MinamiJogen/SmartKunkun.git
cd chatgpt-on-wechat/
```

**(2) 安装核心依赖 (必选)：**
> 能够使用`itchat`创建机器人，并具有文字交流功能所需的最小依赖集合。
```bash
pip3 install -r requirements.txt
```

## 配置

配置文件的模板在根目录的`config-template.json`中，需复制该模板创建最终生效的 `config.json` 文件：

```bash
  cp config-template.json config.json
```

然后在`config.json`中填入配置，以下是对默认配置的说明，可根据需要进行自定义修改（请去掉注释）：

```bash
# config.json文件内容示例
{
  "open_ai_api_key": "YOUR API KEY",                          # 填入上面创建的 OpenAI API KEY，若使用LinkAI则不需要填写
  "model": "gpt-3.5-turbo",                                   # 模型名称, 支持 gpt-3.5-turbo, gpt-3.5-turbo-16k, gpt-4, wenxin, xunfei
  "proxy": "",                                                # 代理客户端的ip和端口，国内环境开启代理的需要填写该项，如 "127.0.0.1:7890"
  "single_chat_prefix": ["bot", "@bot"],                      # 私聊时文本需要包含该前缀才能触发机器人回复
  "single_chat_reply_prefix": "[bot] ",                       # 私聊时自动回复的前缀，用于区分真人
  "group_chat_prefix": ["@bot"],                              # 群聊时包含该前缀则会触发机器人回复
  "group_name_white_list": ["ChatGPT测试群", "ChatGPT测试群2"], # 开启自动回复的群名称列表
  "group_chat_in_one_session": ["ChatGPT测试群"],              # 支持会话上下文共享的群名称  
  "image_create_prefix": ["画", "看", "找"],                   # 开启图片回复的前缀
  "conversation_max_tokens": 1000,                            # 支持上下文记忆的最多字符数
  "speech_recognition": false,                                # 是否开启语音识别
  "group_speech_recognition": false,                          # 是否开启群组语音识别
  "use_azure_chatgpt": false,                                 # 是否使用Azure ChatGPT service代替openai ChatGPT service. 当设置为true时需要设置 open_ai_api_base，如 https://xxx.openai.azure.com/
  "azure_deployment_id": "",                                  # 采用Azure ChatGPT时，模型部署名称
  "azure_api_version": "",                                    # 采用Azure ChatGPT时，API版本
  "character_desc": "你是ChatGPT, 一个由OpenAI训练的大型语言模型, 你旨在回答并解决人们的任何问题，并且可以使用多种语言与人交流。",  # 人格描述
  # 订阅消息，公众号和企业微信channel中请填写，当被订阅时会自动回复，可使用特殊占位符。目前支持的占位符有{trigger_prefix}，在程序中它会自动替换成bot的触发词。
  "subscribe_msg": "感谢您的关注！\n这里是ChatGPT，可以自由对话。\n支持语音对话。\n支持图片输出，画字开头的消息将按要求创作图片。\n支持角色扮演和文字冒险等丰富插件。\n输入{trigger_prefix}#help 查看详细指令。",
  "use_linkai": false,                                        # 是否使用LinkAI接口，默认关闭，开启后可国内访问，使用知识库和Midjourney
  "linkai_api_key": "",                                       # LinkAI Api Key
  "linkai_app_code": ""                                       # LinkAI 应用code
}
```

## LinkAI说明

基于 LinkAI 提供的知识库、Midjourney绘画、文档对话等能力对机器人的功能进行增强。平台地址: https://link-ai.tech/console

## LinkAI配置

将 `plugins/linkai` 目录下的 `config.json.template` 配置模板复制为最终生效的 `config.json`。 (如果未配置则会默认使用`config.json.template`模板中配置，但功能默认关闭，需要可通过指令进行开启)。

以下是插件配置项说明：

```bash
{
    "group_app_map": {               # 群聊 和 应用编码 的映射关系
        "测试群名称1": "default",      # 表示在名称为 "测试群名称1" 的群聊中将使用app_code 为 default 的应用
        "测试群名称2": "Kv2fXJcH"
    },
    "midjourney": {
        "enabled": true,          # midjourney 绘画开关
        "auto_translate": true,   # 是否自动将提示词翻译为英文
        "img_proxy": true,        # 是否对生成的图片使用代理，如果你是国外服务器，将这一项设置为false会获得更快的生成速度
        "max_tasks": 3,           # 支持同时提交的总任务个数
        "max_tasks_per_user": 1,  # 支持单个用户同时提交的任务个数
        "use_image_create_prefix": true   # 是否使用全局的绘画触发词，如果开启将同时支持由`config.json`中的 image_create_prefix 配置触发
    },
    "summary": {
        "enabled": true,              # 文档总结和对话功能开关
        "group_enabled": true,        # 是否支持群聊开启
        "max_file_size": 5000,        # 文件的大小限制，单位KB，默认为5M，超过该大小直接忽略
        "type": ["FILE", "SHARING", "IMAGE"]  # 支持总结的类型，分别表示 文件、分享链接、图片
    }
}
```

根目录 `config.json` 中配置，`API_KEY` 在 [控制台](https://link-ai.tech/console/interface) 中创建并复制过来:

```bash
"linkai_api_key": "Link_xxxxxxxxx"
```

注意：

 - 配置项中 `group_app_map` 部分是用于映射群聊与LinkAI平台上的应用， `midjourney` 部分是 mj 画图的配置，`summary` 部分是文档总结及对话功能的配置。三部分的配置相互独立，可按需开启
 - 实际 `config.json` 配置中应保证json格式，不应携带 '#' 及后面的注释

## LinkAI插件使用

> 使用插件中的知识库管理功能需要首先开启`linkai`对话，依赖全局 `config.json` 中的 `use_linkai` 和 `linkai_api_key` 配置；而midjourney绘画 和 summary文档总结对话功能则只需填写 `linkai_api_key` 配置，`use_linkai` 无论是否关闭均可使用。具体可参考 [详细文档](https://link-ai.tech/platform/link-app/wechat)。

完成配置后运行项目，会自动运行插件，输入 `#help linkai` 可查看插件功能。

### 1.知识库管理功能

提供在不同群聊使用不同应用的功能。可以在上述 `group_app_map` 配置中固定映射关系，也可以通过指令在群中快速完成切换。

应用切换指令需要首先完成管理员 (`godcmd`) 插件的认证，然后按以下格式输入：

`$linkai app {app_code}`

例如输入 `$linkai app Kv2fXJcH`，即将当前群聊与 app_code为 Kv2fXJcH 的应用绑定。

另外，还可以通过 `$linkai close` 来一键关闭linkai对话，此时就会使用默认的openai接口；同理，发送 `$linkai open` 可以再次开启。

### 2.Midjourney绘画功能

若未配置 `plugins/linkai/config.json`，默认会关闭画图功能，直接使用 `$mj open` 可基于默认配置直接使用mj画图。

指令格式：

```
 - 图片生成: $mj 描述词1, 描述词2..
 - 图片放大: $mju 图片ID 图片序号
 - 图片变换: $mjv 图片ID 图片序号
 - 重置: $mjr 图片ID
```

例如：

```
"$mj a little cat, white --ar 9:16"
"$mju 1105592717188272288 2"
"$mjv 11055927171882 2"
"$mjr 11055927171882"
```

注意事项：
1. 使用 `$mj open` 和 `$mj close` 指令可以快速打开和关闭绘图功能
2. 海外环境部署请将 `img_proxy` 设置为 `false`
3. 开启 `use_image_create_prefix` 配置后可直接复用全局画图触发词，以"画"开头便可以生成图片。
4. 提示词内容中包含敏感词或者参数格式错误可能导致绘画失败，生成失败不消耗积分
5. 若未收到图片可能有两种可能，一种是收到了图片但微信发送失败，可以在后台日志查看有没有获取到图片url，一般原因是受到了wx限制，可以稍后重试或更换账号尝试；另一种情况是图片提示词存在疑似违规，mj不会直接提示错误但会在画图后删掉原图导致程序无法获取，这种情况不消耗积分。

### 3.文档总结对话功能

#### 配置

该功能依赖 LinkAI的知识库及对话功能，需要在项目根目录的config.json中设置 `linkai_api_key`， 同时根据上述插件配置说明，在插件config.json添加 `summary` 部分的配置，设置 `enabled` 为 true。

如果不想创建 `plugins/linkai/config.json` 配置，可以直接通过 `$linkai sum open` 指令开启该功能。

#### 使用

功能开启后，向机器人发送 **文件**、 **分享链接卡片**、**图片** 即可生成摘要，进一步可以与文件或链接的内容进行多轮对话。如果需要关闭某种类型的内容总结，设置 `summary`配置中的type字段即可。

#### 限制

 1. 文件目前 支持 `txt`, `docx`, `pdf`, `md`, `csv`格式，文件大小由 `max_file_size` 限制，最大不超过15M，文件字数最多可支持百万字的文件。但不建议上传字数过多的文件，一是token消耗过大，二是摘要很难覆盖到全部内容，只能通过多轮对话来了解细节。
 2. 分享链接 目前仅支持 公众号文章，后续会支持更多文章类型及视频链接等
 3. 总结及对话的 费用与 LinkAI 3.5-4K 模型的计费方式相同，按文档内容的tokens进行计算

## 其他配置说明：

**1.个人聊天**

+ 个人聊天中，需要以 "bot"或"@bot" 为开头的内容触发机器人，对应配置项 `single_chat_prefix` (如果不需要以前缀触发可以填写  `"single_chat_prefix": [""]`)
+ 机器人回复的内容会以 "[bot] " 作为前缀， 以区分真人，对应的配置项为 `single_chat_reply_prefix` (如果不需要前缀可以填写 `"single_chat_reply_prefix": ""`)
+ 可以在正式答案回复前/后添加自动回复，在 `channel/wechat/wechat_channel.py` 中搜索“自动回复”来修改对应代码

**2.群组聊天**

+ 群组聊天中，群名称需配置在 `group_name_white_list ` 中才能开启群聊自动回复。如果想对所有群聊生效，可以直接填写 `"group_name_white_list": ["ALL_GROUP"]`
+ 默认只要被人 @ 就会触发机器人自动回复；另外群聊天中只要检测到以 "@bot" 开头的内容，同样会自动回复（方便自己触发），这对应配置项 `group_chat_prefix`
+ 可选配置: `group_name_keyword_white_list`配置项支持模糊匹配群名称，`group_chat_keyword`配置项则支持模糊匹配群消息内容，用法与上述两个配置项相同。（Contributed by [evolay](https://github.com/evolay))
+ `group_chat_in_one_session`：使群聊共享一个会话上下文，配置 `["ALL_GROUP"]` 则作用于所有群聊

**3.语音识别**

+ 添加 `"speech_recognition": true` 将开启语音识别，默认使用openai的whisper模型识别为文字，同时以文字回复，该参数仅支持私聊 (注意由于语音消息无法匹配前缀，一旦开启将对所有语音自动回复，支持语音触发画图)；
+ 添加 `"group_speech_recognition": true` 将开启群组语音识别，默认使用openai的whisper模型识别为文字，同时以文字回复，参数仅支持群聊 (会匹配group_chat_prefix和group_chat_keyword, 支持语音触发画图)；
+ 添加 `"voice_reply_voice": true` 将开启语音回复语音（同时作用于私聊和群聊），但是需要配置对应语音合成平台的key，由于itchat协议的限制，只能发送语音mp3文件，若使用wechaty则回复的是微信语音。

**4.其他配置**

+ `model`: 模型名称，目前支持 `gpt-3.5-turbo`, `text-davinci-003`, `gpt-4`, `gpt-4-32k`, `wenxin` , `claude` ,  `xunfei`(其中gpt-4 api暂未完全开放，申请通过后可使用)
+ `temperature`,`frequency_penalty`,`presence_penalty`: Chat API接口参数，详情参考[OpenAI官方文档。](https://platform.openai.com/docs/api-reference/chat)
+ `proxy`：由于目前 `openai` 接口国内无法访问，需配置代理客户端的地址，详情参考  [#351](https://github.com/zhayujie/chatgpt-on-wechat/issues/351)
+ 对于图像生成，在满足个人或群组触发条件外，还需要额外的关键词前缀来触发，对应配置 `image_create_prefix `
+ 关于OpenAI对话及图片接口的参数配置（内容自由度、回复字数限制、图片大小等），可以参考 [对话接口](https://beta.openai.com/docs/api-reference/completions) 和 [图像接口](https://beta.openai.com/docs/api-reference/completions)  文档，在[`config.py`](https://github.com/zhayujie/chatgpt-on-wechat/blob/master/config.py)中检查哪些参数在本项目中是可配置的。
+ `conversation_max_tokens`：表示能够记忆的上下文最大字数（一问一答为一组对话，如果累积的对话字数超出限制，就会优先移除最早的一组对话）
+ `rate_limit_chatgpt`，`rate_limit_dalle`：每分钟最高问答速率、画图速率，超速后排队按序处理。
+ `clear_memory_commands`: 对话内指令，主动清空前文记忆，字符串数组可自定义指令别名。
+ `hot_reload`: 程序退出后，暂存微信扫码状态，默认关闭。
+ `character_desc` 配置中保存着你对机器人说的一段话，他会记住这段话并作为他的设定，你可以为他定制任何人格      (关于会话上下文的更多内容参考该 [issue](https://github.com/zhayujie/chatgpt-on-wechat/issues/43))
+ `subscribe_msg`：订阅消息，公众号和企业微信channel中请填写，当被订阅时会自动回复， 可使用特殊占位符。目前支持的占位符有{trigger_prefix}，在程序中它会自动替换成bot的触发词。

## 运行

### 1.本地运行

如果是开发机 **本地运行**，直接在项目根目录下执行：

```bash
python3 app.py                                    # windows环境下该命令通常为 python app.py
```

终端输出二维码后，使用微信进行扫码，当输出 "Start auto replying" 时表示自动回复程序已经成功运行了（注意：用于登录的微信需要在支付处已完成实名认证）。扫码登录后你的账号就成为机器人了，可以在微信手机端通过配置的关键词触发自动回复 (任意好友发送消息给你，或是自己发消息给好友)

### 2.服务器部署

使用nohup命令在后台运行程序：

```bash
touch nohup.out                                   # 首次运行需要新建日志文件  
nohup python3 app.py & tail -f nohup.out          # 在后台运行程序并通过日志输出二维码
```
扫码登录后程序即可运行于服务器后台，此时可通过 `ctrl+c` 关闭日志，不会影响后台程序的运行。使用 `ps -ef | grep app.py | grep -v grep` 命令可查看运行于后台的进程，如果想要重新启动程序可以先 `kill` 掉对应的进程。日志关闭后如果想要再次打开只需输入 `tail -f nohup.out`。此外，`scripts` 目录下有一键运行、关闭程序的脚本供使用。

> **多账号支持：** 将项目复制多份，分别启动程序，用不同账号扫码登录即可实现同时运行。

> **特殊指令：** 用户向机器人发送 **#reset** 即可清空该用户的上下文记忆。

注意，在服务器长期运行时请保持手机端微信在线，建议在打开微信后再锁屏手机，以避免服务器微信掉线。
