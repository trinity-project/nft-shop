# 游戏、商城交互接口细节文档 v1.1

### 摘要
商城会给每款游戏分配一对 appid、appsecret 用于接口请求header校验和参数签名   
目前游戏不用主动申请appid 和 appsecret 商城会自动创建并线下告知   
`同时商城会为游戏创建一个npc 用户 用于请求创建道具和铸币`
`args 中需要额外添加 tsId 参数 用于标识游戏请求操作的 事务id`  

    测试服务器地址：http://47.75.105.222/  
    格式如下(测试服务器数据):       
    appid:      wob071913289742227  
    appsecret:  $2b$10$1ZbzRhmxxPZAtwzb/2zFc..lvkByyQiJFrxITmaV0tRQXAHuWSoN2 
    userid:     6425605781151809538 

**api header 校验**

每个接口请求头需要加入自定义头部 App-Id 值为 上面的 appid:

    headers["App-Id"] = appid

**api 参数签名步骤**  
`参数排序的步骤省略 所有业务参数以json字符串的形式填充到 args 中`  
1.将所有**业务请求参数**按**首字母**先后顺序排序 __升序__：   
以下示例均以某个特定接口**nftGetNew**为参考

    所有必须参数：
    {
        "userId": "user id",
        "id": "asset id",
        "desc": "about desc",
        "sign": "this is argumetns sign"
    }

*由于sign本身不属于业务参数, 仅仅作为最终签名结果比对, 所以它不参与签名*

    排序前参数(剔除非业务参数)：  
    {
        "userId": "user id",
        "id": "asset id",
        "desc": "about desc",
    }
    排序后参数：  
    {
        "desc": "about desc",
        "id": "asset id",
        "userId": "user id"
    }

2.参数名称和参数值链接成一个字符串A

    字符串A结果为： "desc=about descid=asset iduserId=user id"

3.在字符串A的首尾加上appsecret组成一个新字符串B  

    字符串B结果为：
    "$2b$10$uXc9GXGdOCxRf5PUvQ867efsSDWRytM0.2q5C4mJKvAPeJybyZbdGdesc=about descid=asset iduserId=user id$2b$10$uXc9GXGdOCxRf5PUvQ867efsSDWRytM0.2q5C4mJKvAPeJybyZbdG"

4.对字符串进行md5得到签名sign 最终结果为32位16进制字符串  

    签名结果为："8e403efea40c31e127b90470063e91a5"

签名生成算法 python 完整版  

```python
def api_arguments_sign_verify(args, appid):
    """
    接口参数签名验证
    """
    arg_sign = args.get("sign").lower()
    # 移除非业务参数
    del args["sign"]
    # 参数按首字母升序 排序
    pairs = sorted(args.items(), key=lambda e: e[0].lower())
    text = ""
    for key, value in pairs:
        text = text + "{}={}".format(key, value)
    # 字符串A首尾加上 appsecrt
    text = "{0}{1}{0}".format(games_dict.get(appid), text)
    # 对字符串B 进行md5 取16进制字符串形式
    sign = md5(text).hexdigest().lower()
    if arg_sign != sign:
        api_abort(401, message="api arguments sign verify failed")

```

**接口请求规范**

    协议： http (暂定)

    方法： POST

    自定义头部： App-Id 

    请求体(数据类型)：application/json 

`文档中涉及到 id(nft asset id) 参数 不管实际需要的是单个还是多个 都需要用列表的形式 否则会造成签名匹配不上`

### 接口列表

