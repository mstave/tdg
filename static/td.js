// var todo_data = {{ td_data|tojson|safe }};
var td_table=d3.select("#todo_div").append("table");

var thead = td_table.append("thead");
    thead.append("th").text("ID");
    thead.append("th").text("Done");
    thead.append("th").text("Prority");
    thead.append("th").text("Text");
    thead.append("th").text("Creation Date");

function update_td_html(d, p) {
    d.gui_index = p;
    if (typeof(d) == "boolean")
        return("<input type='checkbox'" + ( d ? " checked />" : "/>"));
    else
        return d;
};

var rows = td_table.selectAll("tr").data(todo_data);
rows.enter().append("tr")
rows.exit().remove();

var td = rows.selectAll("td")
            .data(function(d, p) {
                // d.gui_index = p
                return  [p, d._done, d._priority, d.task, d.creation_date];
            })

td.enter().append("td")
            .html(update_td_html);

td.exit().remove()
var d_item;
rows.on('click', function(d,i) {
    // alert(i);
    // d3.select(this)
    d_item=d;

    if (curr_item != null)
        curr_item.classed("myhighlight", false);
    curr_item = d3.select(this).classed("myhighlight",true);

});

var curr_row = 0;
var curr_item;

d3.select("body").on('keydown', function(d,i) {
    // alert(d3.event.keyCode);
    k = d3.event.keyCode;
    if  (k >= 65 && k <= 69) {
        todo_data[curr_row]._priority = String.fromCharCode(k);
    }
    switch (d3.event.keyCode) {
        case 37:
            break; // left
        case 39:
            break; // right
        case 38:
            if (curr_row > 0)
                console.log("setting curr_row to " + (curr_row - 1));
                // curr_item = curr_item.previous_sibling;
                curr_row--;
            break; // up
        case 40:
            if (curr_row < todo_data.length)
                curr_item = curr_item.next_sibling;
                curr_row++;
            break; // down
    update_all();
    }

});

rows.on('mouseover', highlight)
// rows.on('mouseout', unlight)
// d3.selectAll("tr").select("td").insert("input").attr("type", "checkbox");

function update_all() {
    td_table.selectAll("tr")
            .data(todo_data)
            .classed("myhighlight", function(d,i) {
                 console.log("i == " + i + " curr_row = " + curr_row);
                 return curr_row == i;
             });
    rows.selectAll("td")
        .data(function(d, p) {
            return  [p, d._done, d._priority, d.task, d.creation_date];
        })
        .html(update_td_html);
}

function highlight(d, i) {
    d3.select("#comms").text("Row " + i);
    curr_row = i;
    update_all()
    // if (curr_item != null)
        // curr_item.classed("myhighlight", false);
    // curr_item = d3.select(this).classed("myhighlight",true);
    // curr_item = this;
    // d3.select(this).style('background-color', 'gray').style('color','white');

}
function unlight(d, i){
    d3.select(this).style('background-color', 'white').style('color','black');
}
td.exit().remove();
