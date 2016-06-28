function load_tables() {

    editableGrid1 = new EditableGrid("Assignments"); 
    editableGrid1.tableLoaded = function() { this.renderGrid("assigns", "testgrid grid-assigns table table-bordered"); };
    editableGrid1.loadJSON("data/example_assign.json");    

    editableGrid2 = new EditableGrid("Jobs"); 
    editableGrid2.tableLoaded = function() { this.renderGrid("jobs", "testgrid grid-jobs table table-bordered"); };
    editableGrid2.loadJSON("data/example_jobs.json");

    editableGrid3 = new EditableGrid("Users"); 
    editableGrid3.tableLoaded = function() { this.renderGrid("users", "testgrid grid-users table table-bordered"); };
    editableGrid3.loadJSON("data/example_users.json");

}

function sendGrid(urlName) {
    curGrid = editableGrid1;
    obj1 = exportGrid(editableGrid1);
    obj2 = exportGrid(editableGrid2);
    obj3 = exportGrid(editableGrid3);
    obj = {"assigns": obj1, "jobs": obj2, "users": obj3};
    // $('#output').html(JSON.stringify(obj, null, "\t"));

    $.ajax({
        type: "POST",
        url: urlName,
        data: JSON.stringify(obj),
        contentType: 'application/json',
        dataType: 'json',
        error: function(data) {
            console.log(data);
        },
        success: function(data) {
            console.log(data);
        }
    });
}

function doValidate() {
    sendGrid("/validate");
}

function doOptimize() {
    sendGrid("/optimize");
}

function exportGrid(curGrid) {
    var obj = [];
    for (i = 0; i < curGrid.getRowCount(); i++) { 
        obj.push(curGrid.getRowValues(i));
    }
    return obj;
}

$( document ).ready(function() {

    load_tables();
    $('#validate').click(doValidate);
    $('#optimize').click(doOptimize);

});
