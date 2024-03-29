
var totalWeight = 0.0;
var currentOrder = {};
var weights = {};
var maxWeight = 23.8;
var currentCat = "";

function constructOrder(userid){

    if (totalWeight<0.1){
        document.getElementById("warning").innerHTML = "No item chosen!";
        return;
    }else if (totalWeight>maxWeight){
        document.getElementById("warning").innerHTML = "Order too heavy!";
        return;
    }
    num_order = Object.keys(currentOrder).length;
    priority = document.getElementById("priority_list").value;

    weightIncludingContainer = totalWeight + 1.2;
    myform = $('<form action="/asp/clinic_manager/construct_order" method="GET"/>')
        .append($('<input type="hidden" name="num" value=' + num_order + '>'))
        .append($('<input type="hidden" name="weight" value=' + weightIncludingContainer + '>'))
        .append($('<input type="hidden" name="priority" value=' + priority + '>'))
        .append($('<input type="hidden" name="user" value=' + userid + '>'));

        var i = 0;
        for (key in currentOrder){
            myform.append($('<input type="hidden" name="item'+i+'" value='+ key + '>'))
                  .append($('<input type="hidden" name="item'+i+'num" value='+ currentOrder[key] + '>'));
            i++;
        }

        myform.appendTo($(document.body)) //it has to be added somewhere into the <body>
              .submit();
}

function initiateVar(userid, cat_name){
    categories = document.getElementById("category_list").childNodes;
    for (cat in categories){
        if (cat.childNodes[0].innerHTML==cat_name){
            cat.style.backgroundColor = "#bbbbbb";
        }else{
            cat.style.backgroundColor = "#eeeeee";
        }
    }
}

function calculateTotalWeight(){
    w = 0.0;
    for (key in currentOrder){
        w += currentOrder[key] * weights[key];
    }
    return parseFloat(w.toFixed(2));
}

function updateVar(itemid, quantity){
        currentOrder[itemid] = quantity; 
        totalWeight = calculateTotalWeight();
        console.log("totalWeight:"+totalWeight);
        document.getElementById("totalWeight").value = totalWeight;
        if (document.getElementById("totalWeight").value > maxWeight){
            document.getElementById("warning").innerHTML = "Order too heavy!";
        }else{ 
            document.getElementById("warning").innerHTML = "";
        }
        console.log("updated");   
}

function updateOrder(itemid, itemweight, quantity){
    console.log("maxWeight: "+maxWeight);
    exist = false;
    for (key in currentOrder){
        if (key==itemid){
            exist = true; break;
        }
    }
    quant = quantity;
    itemwei = itemweight;
    console.log("quant"+quant);
    console.log("itemwei"+itemwei);
    if (exist){
        console.log("exists");

        updateVar(itemid,quant); 
        if (quant==0){
            delete currentOrder[itemid];
        }    
    } else {
        console.log("doesnt exist");
        newweight =  itemwei * quant;
        weights[itemid] = itemwei;
        updateVar(itemid,quant);
    }
}