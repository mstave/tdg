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
    todo.td_table=d3.select("#todo_div").append("table").attr("id","main_table");
    // todo: create an array of column names and  use thead.data()
    todo.thead = todo.td_table.append("thead");

    todo.thead.append("th").text("ID").attr("id","th_id");
    todo.thead.append("th").text("X").attr("id","th_done");
    todo.thead.append("th").text("Pri").attr("id","th_pri");
    todo.thead.append("th").text("Task").attr("id","th_task");
    todo.thead.append("th").text("Created").attr("id","th_created");

    todo.rows = todo.td_table.selectAll("tr").data(todo.todo_data);
    todo.rows.enter().append("tr")
    todo.rows.exit().remove();

    todo.td = todo.rows.selectAll("td")
            .data(function(d, p) {
                d.gui_index = p 
                return  [p, d._done, d._priority, d.task, d.creation_date];
            })

    todo.td.enter().append("td")
            .html(todo.update_td_html)
            .on("change", todo.change_data );

    todo.td.exit().remove();
    todo.col_count = -1;
    todo.update_all();
}

todo.toggle_complete = function() {
        todo.todo_data[todo.curr_row]._done = !todo.todo_data[todo.curr_row]._done;
    }

    // todo.rows.on('mouseover', todo.highlight)
    // // todo fix this to test highlight prop
    // todo.rows.on('dblclick', function(d,i) {
    //     todo.clicked = i;
    //     // todo.update_all();    
    // });



// todo.pause_events = function() {
//     todo.rows.on('click', null);
//     todo.rows.on('mouseover', null);

//     d3.select("body").on('keydown',null);
//     console.log("Pausing events");
// }

todo.change_data = function (d, p) {
    //this.onclick=null;
    //todo.clicked=this.parentElement.rowIndex;
    todo.tempsave = todo.todo_data[todo.clicked];
    todo.update_data(todo.clicked, p, d3.event.target.value);
    d3.xhr("/json.up").header('content-type','application/json').post(JSON.stringify(todo.todo_data[todo.clicked]), function(error, data) {
    });
    todo.clicked = -1;
    todo.update_all();
}

todo.update_data = function(row, column, new_value) {
    switch (column) {
        case 1:  // Done
	    todo.toggle_complete();
	    break;
        case 2:  // Priority
	    todo.todo_data[row]._priority = new_value;
	    break;
        case 3:  // Task
	    todo.todo_data[row].task = new_value;
	    break;
	case 4:
	    todo.todo_data[row].creation_date = new_value;
	    break;
        }
}

var theevent = null;

// todo.unpause_events = function ()  {
//     console.log("Unpausing events");
    


todo.handle_key = function (d, i) {
    k = d3.event.keyCode;
    if  (k >= 65 && k <= 69) {
         todo.todo_data[todo.curr_row]._priority = String.fromCharCode(k);
    }
    var ignore_key = false;
    if (d3.event.target instanceof HTMLInputElement) { 
	return;
    }

    switch (k) {
        case 32:      // space
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
	default:
	     ignore_key = true;
	     break;
        }
	todo.clicked = -1;
        if (!ignore_key) {
	    todo.update_all();
	}
 }

todo.edit_click = function (d,f) {
    console.log("edit click");
    console.log(this);
    console.log(d);
    console.log(f);
    todo.update_all();
} 

todo.update_td_html = function(d, p) {
    if ( todo.col_count++ > 3 ) { //number of columns
        todo.col_count = 0;
    }
    if (todo.col_count == 0) {
        todo.datarow = d
    }

    switch (todo.col_count) {
        case 0:  // ID
            return '<button style="visbility:hidden" onclick="todo.delete_todo(' + d + ')" class="edit_button">Delete</button>' + "&nbsp;" +  d
        case 1:  // Done
            return("<input class='done_check' type='checkbox'" + ( d ? " checked />" : "/>"));
        case 2:  // Priority
            if (todo.clicked == todo.datarow) {    // edit mo/de
                return todo.create_select_pri(d);
            } else
                return d;
        case 3:  // Task
            if (todo.clicked == todo.datarow ) {
                // return ('<input id="toedit" onclick="focus()" type="text" value="' + d + '"/>');
                return ('<input type="text" size= ' + ( 10 + d.length) + ' value="' + d + '"/>');
            } else
                return d;
        case 4:  // Created
            if (todo.clicked == todo.datarow) {
                return ('<input size="11" type="date" value="' + d + '"/>');
            } else
                return d;
        }
};

todo.delete_todo = function(del_row) {
    var delval = "none";
    todo.clicked = del_row
    d3.xhr("/del/" + del_row).post(function(error,data) {
	todo.reload();
    });
   // setTimeout(todo.reload,5000);
//    location.reload(true);

}

todo.reload = function() {
    location.reload(true);
}

var zzz = 0;

todo.update_all = function() {
    
    d3.select("body").on('keydown',todo.handle_key);
    
    todo.td_table.selectAll("tr")
        .data(todo.todo_data)
	.on('mouseover', todo.highlight)
        .on('click', function(d,i) {
	    if (d3.event.target instanceof HTMLTableCellElement) {
	        todo.clicked = i;
		todo.update_all();
            }
	})
        .classed("myhighlight", function(d,i) {
             return todo.curr_row == i;
         });


    todo.rows.selectAll("td")
        .data(function(d, i) {
            return  [i, d._done, d._priority, d.task, d.creation_date];
        })
        .html(todo.update_td_html)
        .on("change", todo.change_data );
    
    todo.td_table.selectAll(".edit_button")
	.on("click", todo.edit_click);

    todo.td_table.selectAll(".edit_button")
        .classed("hide_button", function(d,i) {
    	        return todo.curr_row != i;
    	 });

    todo.td_table.selectAll("done_check")
        .on("change", todo.change_data );

}

todo.highlight = function(d, i) {
    if (todo.curr_row == i)
	return;
    todo.curr_row = i;
    todo.clicked = i;
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
