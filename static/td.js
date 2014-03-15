// var todo_data = {{ td_data|tojson|safe }};
var td_table=d3.select("#todo_div").append("table");
var thead = td_table.append("thead");
    thead.append("th").text("ID");
    thead.append("th").text("Done");
    thead.append("th").text("Prority");
    thead.append("th").text("Text");
    thead.append("th").text("Creation Date");

function update_td_html(d) {
    if (typeof(d) == "boolean")
        return("<input type='checkbox'" + ( d ? " checked />" : "/>"));
    else
        return d;
};

var rows = td_table.selectAll("tr").data(todo_data);
rows.enter().append("tr");
rows.exit().remove();

var td = rows.selectAll("td")
            .data(function(d, p) {
                return  [p, d._done, d._priority, d.task, d.creation_date];
            })
td.enter().append("td")
            .html(update_td_html);

td.exit().remove()

rows.on('click', function(d,i) {
    // alert(i);
    // d3.select(this) -
});

var curr_row = 0;

d3.select("body").on('keydown', function() {
    // alert(d3.event.keyCode);
    k = d3.event.keyCode;
    if  (k >= 65 && k <= 69) {
        todo_data[curr_row]._priority = String.fromCharCode(k);
    }
    switch (d3.event.keyCode) {
      case 65: {
        // alert(todo_data[curr_row]._priority);
        // todo_data[curr_row]._priority='(a)';

        rows.selectAll("td")
            .data(function(d, p) {
                return  [p, d._done, d._priority, d.task, d.creation_date];
            })
            .html(update_func);
                // 
                // if (typeof(d) == "boolean")
                    // return("<input type='checkbox'" + ( d ? " checked />" : "/>"))
                // else
                    // return d;
        break;
        }
    }
});

rows.on('mouseover', highlight)
rows.on('mouseout', unlight)
// d3.selectAll("tr").select("td").insert("input").attr("type", "checkbox");
function highlight(d, i) {
    d3.select("#comms").text("Row " + i);
    curr_row = i;
    d3.select(this).style('background-color', 'gray').style('color','white');

}
function unlight(d, i){
    d3.select(this).style('background-color', 'white').style('color','black');
}
td.exit().remove();
