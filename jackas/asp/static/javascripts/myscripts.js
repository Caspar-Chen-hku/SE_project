
var totalWeight = 0.0;
var currentOrder = {};
var maxWeight = 25.0;

function initiateVar(){
    totalWeight = 0.0;
    currentOrder = {};
    maxWeight = 25.0;

}

function updateVar(itemid, quantity){
        if (document.getElementById("totalWeight").value > maxWeight){
            document.getElementById("warning").innerHTML = "Order too heavy!";
        }else{ 
            document.getElementById("warning").innerHTML = "";
        }
        currentOrder[itemid] = quantity;    
}

function updateOrder(itemid, itemweight, quantity){
    exist = false;
    for (key in currentOrder){
        if (key==itemid){
            exist = true; break;
        }
    }
    quant = parseInt(quantity);
    itemwei = parseInt(itemweight);
    if (exist){
        totalWeight += itemwei * (quant - currentOrder[itemid])
        document.getElementById("totalWeight").value = totalWeight;  
        updateVar(itemid,quant); 
        if (quant==0){
            delete currentOrder[itemid];
        }    
    } else {
        totalWeight += itemwei * quant;
        document.getElementById("totalWeight").value = totalWeight;
        console.log("totalWeight: "+totalWeight);
        console.log("maxWeight: "+maxWeight);
        updateVar(itemid,quant);
    }
    console.log(currentOrder);
}

function constructOrder(userid){
    if (document.getElementById("totalWeight").value > maxWeight){
        return;
    }
    new_priority = document.getElementById("priority_list").value;
    $("construct").click(function(){
    $.post("clinic_manager/"+userid+"/construct_order", {neworder: currentOrder, weight: totalWeight, priority: new_priority}, function(result){
    });
});
}