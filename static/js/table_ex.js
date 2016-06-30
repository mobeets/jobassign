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

function exportGrid(curGrid) {
    // console.log(curGrid);
    var obj = [];
    for (i = 0; i < curGrid.getRowCount(); i++) { 
        obj.push(curGrid.getRowValues(i));
    }
    return obj;
}

function sendGrid(urlName, successFcn) {
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
            successFcn(data);
        }
    });
}

function updateAssigns(data) {
    // assigns = [{u'SING': 0, u'RING': 3, u'SLEEP': 9, u'name': u'Frodo', u'WALK': 5}, ...]
    assigns = data["assigns"];
    rows = [];
    for (i = 0; i < assigns.length; i++) {
        rows.push({"id": i+1, "values": assigns[i]});
    }
    sheet = {"data": rows};
    // console.log("Updating...");
    // console.log(sheet);
    editableGrid1.update(sheet);
    // console.log("Updated. Maybe.");
}

function handleValidation(data) {
    console.log("I feel so validated.");
}

function doValidate() {
    sendGrid("/validate", handleValidation);
}

function doOptimize() {
    sendGrid("/optimize", updateAssigns);
}

$( document ).ready(function() {

    load_tables();
    $('#validate').click(doValidate);
    $('#optimize').click(doOptimize);

});
