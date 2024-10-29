function c(id){
}
function popTip(d) {
	if(!document.getElementById("J_FIXED")){
		var div = document.createElement("div");
		div.innerHTML = '<div id="J_FIXED" class="m-tip" style="display:none;"><div id="J_TIPS" class="inner"></div></div>';
		document.body.appendChild(div); 
	}
	document.getElementById("J_TIPS").innerHTML = d;
	document.getElementById("J_FIXED").style = "display:block";
	window.setTimeout(function(){ 
		document.getElementById("J_FIXED").style = "display:none";
	},3000);
}
function copy(id) {
	var clipboard = new ClipboardJS(id); 
	clipboard.on('success', function(e) {
		popTip('已复制')
	});
	clipboard.on('error', function(e) {
		popTip('复制失败')
	});
}
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?3ee8fad4703fe9b02a2710613ec82335";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
document.addEventListener('DOMContentLoaded',function(){var $navbarBurgers=Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'),0); if($navbarBurgers.length>0){$navbarBurgers.forEach(function($el){$el.addEventListener('click',function(){var target=$el.dataset.target;var $target=document.getElementById(target);$el.classList.toggle('is-active');$target.classList.toggle('is-active')})})}});