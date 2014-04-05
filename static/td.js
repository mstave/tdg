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

// todo.rows = null;

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
            .html(todo.update_td_html)
            .on("change", function (d, p) {
                todo.tempsave = todo.todo_data[todo.clicked];
                todo.tempsave2  = d
                // alert("blurry p: " + p + " d: " + d + " this: " + this + " item: " + todo.todo_data[todo.clicked]);
                d3.xhr("/json.up").header('content-type','application/json').post(JSON.stringify(todo.tempsave), function(error, data) {
                    // d3.xhr("/modify/" + todo.clicked + "/task/foobar").get(function(error, data) {
                    console.log(error);
                    console.log(data);
                    alert (error + data);
                });
            });

    todo.td.exit().remove()

    todo.unpause_events();

// todo should this be window.on?


    todo.toggle_complete = function() {
        todo.todo_data[todo.curr_row]._done = !todo.todo_data[todo.curr_row]._done;
    }

    // todo.rows.on('mouseover', todo.highlight)
    // // todo fix this to test highlight prop
    // todo.rows.on('dblclick', function(d,i) {
    //     todo.clicked = i;
    //     // todo.update_all();
    // });

}
todo.col_count = -1;

todo.pause_events = function() {
    todo.rows.on('dblclick', null);
    todo.rows.on('mouseover', null);
    d3.select("body").on('keydown',null);
}

todo.unpause_events = function ()  {
    todo.rows.on('mouseover', todo.highlight)
    // todo fix this to test highlight prop
    todo.rows.on('dblclick', function(d,i) {
        todo.clicked = i;
        todo.pause_events();
        todo.update_all();
    });
        d3.select("body").on('keydown', function(d,i) {
        // alert(d3.event.keyCode);
        k = d3.event.keyCode;
        if  (k >= 65 && k <= 69) {
            todo.todo_data[todo.curr_row]._priority = String.fromCharCode(k);
        }
        switch (k) {
            case 32:      // space
                // alert("spaced!");
                todo.toggle_complete();
                d3.event.preventDefault();
                break;
            case 37:      // left
                todo.update_all();  // for debugging: force an update
                break;    // right
            case 39:
                break;
            case 38:      // up
                if (todo.curr_row > 0) {
                    todo.curr_row--;
                    window.scrollBy(0,-20);
                    // window.scrollTo(window.outerWidth/ 2, 45 + (todo.curr_row/todo.todo_data.length * window.outerHeight));
                d3.event.preventDefault();
                }
                break;

            case 40:      // down
                if (todo.curr_row < todo.todo_data.length)
                    todo.curr_row++;
                d3.event.preventDefault();
                window.scrollBy(0,20);
                break;
        }
        todo.update_all();
    });
}

todo.update_td_html = function(d, p) {
    if ( todo.col_count++ > 3 ) { //number of columns
        todo.col_count = 0;
    }
    if (todo.col_count == 0) {
        if ( p == todo.clicked){
            console.log("yes, " + p);
        }
        todo.datarow = d
    }
    // if (typeof(d) == "boolean")
    switch (todo.col_count) {
        case 0:  // ID
            return d;
        case 1:  // Done
            return("<input type='checkbox'" + ( d ? " checked />" : "/>"));
        case 2:  // Priority
            if (todo.clicked == todo.datarow) {    // edit mode
                return todo.create_select_pri(d);
            } else
                return d;
        case 3:  // Task
            if (todo.clicked == todo.datarow ) {
                // return ('<input id="toedit" onclick="focus()" type="text" value="' + d + '"/>');
                return ('<input id="toedit" type="text" value="' + d + '"/>');
            } else
                return d;
        case 4:  // Created
            if (todo.clicked == todo.datarow) {
                return ('<input type="text" value="' + d + '"/>');
            } else
                return d;
        }
};

todo.editcell = function(id) {
    document.getElementById('toedit').focus();
    document.getElementById('toedit').select()
}

todo.update_all = function() {
    todo.td_table.selectAll("tr")
            .data(todo.todo_data)
            .classed("myhighlight", function(d,i) {
                 // console.log("i == " + i + " curr_row = " + curr_row);
                 return todo.curr_row == i;
             });
    todo.rows.selectAll("td")
        .data(function(d, i) {
            return  [i, d._done, d._priority, d.task, d.creation_date];
        })
        .html(todo.update_td_html);
    // todo.status_msg(todo.todo_data[todo.curr_row].task);
}

todo.highlight = function(d, i) {
    todo.curr_row = i;
    todo.update_all()

}

todo.add_new = function() {
}

todo.status_msg=function(msg) {
    // msg = msg + "`"
    d3.select("#comms").text(msg);
}

todo.create_select_pri = function(selected){
    pris = ['A', 'B', 'C', 'D', 'E'];
    ret = '<select>';
    for (var i = 0; i < 4; i++) {
        if (selected == pris[i])
            ret += '<option selected value="' + pris[i] + '">' + pris[i] +'</option>';
        else
            ret += '<option value="' + pris[i] + '">' + pris[i] +'</option>';
    }
    return ret + "</select>";
}
todo.init();