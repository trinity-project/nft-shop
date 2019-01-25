define(function(){
    function commonUserCenterText(lgT, lgFlag) {
        lgT.home_lg_1 = lgFlag == "cn" ? "首页" : "Home";
        lgT.home_lg_2 = lgFlag == "cn" ? "个人中心" : "Personal Center";
        lgT.home_lg_3 = lgFlag == "cn" ? "点击编辑头像" : "Click To Edit The Head Image";
        lgT.home_lg_4 = lgFlag == "cn" ? "修改密码" : "Modify Password";
        lgT.home_lg_5 = lgFlag == "cn" ? "充值NFT" : "recharge NFT";
        lgT.home_lg_6 = lgFlag == "cn" ? "充值WBT" : "recharge WBT";
        lgT.home_lg_7 = lgFlag == "cn" ? "我的账户" : "My Account";
        lgT.home_lg_8 = lgFlag == "cn" ? "充值记录" : "Recharge Record";
        lgT.home_lg_9 = lgFlag == "cn" ? "提币记录" : "Currency Record";
        lgT.home_lg_10 = lgFlag == "cn" ? "售卖记录" : "Sales Record";
        lgT.home_lg_11 = lgFlag == "cn" ? "订单记录" : "Order Record";
        lgT.modal_box_lg_18 = lgFlag == "cn" ? "充值" : "Recharge";
        lgT.home_lg_12 = lgFlag == "cn" ? "已触到到尽头了!" : "It's at the end of the touch!";
    }

	function getLanguageText(pgName, lgFlag) {
        var lgT = {
            header_lg_1: lgFlag == "cn" ? "ENGLISH" : "中 文",
            header_lg_2: lgFlag == "cn" ? "语言" : "Language",
            header_lg_3: lgFlag == "cn" ? "登录" : "LOG IN",
            header_lg_4: lgFlag == "cn" ? "注册" : "REGISTERED",
            header_lg_5: lgFlag == "cn" ? "欢迎" : "WELCOME",
            header_lg_6: lgFlag == "cn" ? "登出" : "LOG OUT",
            header_lg_7: lgFlag == "cn" ? "搜索" : "Search",
            header_lg_8: lgFlag == "cn" ? "首页" : "Home",
            header_lg_9: lgFlag == "cn" ? "官方商城" : "Official Market",
            header_lg_10: lgFlag == "cn" ? "C2C商城" : "C2C Market",
            header_lg_11: lgFlag == "cn" ? "游戏论坛" : "Game Forum",
            header_lg_12: lgFlag == "cn" ? "常见问题" : "Common Problem",
            header_lg_13: lgFlag == "cn" ? "新手指南" : "Novice Guide",
            footer_lg_1: lgFlag == "cn" ? "快加入OpenSea社区吧" : "Join the OpenSea Community",
            footer_lg_2: lgFlag == "cn" ? "快加入OpenSea社区吧快加入OpenSea社区吧" : "Join the OpenSea Community Join the OpenSea Community",
            a404_lg_1 : lgFlag == "cn" ? "抱歉，您似乎来错地方了！" : "Sorry, you seem to be in the wrong place!",
            a404_lg_2 : lgFlag == "cn" ? "返回首页" : "Return to the home page",
            a500_lg_1 : lgFlag == "cn" ? "抱歉，服务器出了点小故障，我们正抓紧抢修！" : "Sorry, there is a little trouble with the server. We are rush to repair it!",
            a500_lg_2 : lgFlag == "cn" ? "返回首页" : "Return to the home page",
        };
        var name = pgName.replace(/\/\d/g, "");
        switch(name) {
            case "/index":
                lgT.index_lg_1 = lgFlag == "cn" ? "首页" : "Home";
                break;
            case "/market":
                lgT.market_lg_1 = lgFlag == "cn" ? "所有分类" : "All Lassifications:";
                lgT.market_lg_2 = lgFlag == "cn" ? "所有商品" : "All Goods";
                lgT.market_lg_3 = lgFlag == "cn" ? "所有商品" : "All Goods";
                lgT.market_lg_4 = lgFlag == "cn" ? "排序:" : "Sort:";
                lgT.market_lg_5 = lgFlag == "cn" ? "人气商品" : "Popular Goods";
                lgT.market_lg_6 = lgFlag == "cn" ? "最近上架" : "New Arrival";
                lgT.market_lg_7 = lgFlag == "cn" ? "人气商品" : "Popular Goods";
                lgT.market_lg_8 = lgFlag == "cn" ? "最新上架" : "New Arrival";
                lgT.market_lg_9 = lgFlag == "cn" ? "全部种类" : "All Categories";
                lgT.market_lg_10 = lgFlag == "cn" ? "请登录您的账号" : "Please Log In";
                lgT.market_lg_11 = lgFlag == "cn" ? "特性" : "Properties";
                lgT.market_lg_12 = lgFlag == "cn" ? "滤波特性" : "Filter Properties";
                lgT.market_lg_13 = lgFlag == "cn" ? "展示更多" : "Show More";
                lgT.market_lg_14 = lgFlag == "cn" ? "时代" : "Generation";
                lgT.list_item_lg_2 = lgFlag == "cn" ? "立即购买" : "Buy Now";
                break;
            case "/guide":
                lgT.guide_lg_1 = lgFlag == "cn" ? "了解NFT商城平台" : "Understand the NFT business city platform";
                break;
            case "/faq":
                lgT.faq_lg_1 = lgFlag == "cn" ? "常见问题" : "COMMON PROBLEM";
                break;
            case "/user/home":
                commonUserCenterText(lgT, lgFlag);
                lgT.account_lg_1 = lgFlag == "cn" ? "温馨提示: 只有nft资产才有资产ID" : "Reminder:Only NFT assets have assets ID";
                lgT.account_lg_2 = lgFlag == "cn" ? "资产类型" : "Asset Type";
                lgT.account_lg_3 = lgFlag == "cn" ? "资产数量" : "Asset Number";
                lgT.account_lg_4 = lgFlag == "cn" ? "可用数量" : "Available Number";
                lgT.account_lg_5 = lgFlag == "cn" ? "锁定数量" : "Locked Number";
                lgT.account_lg_6 = lgFlag == "cn" ? "资产ID" : "ASSET ID";
                lgT.account_lg_7 = lgFlag == "cn" ? "操作" : "Operation";
                lgT.account_lg_8 = lgFlag == "cn" ? "分配" : "Distribution";
                lgT.account_lg_9 = lgFlag == "cn" ? "提币" : "Take Coin";
                lgT.account_lg_10 = lgFlag == "cn" ? "挂售" : "Hang and Sell";
                lgT.account_lg_11 = lgFlag == "cn" ? "分配" : "Distribution";
                lgT.account_lg_12 = lgFlag == "cn" ? "提币" : "Take Coin";
                lgT.modal_box_lg_1 = lgFlag == "cn" ? "分配资产到游戏" : "Distribution of Assets to Games";
                lgT.modal_box_lg_2 = lgFlag == "cn" ? "资产类型: NFT" : "Asset Type:NFT";
                lgT.modal_box_lg_3 = lgFlag == "cn" ? "资产编号:" : "Asset Number:";
                lgT.modal_box_lg_4 = lgFlag == "cn" ? "选择游戏" : "Choose the Game";
                lgT.modal_box_lg_5 = lgFlag == "cn" ? "分配数量" : "Assigned Amount";
                lgT.modal_box_lg_6 = lgFlag == "cn" ? "确定" : "Confirm";
                lgT.modal_box_lg_7 = lgFlag == "cn" ? "提币到您的账户" : "Money to Your Account";
                lgT.modal_box_lg_8 = lgFlag == "cn" ? "资产类型:" : "Asset Type:";
                lgT.modal_box_lg_9 = lgFlag == "cn" ? "资产编号:" : "Asset Number:";
                lgT.modal_box_lg_10 = lgFlag == "cn" ? "提币地址" : "Currency Address";
                lgT.modal_box_lg_11 = lgFlag == "cn" ? "提币数量" : "Currency Number";
                lgT.modal_box_lg_12 = lgFlag == "cn" ? "确定" : "Confirm";
                lgT.modal_box_lg_13 = lgFlag == "cn" ? "挂售资产" : "Hang Up Assets";
                lgT.modal_box_lg_14 = lgFlag == "cn" ? "资产类型:" : "Asset Type:";
                lgT.modal_box_lg_15 = lgFlag == "cn" ? "资产编号:" : "Asset Number:";
                lgT.modal_box_lg_16 = lgFlag == "cn" ? "挂售数量" : "Currency Number";
                lgT.modal_box_lg_17 = lgFlag == "cn" ? "确定" : "Confirm";
                break;
            case "/user/recharge":
                commonUserCenterText(lgT, lgFlag);
                lgT.recharge_records_lg_1 = lgFlag == "cn" ? "充值时间" : "Recharge Time";
                lgT.recharge_records_lg_2 = lgFlag == "cn" ? "资产类型" : "Asset Type";
                lgT.recharge_records_lg_3 = lgFlag == "cn" ? "充值数量" : "Recharge Number";
                lgT.recharge_records_lg_4 = lgFlag == "cn" ? "交易txID" : "Transaction txID";
                lgT.recharge_records_lg_5 = lgFlag == "cn" ? "上架时间" : "Shelf Time";

                lgT.recharge_order_lg_1 = lgFlag == "cn" ? "请扫描二维码完成您的订单" : "Please scan the QR code to complete your order";
                lgT.recharge_order_lg_2 = lgFlag == "cn" ? "收款地址为:" : "Receivable address:";

                lgT.recharge_infos_lg_1 = lgFlag == "cn" ? "充值订单编号" : "Recharge order number";
                lgT.recharge_infos_lg_2 = lgFlag == "cn" ? "资产类型" : "Asset type";
                lgT.recharge_infos_lg_3 = lgFlag == "cn" ? "充值数量" : "Amount of recharge";
                lgT.recharge_infos_lg_4 = lgFlag == "cn" ? "链上交易txID" : "Chain Trading txID";
                lgT.recharge_infos_lg_5 = lgFlag == "cn" ? "充值状态" : "Recharge state";
                lgT.recharge_infos_lg_6 = lgFlag == "cn" ? "创建时间" : "Creation time";
                lgT.recharge_infos_lg_7 = lgFlag == "cn" ? "完成" : "OK";
                lgT.recharge_infos_lg_8 = lgFlag == "cn" ? "请确认充值订单" : "Please confirm the order of recharge";
                break;
            case "/user/takeout":
                commonUserCenterText(lgT, lgFlag);
                lgT.takeout_records_lg_1 = lgFlag == "cn" ? "资产类型" : "Asset Type";
                lgT.takeout_records_lg_2 = lgFlag == "cn" ? "提币数量" : "Currency Number";
                lgT.takeout_records_lg_3 = lgFlag == "cn" ? "交易txID" : "Transaction txID";
                lgT.takeout_records_lg_4 = lgFlag == "cn" ? "提币状态" : "Currency Status";
                lgT.takeout_records_lg_5 = lgFlag == "cn" ? "到账时间" : "Payment Date";
                break;
            case "/user/order":
                commonUserCenterText(lgT, lgFlag);
                lgT.order_records_lg_1 = lgFlag == "cn" ? "充值时间" : "Creation Time";
                lgT.order_records_lg_2 = lgFlag == "cn" ? "订单编号" : "Order Number";
                lgT.order_records_lg_3 = lgFlag == "cn" ? "买家信息" : "Commodity Buyers";
                lgT.order_records_lg_4 = lgFlag == "cn" ? "关联商品" : "Associated Goods";
                break;
            case "/user/take_coin":
                commonUserCenterText(lgT, lgFlag);
                break;
            case "/user/sales":
                commonUserCenterText(lgT, lgFlag);
                lgT.sales_records_lg_1 = lgFlag == "cn" ? "关联资产" : "Associated Assets";
                lgT.sales_records_lg_2 = lgFlag == "cn" ? "售卖价格" : "Selling Price";
                lgT.sales_records_lg_3 = lgFlag == "cn" ? "售卖状态" : "Selling Status";
                lgT.sales_records_lg_4 = lgFlag == "cn" ? "申请时间" : "Application Time";
                break;
            case "/login":
                commonUserCenterText(lgT, lgFlag);
                lgT.login_lg_1 = lgFlag == "cn" ? "邮箱" : "EMAIL";
                lgT.login_lg_2 = lgFlag == "cn" ? "密码" : "PASSWORD";
                lgT.login_lg_3 = lgFlag == "cn" ? "记住密码" : "REMEMBER ME";
                lgT.login_lg_4 = lgFlag == "cn" ? "忘记密码？" : "FORGET THE PASSWORD？";
                lgT.login_lg_5 = lgFlag == "cn" ? "登录" : "LOG IN";
                break;
            case "/register":
                commonUserCenterText(lgT, lgFlag);
                lgT.register_lg_1 = lgFlag == "cn" ? "邮箱" : "EMAIL";
                lgT.register_lg_2 = lgFlag == "cn" ? "密码" : "PASSWORD";
                lgT.register_lg_3 = lgFlag == "cn" ? "确认密码" : "CONFIRM THE PASSWORD";
                lgT.register_lg_4 = lgFlag == "cn" ? "注册" : "REGISTER";
                break;
            case "/order/confirm":
                commonUserCenterText(lgT, lgFlag);
                lgT.order_lg_1 = lgFlag == "cn" ? "订单编号" : "Order Number";
                lgT.order_lg_2 = lgFlag == "cn" ? "买家信息" : "Buyer Information";
                lgT.order_lg_3 = lgFlag == "cn" ? "卖家信息" : "Seller Information";
                lgT.order_lg_4 = lgFlag == "cn" ? "创建时间" : "Creation Time";
                lgT.order_lg_5 = lgFlag == "cn" ? "确认订单" : "Confirm Order";
                lgT.order_lg_6 = lgFlag == "cn" ? "请确认订单" : "Please Confirm the Order";
                break;

        }
        return lgT;
    }
    return getLanguageText;
})