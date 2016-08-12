
$(document).ready(function(){
    job_selected_change($('.job').first());
    $(".cpu_used").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) ||
             // Allow: Ctrl+C
            (e.keyCode == 67 && e.ctrlKey === true) ||
             // Allow: Ctrl+X
            (e.keyCode == 88 && e.ctrlKey === true) ||
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });
});

$("#job_selected").change(function(){
    job_selected = $("select option:selected").text();
    $(".job").each(function(){
        if ($(this).hasClass("hide") === false){
            $(this).addClass("hide");
        }
        if ($(this).find("td:eq(1)").text() == job_selected){
            $(this).removeClass("hide");
            job_selected_change($(this));
        }
    });
});

function job_selected_change(tb_element){
    var data_need = {};
    var data_vol = 0;

    tb_element.find(".data_used").each(function(){
        var volume = $(this).find("span").text();
        data_need[$(this).text().replace(volume,'')] = Number(volume.slice(0, -2));
        data_vol += Number(volume.slice(0, -2));
    });
    tb_element.find(".total").html(data_vol + " GB");

    $(".server").each(function(){
        $(this).find(".data_hosted").find("span").css("color", "black");
        var data_had = 0;
        var data_missing = "";
        var data_got = $(this).find(".data_hosted").find("span").text().split(", ");

        for (var key in data_need){
            var position = data_got.indexOf(key);
            if ( position != -1 ){
                $(this).find(".data_hosted").find("span").eq(position).css("color", "green");
                data_had += data_need[key];
            }
            else{
                data_missing += key + ", ";
            }
        }
        if (data_missing === ""){
            data_missing = "N/A";
        }
        else{
            lack = data_vol-data_had;
            data_missing = data_missing.slice(0,-2) + " (" + lack + "GB of " + data_vol + "GB)";
        }
        $(this).find(".data_covered").html((100*data_had/data_vol).toFixed(1) + "%");
        $(this).find(".data_missed").html(data_missing);
    });
}

$("#refresh").click(function(){
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    $(".server").each(function(){
        server_name = $(this).find("h4").text().split(",")[0];
        server = $(this);
        $.ajax({
            type: "POST",
            url: "/run_ajax/",
            data:{
                csrfmiddlewaretoken: csrf_token,
                server_name: server_name
            },
            success: function(ret){
                var $selected = $("." + server_name);
                populate_chart(ret[server_name], d3.select($selected.toArray()[0]));
                calculate_cpus_avail(ret[server_name], server);
            }
        });
    });

    $("#refresh").attr("disabled", "disabled");
    setTimeout(function(){
        $("#refresh").removeAttr("disabled");
    }, 1000);
});

$(".cpu_used").change(function(){
    var total_reps = 0;
    $(".cpu_used").each(function(){
        total_reps += Number($(this).val());
    });
    $(".total_reps").html(total_reps);
});

var margin = {top: 30, right: 10, bottom: 10, left: 40},
    width = 480 - margin.left - margin.right,
    height = 260 - margin.top - margin.bottom;

var x = d3.scale.ordinal().rangeRoundBands([0, width], 0.1);
var y = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis().scale(x).orient("bottom");
var yAxis = d3.svg.axis().scale(y).orient("left").ticks(10, "%");

// var svgs = [];
$(".server").each(function(){
    server = $(this).find("h4").text().split(",")[0];
    var svg = d3.select(".chartHolder").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("class", server)
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("y", 0)
            .attr("dy", "-1em")
            .style("text-anchor", "head")
            .text("Utilization");
    populate_chart(server_utils[server], svg);
    calculate_cpus_avail(server_utils[server], $(this));
});

function populate_chart(util_list, svg){
    svg.selectAll(".bar").remove();
    var len = util_list.length;
    var bar = svg.selectAll(".bar")
                    .data(util_list)
                    .enter().append("rect")
                    .attr("class", "bar")
                    .attr("x", function(d,i) { return i * (430/len) + 130/len; })
                    .attr("width", 300/len)
                    .attr("y", function(d) { return 220 - 2.2*d; })
                    .attr("height", function(d) { return 2.2*d; })
                    .selectAll("div");
}

function calculate_cpus_avail(util_list, server_element){
    var num = 0;
    util_list.map(function(x){if(x <= 10)num++;});
    server_element.find(".cpus_avail").html(num);
}
