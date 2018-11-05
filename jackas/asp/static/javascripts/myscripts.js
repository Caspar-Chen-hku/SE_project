
var totalWeight = 0.0;
var currentOrder = {};
var maxWeight = 25.0;
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

    myform = $('<form action="http://127.0.0.1:8000/asp/clinic_manager/construct_order" method="GET"/>')
        .append($('<input type="hidden" name="num" value=' + num_order + '>'))
        .append($('<input type="hidden" name="weight" value=' + totalWeight + '>'))
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


function constructOrder1(userid){
    console.log("clicked");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

        }
    };
    num_order = Object.keys(currentOrder).length;
    priority = document.getElementById("priority_list").value;

    request_str = "http://127.0.0.1:8000/asp/clinic_manager/construct_order?num="+num_order+"&weight="+totalWeight+"&priority="+priority+"&user="+userid;

    var i = 0;
    for (key in currentOrder){
        request_str += "&item"+i+"="+key + "&item"+i+"num"+"="+currentOrder[key];
    }

    xhttp.open("GET", request_str, true);
    xhttp.send();
}

function initiateVar(){
    totalWeight = 0.0;
    currentOrder = {};
    maxWeight = 25.0;
}

function changeColor(category){
    categories = document.getElementById("category_list").childNodes;
    for (cat in categories){
        if (cat.childNodes[0]==category){
            cat.style.backgroundColor = "#bbbbbb";
        }else{
            cat.style.backgroundColor = "#eeeeee";
        }
    }
    currentCat = category.innerHTML;
    document.getElementById("cat").innerHTML = currentCat;
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
        updateVar(itemid,quant);
    }
}