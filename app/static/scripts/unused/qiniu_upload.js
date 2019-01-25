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

	var require_min_count = 3,
		require_max_count = 5,
		cur_url_path = location.pathname,
		max_file_size = '10MB',
		img_domain = 'http://img.aixunbang.com/',
		get_token_url = '/get/qiniu/uptoken';

	
	var uploader = Qiniu.uploader({
		runtimes: 'html5,flash,html4',      // 上传模式,依次退化
		browse_button: 'pickfiles',         // 上传选择的点选按钮，**必需**
		uptoken_url: get_token_url,
		get_new_uptoken: false,             // 设置上传文件的时候是否每次都重新获取新的 uptoken
		// unique_names: true,
		multi_selection: false,				//是否开启多选文件
		domain: img_domain,
		//container: 'container',             // 上传区域 DOM ID，默认是 browser_button 的父元素，
    	//flash_swf_url: 'path/of/plupload/Moxie.swf',  //引入 flash,相对路径
    	max_retries: 1,                     // 上传失败最大重试次数
    	dragdrop: false,                     // 开启可拖曳上传
    	drop_element: 'imgbox',          // 拖曳上传区域元素的 ID，拖曳文件或文件夹后可触发上传
    	chunk_size: '4mb',                  // 分块上传时，每块的体积
    	auto_start: true,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传,
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
	        },
	        'FilesRemoved': function(up,files){
	        },
	        'BeforeUpload': function(up, file) {
	        },
	        'UploadProgress': function(up, file) {
	        },
	        'FileUploaded': function(up, file, info) {
	        	console.log(info);
	        	var res = $.parseJSON(info);
	        	console.log(res.key);
	        	var sourceLink = img_domain + res.key; //获取上传成功后的文件的Url
	        	if ($('#thumbnail').length > 0){
	        		$('#thumbnail').val(sourceLink);
	        		$('.preview-img').attr("src",sourceLink);
	        	}
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
	        	var milliscond = Date.now().toString()
	        	var file_sufix = '.' + file.name. split('.')[1]
	        	var key = 'thumbnail/' + date + '/' + milliscond + file_sufix
	        	return key;
	            // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
	            // 该配置必须要在 unique_names: false , save_key: false 时才生效
	        }
    	}
	});
	
	//阻止pickfile btn click 默认事件
	$('.pickfiles').on('click',function(){
		return false;
	})

})