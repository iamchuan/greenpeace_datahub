var $layersCtrl;
var $map = L.map('mapid');
var $year = ['2017', '2016', '2015', '2014', '2013'];

$(function() {

    $(".se-pre-con").hide();

    $map.setView([34.53, 108.92], 4);

    var $tileLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo($map);

//    add year options
    $.each($year, function(index, value) {
        $('#select_year').append('<option value="' + value + '"> ' + value + ' </option>');
    })

    Number.prototype.pad = function(size) {
        var s = String(this);
        while (s.length < (size || 2)) {s = "0" + s;}
        return s;
    }

//    add month options
    for (i = 1; i < 13; i++) {
        $('#select_month').append('<option value="' + i + '"> ' + (i).pad(2) + ' </option>');
    }


// Get the options to be hidden/shown
    var ary = [1, 2, 3, 4, 5, 6];

    var $month_to_hide = $('select[name=month] option').filter(function () {
        return ($.inArray(parseInt(this.value), ary) > -1);
    });


    $('#select_year').on('change', function () {
        if ($('select[name="year"]').val() == 2016) {
            if ($.inArray(parseInt($('select[name="month"]').val()), ary) > -1) {
                $('select[name="month"]').val('7');
            }
            $month_to_hide.attr('disabled','disabled');
        } else {
            $month_to_hide.removeAttr('disabled');
        }
    })


    $('.draggable').draggable();

    var date = {
            year: $('select[name="year"]').val(),
            month: $('select[name="month"]').val(),
    };

    $('#show_level').on('click', function() {
        $('#p_levels').show(500);
    })

    $('#hide_level').on('click', function() {
        $('#p_levels').hide(500);
    })

    $('#submit').on('click', function() {

        $(".se-pre-con").fadeIn(300);

        var date = {
            year: $('select[name="year"]').val(),
            month: $('select[name="month"]').val(),
        };

        var newLayers = {};

        $.getJSON($SCRIPT_ROOT + '/pollutants', date)
        .done(function(data) {
            $(".se-pre-con").fadeOut(300);
//            create new layer group
            $.each(data, function(key, rows){
                var pol = [];
                $.each(rows, function(index, row) {
                    pol.push(L.circleMarker([row.lat, row.lng], {radius: 6, color: row.col, fillOpacity: 0.4})
                    .bindPopup('<strong>' + row.area + '<br>' + key + ': ' + row.val + '</strong>'))
                });

                newLayers[key] = L.layerGroup(pol);
            });
//            remove existed layer group
            if ($layersCtrl !== undefined) {
                $.each($layersCtrl._layers, function(index, layer) {
                    $map.removeLayer(layer['layer']);
                })
                $map.removeControl($layersCtrl);
            }
//            add new layer group
            $layersCtrl = L.control.layers(newLayers, null, {collapsed: false}).addTo($map);
            $map.addLayer($layersCtrl._layers[0]['layer']);
        })
        .fail(function() { alert('Your request cannot be completed, please try again later!'); });
    })

})