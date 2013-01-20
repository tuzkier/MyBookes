(function(){
	$(document).ready(function(){
		$(document).scroll(function(){
			if ($(document).scrollTop() >= 57)
			{
				$(".category").removeClass("pos-absolute");
				$(".category-container").addClass("suspended");
				$(".category").addClass("pos-fixed");
				$(".category").addClass("category-fixed");
			}
			else
			{
				$(".category").removeClass("pos-fixed");
				$(".category-container").removeClass("suspended");
				$(".category").addClass("pos-absolute");
				$(".category").removeClass("category-fixed");
			}
		});
		$(".category .category-list").bind("click",function(e){
			var target = wfh.get_event_target(e);
			if (target.tagName.toLowerCase() != "a")
				return;
			$(".category-item").removeClass("category-selected")
			$(target).parent().addClass("category-selected")
		});
	});
})();
