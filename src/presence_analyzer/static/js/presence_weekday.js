function visualize_user_data($, result) {
 	var chart_div = $('#chart_div');
 	var loading = $('#loading');
    var data = google.visualization.arrayToDataTable(result);
    var options = {};
    chart_div.show();
    loading.hide();
    var chart = new google.visualization.PieChart(chart_div[0]);
    chart.draw(data, options);
}