#####  nftGetNew (低频接口)
用于游戏端向商城发起nft资产创建请求  
`由于向链上发起铸币后需要一个确认过程 无法保证此次铸币一定是成功的`  
`商城这边收到链上监控通知后会向游戏端发送铸币成功的通知`  
`该通知会返回游戏端请求铸币时携带的 id list`
<table>
    <tbody>
        <tr>
            <td>接口提供方</td>
            <td colspan="2">商城</td>
        </tr>
        <tr>
            <td>api</td>
            <td colspan="2">/api/v1/nft/get/new</td>
        </tr>
        <tr>
            <td>描述</td>
            <td colspan="2">获取一个新的nft资产</td>
        </tr>
        <tr>
            <td colspan="3" style="text-align:center">接收参数</td>
        </tr>
        <tr>
            <td>参数</td>
            <td>类型</td>
            <td>说明</td>
        </tr>
        <tr>
            <td>userId</td>
            <td>digit string</td>
            <td>用户唯一标识符</td>
        </tr>
        <tr>
            <td>id</td>
            <td>list</td>
            <td>nft id list</td>
        </tr>
        <tr>
            <td>desc</td>
            <td>string</td>
            <td>nft资产在游戏中属性描述</td>
        </tr>
        <tr>
            <td>sign</td>
            <td>string</td>
            <td>业务参数签名</td>
        </tr>
        <tr>
            <td colspan="3" style="text-align:center">接口返回</td>
        </tr>
        <tr>
            <td>参数</td>
            <td>类型</td>
            <td>说明</td>
        </tr>
        <tr>
            <td>api</td>
            <td>string</td>
            <td>调用的接口api</td>
        </tr>
        <tr>
            <td>code</td>
            <td>int</td>
            <td>处理结果标识 1 成功 -1 失败 0 未处理</td>
        </tr>
        <tr>
            <td>http_status_code</td>
            <td>int</td>
            <td>http 请求状态码 200、 201、400、401、500</td>
        </tr>
        <tr>
            <td>message</td>
            <td>obj</td>
            <td>返回消息对象 或者错误原因</td>
        </tr>
        <tr>
            <td style="text-align: right;">userId</td>
            <td>digit string</td>
            <td>用户唯一标识符</td>
        </tr>
        <!-- <tr>
            <td style="text-align: right;">id</td>
            <td>string</td>
            <td>nft资产唯一标识符</td>
        </tr> -->
    </tbody>
</table>

处理成功返回示例：
```json
{
    "api": "/api/v1/nft/consignment",
    "code": 1,
    "http_status_code": 201,
    "message": {
        "userId": "id for user"
    }
}
```
未处理返回示例：
```json
{
    "api": "/api/v1/nft/consignment",
    "code": 0,
    "http_status_code": 401,
    "message": "api arguments sign verify failed"
}
```
处理失败返回示例：
```json
{
    "api": "/api/v1/nft/consignment",
    "code": -1,
    "http_status_code": 200,
    "message": "the reason of faile"
}
```
##### propsGetNew(中频)
    用于游戏端向商城发起道具创建请求

    items的size最好应控制在10以内

    接口提供方:  
        商城

    api:  
        /api/v1/props/get/new

    接收参数：  
        userId                      用户唯一编号
        items   list                每个item包括以下字段
            name        string          道具名称
            desc        string          道具描述
            itemId      string          道具唯一编号
            price       string    出售价格
            amount      int             道具数量
        sign  

    接口返回：详情见nftGetNew
接收参数请求示例 以下 userid sign 均在测试服务器有效
```json
参数 json object 形式
{
    "userId": "6425605781151809538",
    "items": [
        {
            "name": "prop1",
            "desc": "the desc about prop1",
            "price": "12.22334",
            "itemId": "b123456a",
            "amount": 30
        },
        {
            "name": "prop2",
            "desc": "the desc about prop2",
            "price": "10.900",
            "itemId": "c123456f",
            "amount": 100
        }
    ],
    "sign": "7a6558ac4ab050e37e4d0ddcf5aa433f"
}
参数转为 json string形式 注意外层是双引号 内层为单引号
{
    "args": "{'userId': '6425605781151809538', 'items': [{'name': 'prop1', 'desc': 'the desc about prop1', 'price': '12.22334', 'itemId': 'b123456a', 'amount': 30}, {'name': 'prop2', 'desc': 'the desc about prop2', 'price': '10.900', 'itemId': 'c123456f', 'amount': 100}]}",
    "sign": "7a6558ac4ab050e37e4d0ddcf5aa433f"
}
参与签名计算的字符串 sign_text:
"args={'userId': '6425605781151809538', 'items': [{'name': 'prop1', 'desc': 'the desc about prop1', 'price': '12.22334', 'itemId': 'b123456a', 'amount': 30}, {'name': 'prop2', 'desc': 'the desc about prop2', 'price': '10.900', 'itemId': 'c123456f', 'amount': 100}]}"
```
返回示例
```json
{
    "code": 1,
    "http_status_code": 201,
    "message": {
        "items": [
            "b123456a",
            "c123456f"
        ],
        "userId": 6425605781151809538
    },
    "api": "/api/v1/props/get/new"
}
```

