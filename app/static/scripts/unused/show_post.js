require(['jquery','plupload','qiniu'],function($){
	//时间对象的格式化; 
	Date.prototype.format = function(format) {  
	    /* 
	     * eg:format="yyyy-MM-dd hh:mm:ss"; 
	     */  
	    var o = {  
	        "M+" : this.getMonth() + 1, // month  
	        "d+" : this.getDate(), // day  
	        "h+" : this.getHours(), // hour  
	        "m+" : this.getMinutes(), // minute  
	        "s+" : this.getSeconds(), // second  
	        "q+" : Math.floor((this.getMonth() + 3) / 3), // quarter  
	        "S" : this.getMilliseconds()  
	        // millisecond  
	    }  
	    if (/(y+)/.test(format)) {  
	        format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4  
	                        - RegExp.$1.length));  
	    } 
	    for (var k in o) {  
	        if (new RegExp("(" + k + ")").test(format)) {  
	            format = format.replace(RegExp.$1, RegExp.$1.length == 1  
	                            ? o[k]  
	                            : ("00" + o[k]).substr(("" + o[k]).length));  
	        }  
	    }  
	    return format;  
	}

	function remove_by_val(arr, val){
		for(var i=0; i<arr.length; i++){
			if (arr[i] == val){
				arr.splice(i,1);
				break;
			}
		}
	}

	var require_min_count = 2,
		require_max_count = 4,
		cur_url_path = location.pathname,
		pic_list = [],
		max_file_size = '10MB',
		img_domain = 'http://img.aixunbang.com/',
		get_token_url = '/get/qiniu/uptoken';

	//遍历预览列表 有url的加入到pic_list
	$.each($('.img-preview-list').find('li'),function(){
		var that = $(this);
		if (that.data('url').indexOf(img_domain) >= 0){
			pic_list.push(that.data('url'));
		}
	})
	$('.go-back').on('click',function(){
		history.back();
		// history.go(-1); //后退+刷新 
	})
	console.log(pic_list);
	
	var uploader = Qiniu.uploader({
		runtimes: 'html5,flash,html4',      // 上传模式,依次退化
		browse_button: 'pickfiles',         // 上传选择的点选按钮，**必需**
		uptoken_url: get_token_url,
		get_new_uptoken: false,             // 设置上传文件的时候是否每次都重新获取新的 uptoken
		// unique_names: true,
		multi_selection: true,				//是否开启多选文件
		domain: img_domain,
		//container: 'container',             // 上传区域 DOM ID，默认是 browser_button 的父元素，
    	//flash_swf_url: 'path/of/plupload/Moxie.swf',  //引入 flash,相对路径
    	max_retries: 1,                     // 上传失败最大重试次数
    	dragdrop: true,                     // 开启可拖曳上传
    	drop_element: 'imgbox',          // 拖曳上传区域元素的 ID，拖曳文件或文件夹后可触发上传
    	chunk_size: '4mb',                  // 分块上传时，每块的体积
    	auto_start: false,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传,
    	filters: {
    		mime_types: [
    			{title : "Image files", extensions : "jpg,jpeg,png"}
    		],
    		max_file_size: max_file_size            // 最大文件体积限制
    	},
    	init: {
    		'QueueChanged': function(up){
    			//更新当前要上传的文件数量
    		},
	        'FilesAdded': function(up, files) {
	        	//文件数量超过指定的max_count 则不上上传
	        	console.log(up.files.length);
	        	if(files.length > 5 || up.files.length > require_max_count){
	        		console.log('最多只能选择5张图片');
	        		plupload.each(files,function(file){
	        			up.removeFile(file);
	        		})
	        	}else{
	        		plupload.each(files,function(file){
	        			add_preview_item(file);
	        		})
	        		if((up.files.length + pic_list.length) >= require_min_count){
	        			switch_up_btn(true);
	        			if((up.files.length + pic_list.length) >= require_max_count){
	        				switch_pick_btn(false);
	        			}
	        		}
	        	}
	        },
	        'FilesRemoved': function(up,files){
	        	if(up.files.length < require_max_count){
	        		switch_pick_btn(true);
	        		if(up.files.length < require_min_count){
	        			switch_up_btn(false);
	        		}
	        	}
	        },
	        'BeforeUpload': function(up, file) {
	        	// 每个文件上传前,处理相关的事情
	        },
	        'UploadProgress': function(up, file) {
	        	update_progress(file);
	               // 每个文件上传时,处理相关的事情
	        },
	        'FileUploaded': function(up, file, info) {
	        	upload_success(file);
	        	console.log(info);
	        	var res = $.parseJSON(info);
	        	console.log(res.key);
	        	var source_link = img_domain + res.key;  //获取上传成功后的文件的Url
	        	pic_list.push(source_link);
	        	show_set_cover_btn(file.id,source_link);
	        },
	        'Error': function(up, err, errTip) {
	        	if(err && err.code == plupload.FILE_SIZE_ERROR){
	        		alert('图片大小超过' + max_file_size + '了');
	        	}
	        	else if(err && err.code == plupload.FILE_EXTENSION_ERROR){
	        		alert('当前选择的文件不符合要求,请检查要上传的文件是否为jpg/png/jpeg');
	        	}
	               //上传出错时,处理相关的事情
	        },
	        'UploadComplete': function() {
	               //队列文件处理完毕后,处理相关的事情
	        },
	        'Key': function(up, file) {
	        	// console.log(file,up);
	        	var date = new Date().format('yyyy-MM-dd')
	        	var milliscond = Date.now().toString();
	        	var file_sufix = '.' + file.name. split('.')[1]
	        	var key = 'show/' + date + '/' + milliscond + file_sufix
	        	return key;
	            // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
	            // 该配置必须要在 unique_names: false , save_key: false 时才生效
	        }
    	}
	});
	
	function check_login(){
		if($('body').hasClass('lobin')){
			return true;
		}else{
			return false;
		}
	}

	function show_set_cover_btn(id,source_link){
		var target = $('#' + id).find('.set-cover');
		target.attr('data-url',source_link);
		target.show();
	}

	function upload_success(file){
		var target = $('#' + file.id);
		target.find('.up-progress').remove();
		target.find('.remove').remove();
		target.find('.success').show();
	}

	function update_progress(file){
		var target = $('#' + file.id).find('.up-progress');
		target.css('width',file.percent + '%');
	}
	
	function switch_up_btn(bool_value){
		$('#up-imgs').attr('disabled',!bool_value);
	}

	function switch_pick_btn(bool_value){
		$('#pickfiles').attr('disabled',!bool_value);
		uploader.disableBrowse(!bool_value);
	}

	function get_preview_url(file){
		// IE11（Edge），10,Chrome,Firefox 兼容
		var window_url = window.URL || window.webkitURL;
		var data_url = window_url.createObjectURL(file.getNative());
		return data_url;
	}

	//添加图片
	function add_preview_item(file){
		var browser_type = get_browser_type();
		console.log(browser_type);
		// browser_type = 'ie9';
		if(browser_type == 'safari' || browser_type == 'ie9'){
			var moxie_img = new o.Image();
			moxie_img.onload = function(){
				console.log('load success');
				this.downsize(120,120,true);
				var url = this.getAsDataURL();
				create_preview_dom(url,file.id);
			};
			moxie_img.onerror = function(e){
				console.log(e,'出错了');
			};
			moxie_img.load(file.getSource());
		}
		else{
			var url = get_preview_url(file);
			create_preview_dom(url,file.id);
		}
	}

	function create_preview_dom(url,file_id){
		var html = '<li style="background-image:url(' + url + ')"><span class="glyphicon success glyphicon-ok"></span>' + 
			'<span class="set-cover">设为封面</span>' + 
			'<span class="glyphicon remove glyphicon-remove"></span><div class="up-progress"></div></li>';
		var $item = $(html);
		$item.attr("id",file_id);
		$('.img-preview-list').append($item);
	}

	function get_browser_type(){
		var s, sys = {}, ua=navigator.userAgent.toLowerCase();
		(s=ua.match(/msie ([\d.]+)/))?sys.ie=s[1]:
		(s=ua.match(/firefox\/([\d.]+)/))?sys.firefox=s[1]:
		(s=ua.match(/chrome\/([\d.]+)/))?sys.chrome=s[1]:
		(s=ua.match(/opera.([\d.]+)/))?sys.opera=s[1]:
		(s=ua.match(/version\/([\d.]+).*safari/))?sys.safari=s[1]:0;
		if(sys.chrome){
			return 'chrome';
		}else if(sys.firefox){
			return 'firefox';
		}else if(sys.ie){
			if(sys.ie == '9.0'){
				return 'ie9';
			}
			return 'ie';
		}else if(sys.opera){
			return 'opera';
		}else if(sys.safari){
			return 'safari';
		}
	}
	
	//删除图片
	$('.img-preview-list').delegate('.remove','click',function(){
		console.log(uploader.files);
		var that = $(this),target = that.closest('li');
		var rm_file = uploader.getFile(target.attr("id"));
		if(rm_file){
			uploader.removeFile(rm_file);
		}
		console.log(uploader.files);
		target.remove();
		//编辑的情况下删除图片
		if(target.data("url") && target.data("url").indexOf(img_domain) >= 0){
			remove_by_val(pic_list, target.data('url'));
			//检查是否删掉了封面图片
			var thumbnail_dom = $('.form-filed').find('input[name="thumbnail"]');
			if(target.data('url') == thumbnail_dom.val()){
				thumbnail_dom.val('');
			}
		}
		console.log(pic_list);
	})

	//阻止pickfile btn click 默认事件
	$('.pickfiles').on('click',function(){
		return false;
	})

	//上传图片
	$('#up-imgs').on('click',function(){
		var files_count = uploader.files.length;
		if(files_count >= require_min_count && files_count <= require_max_count){
			uploader.start();
			console.log('start up imgs');
			switch_up_btn(false);
		}
		// uploader.disableBrowse();
		console.log(files_count);
		return false;
	})

	//设置封面
	$('.img-preview-list').delegate('.set-cover','click',function(){
		var target = $('.form-filed').find('input[name="thumbnail"]');
		if($(this).data('url').indexOf(img_domain) >= 0){
			target.val($(this).data('url'));
			$('.img-preview-list').find('.set-cover').text('设为封面');
			$(this).text('封面');
		}
	})

	function join_text_imgs(){
		var temp_content = '', content_filed = $('textarea');
		temp_content = '<p>' + content_filed.val() + '</p>';
		
		$.each(pic_list,function(){
			temp_content = temp_content + '<p><img src=' + this + '></p>';
		})
		content_filed.val(temp_content);
	}

	function check_before_post(){
		var is_correct = false;
		var $fileds = $('.form-filed');
		var pid = $fileds.find('input[name="pid"]').val(),
			product = $fileds.find('input[name="product"]').val(),
			thumbnail = $fileds.find('input[name="thumbnail"]').val(),
			title = $('input[name="title"]').val(),
			content = $('textarea').val();

		if($.trim(pid).length && $.trim(product).length && $.trim(thumbnail).length && $.trim(content).length && $.trim(title).length){
			if(pic_list.length >= require_min_count){
				if((Number(pid).toString() != 'NaN' && Number(pid) > 0) && ((Number(product).toString() != 'NaN' && Number(product) > 0))){
					if($.trim(content).length >= 30){
						join_text_imgs();
						return true;
					}else{
						alert('中奖感言至少30个字哦'); 
					}
				}
			}else{
				alert('至少需要上传' + require_min_count + '张商品图片');
			}
		}else if($.trim(thumbnail).length == 0){
			alert('你还为晒单设置封面呢');
		}else if($.trim(title).length == 0){
			alert('晒单标题不能为空哦');
		}else{
			alert('出错了，骚年你到底做了什么啊??');
		}
	}
	//post click
	$('.submit-btn').find('button').on('click',function(){
		console.log('click');
		if(!check_before_post()){
			return false;
		}
	})
		
})