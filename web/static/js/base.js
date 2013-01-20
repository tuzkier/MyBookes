(function(w){

	function init_wfh()
	{
		return {
			get_event_target: function(e){
				if (!e)
					return null;
				e = window.event || e;
				return e.target || e.srcElement;
			}
		}
	}
	w.wfh = init_wfh();
})(window)
