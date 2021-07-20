  

import JsonP from 'jsonp'

// function jsonp(url) {
//         return new Promise((resolve, reject) => {
//             window.jsonCallBack =(result) => {
//                 resolve(result)
//             }
//             const JSONP = document.createElement('script');
//             JSONP.type = 'text/javascript';
//             JSONP.src = url;
//             document.getElementsByTagName('head')[0].appendChild(JSONP);
//             setTimeout(() => {
//                 document.getElementsByTagName('head')[0].removeChild(JSONP)
//             },500)
//         })
// }

export var arr = []

function jsonpgz(data) {
	return (data)
}


export function fetchData(code) {
	const realTime = Date.now();
	return new Promise((resolve,reject)=>{
		JsonP("https://fundgz.1234567.com.cn/js/" + code + ".js?rt=" + realTime,
		{
			name:"jsonpgz",
		},
		function(err,res){
			if(err!=null){
				reject(err)
			}else{
				resolve(res)
			}
		})
	})
};