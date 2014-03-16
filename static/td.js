// var todo_data = {{ td_data|tojson|safe }};
var todo = {}       // Namespace for all this

todo.init = function() {
    d3.json("todo.json", function(error, json) {
        todo.todo_data=json.dd;     // json todo_file
        if (error) {
            console.warn(error);
            return alert(error);
        }
        todo.create_table();
    })
}

todo.create_table = function() {
    todo.curr_row = 0;      // row that is selected
    todo.td_table=d3.select("#todo_div").append("table");
    // todo: create an array of column names and  use thead.data()
    todo.thead = todo.td_table.append("thead");

    todo.thead.append("th").text("ID");
    todo.thead.append("th").text("X");
    todo.thead.append("th").text("Pri");
    todo.thead.append("th").text("Task");
    todo.thead.append("th").text("Created");

    todo.rows = todo.td_table.selectAll("tr").data(todo.todo_data);
    todo.rows.enter().append("tr")
    todo.rows.exit().remove();

    todo.td = todo.rows.selectAll("td")
            .data(function(d, p) {
                // d.gui_index = p
                return  [p, d._done, d._priority, d.task, d.creation_date];
            })

    todo.td.enter().append("td")
            .html(todo.update_td_html);

    todo.td.exit().remove()

// todo should this be window.on?
    d3.select("body").on('keydown', function(d,i) {
        // alert(d3.event.keyCode);
        k = d3.event.keyCode;
        if  (k >= 65 && k <= 69) {
            todo.todo_data[todo.curr_row]._priority = String.fromCharCode(k);
        }
        switch (d3.event.keyCode) {
            case 37:      // left
                todo.update_all();  // for debugging: force an update
                break;    // right
            case 39:
                break;
            case 38:      // up
                if (todo.curr_row > 0) {
                    todo.curr_row--;
                }
                break;

            case 40:      // down
                if (todo.curr_row < todo.todo_data.length)
                    todo.curr_row++;
                break;
        }
        todo.update_all();
    });

    todo.rows.on('mouseover', todo.highlight)
    // todo fix this to test highlight prop
    todo.rows.on('click', function(d,i) {
        // if (todo.curr_item != null)
        //     todo.curr_item.classed("myhighlight", false);
        // todo.curr_item = d3.select(this).classed("myhighlight",true);
    });

}

todo.update_td_html = function(d, p) {
    d.gui_index = p;
    if (typeof(d) == "boolean")
        return("<input type='checkbox'" + ( d ? " checked />" : "/>"));
    else
        return d;
};

todo.update_all = function() {
    console.log("Updating all");
    todo.td_table.selectAll("tr")
            .data(todo.todo_data)
            .classed("myhighlight", function(d,i) {
                 // console.log("i == " + i + " curr_row = " + curr_row);
                 return todo.curr_row == i;
             });
    todo.rows.selectAll("td")
        .data(function(d, p) {
            return  [p, d._done, d._priority, d.task, d.creation_date];
        })
        .html(todo.update_td_html);
}

todo.highlight = function(d, i) {
    d3.select("#comms").text("Row " + i);
    todo.curr_row = i;
    todo.update_all()

}

todo.init();