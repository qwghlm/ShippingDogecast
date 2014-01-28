$(document).ready(function() {
    currentForecast = -1;
    currentLine = 3;
    $.get('dogecast.json', successJSON);   
});

var forecast;
var currentForecast;
var lines = ['label', 'wind', 'sea_state', 'weather', 'visibility'];
var currentLine;

function successJSON(data) {
    forecast = data.areas;
    $('#last_updated').html("Last updated: " + data.last_updated + ".");
    nextLine();
    setInterval(nextLine, 6000);
}

var colors = ['#FF00FF', '#00FF00', '#0033FF', '#FFFF00'];

function randSort() {
    return Math.random() < 0.5;
}

function nextLine() {
    $('#main').fadeOut(500, updateScreen);
}

function updateScreen() {

    currentForecast++;
    currentForecast %= forecast.length;

    var forecastData = forecast[currentForecast];
    colors.sort(randSort);

    for (var i=0; i<lines.length; i++) {
        var areaName = lines[i];
        var $area = $("#area-" + areaName);

        if (areaName !== 'label') {
            var top = $area.data('top') + 10 * Math.random();
            var left = $area.data('left') + 10 * Math.random();
            var color = colors[i-1];
            $area.css({
                'color' : color,
                'top' : top + '%',
                'left' : left + '%'
            });
        }
 
        $area.empty().html(forecastData[areaName]);
    }

    $('#main').fadeIn(500);

}