#####  nftConsignmentSale(高频)
    用于游戏端向商城发起nft资产挂售请求

    接口提供方:  
        商城

    api:  
        /api/v1/nft/consignment

    接收参数：  
        args
            userId  
            id     list           单个id也用列表形式 方便以后业务扩展
            desc   json  string   资产描述
            price  digit string
            tsId   string         事务编号
        sign  

    接口返回：详情见nftGetNew

#####  nftTransfer(高频)
    用于游戏端向商城发起nft资产转移请求 

    接口提供方:  
        商城

    api:  
        /api/v1/nft/transfer

    接收参数：  
        args
            userId  
            id          list        单个id也用列表形式 方便以后业务扩展
            desc
            tsId
        sign  

    接口返回：详情见nftGetNew

#####  erc20Transfer(高频)
    用于游戏端向商城发起erc20资产转移请求

    接口提供方:  
        商城

    api:  
        /api/v1/erc20/transfer

    接收参数：  
        args
            userId  
            amount  string    
            tsId    
        sign  

    接口返回：详情见nftGetNew
请求示例:
```json
{
	"args": "{'userId': '6428506271590121473', 'amount': '33.333', 'tsId': 'afdkkhk'}",
	"sign": "17c044f80c0be9a3adc37c0fec491511"
}
```
返回示例:  
游戏端在收到 `code != -1` 的返回的情况下 将该 `事务id` 置为`已处理`的状态
```json
{
    "code": 1,
    "http_status_code": 201,
    "api": "/api/v1/erc20/transfer",
    "data": {
        "amount": 1,
        "userId": "6428506271590121473"
    }
}

{
    "code": -1,
    "http_status_code": 200,
    "api": "/api/v1/erc20/transfer",
    "message": "NOT NULL constraint failed: gametransaction.game_id"
}
```

#####  erc20Expend(高频)
    玩家在游戏内花费wbt资产接口 

    接口提供方:  
        商城

    api:  
        /api/v1/erc20/expend

    接收参数：  
        args
            userId  
            targetUserId                可选参数
            amount                      string
            tsId
        sign  

    接口返回：详情见erc20Transfer

#####  Login
    用于游戏端向商城发起登录请求

    接口提供方:  
        商城

    api:  
        /api/v1/game/login

    接收参数：  
        email  
        password  
        sign

    接口返回：
        message: info obj or error info

登录成功返回示例：
```json
{
    "api": "/api/v1/game/login",
    "code": 1,
    "http_status_code": 200,
    "message": {
        "userId": "6270805711492198401"
    }
}
```
登录失败返回示例：
```json
{
    "api": "/api/v1/game/login",
    "code": -1,
    "http_status_code": 200,
    "message": "password error"
}
```
user_id 为63位整数  
可选的session信息在http header `set-cookie`
remember_token=1|808626e403264f7e9e7c1d97eed69ad00411c251ecf8653ab7c678b347613053db1e5a7a7ab65edc783251fb49f951e7a251e50ce4805241568ab8fc50ca959a; Expires=Tue, 10-Jul-2018 07:04:51 GMT; Path=/  


####  游戏提供给商城的接口  

分配资产到游戏的接口参见  
`nftTransfer`  

`erc20Transfer`  

购买道具成功后同步到游戏参见  
 `propsGetNew`

接收铸币成功通知接口  

商城向游戏发送铸币成功通知

    接口提供方:  
        游戏

    api:  
        ""

    接收参数：  
        userId      digit string    用户唯一编号
        id          list            nft id list
        sign        string          参数签名

    接口返回：
        message: info obj or error info
