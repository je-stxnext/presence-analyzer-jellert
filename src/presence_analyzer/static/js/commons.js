google.load("visualization", "1", {packages:["corechart"], 'language': 'en'});

function parseInterval(value) {
    var result = new Date(1,1,1);
    result.setMilliseconds(value*1000);
    return result;
}

function load_users($){
	var loading = $('#loading');
	$.getJSON("/api/v1/users", function(result) {
	    var dropdown = $("#user_id");
	    $.each(result, function(item) {
	        dropdown.append($("<option />").val(this.user_id).text(this.name));
	    });
	    dropdown.show();
	    loading.hide();
	});
}

function change_user($, url, change_user_handler){
	var loading = $('#loading');
    $('#user_id').change(function(){
        var selected_user = $("#user_id").val();
        var chart_div = $('#chart_div');
        if(selected_user) {
            loading.show();
            chart_div.hide();
            $.getJSON(url+selected_user, function(result) {
            	change_user_handler($, result);
            });
        }
    });



}


