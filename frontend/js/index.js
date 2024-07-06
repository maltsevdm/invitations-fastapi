function sendToBackend () {
    const data = {}
    const checkboxAcceptYes = document.getElementById("accept-yes")
    const checkboxAcceptNo = document.getElementById("accept-no")    
    if (checkboxAcceptNo.checked) {
        data['accept'] = false
    } else if (checkboxAcceptYes.checked) {
        data['accept'] = true
    } else {
        alert("Ответьте, будете ли вы присутствовать")
        return
    }

    const checkboxChildrenYes = document.getElementById("children-yes")
    const checkboxChildrenNo = document.getElementById("children-no") 
    
    if (checkboxChildrenNo.checked) {
        data['children'] = false
    } else if (checkboxChildrenYes.checked) {
        data['children'] = true
    }

    const checkboxes = document.querySelectorAll('[id^="drinks-"]');
    const checkboxNotDrink = document.getElementById("drinks-Не-пью")

    if (checkboxNotDrink.checked) {
        data['drinks'] = ["Не пью"]
    } else {
        data['drinks'] = []
        checkboxes.forEach(function (el) {
            if (el.id != "drinks-Не-пью" && el.checked == true) {
                const answer = el.id.split("-").slice(1).join(" ")
                data['drinks'].push(answer)
            }
        })
    }

    const comment = document.getElementById("inputComment") 
    data['comment'] = comment.value
    
    const arr = document.URL.split('/')
    data['id'] = arr[arr.length - 1]

    var req = new XMLHttpRequest();
    req.open("POST", "/send_to_tg?password=123", false);
    req.setRequestHeader("Content-Type", "application/json");
    req.send(JSON.stringify(data));

    alert("Спасибо за ответ!")
}

function handlerCheckboxesAccept (answer) {
    const checkboxYes = document.getElementById("accept-yes")
    const checkboxNo = document.getElementById("accept-no")
    if (answer == "yes" && checkboxNo.checked) {
        checkboxNo.checked = false
    }
    if (answer == "no" && checkboxYes.checked) {
        checkboxYes.checked = false
    }
}

function handlerCheckboxesChildren (answer) {
    const checkboxYes = document.getElementById("children-yes")
    const checkboxNo = document.getElementById("children-no")
    if (answer == "yes" && checkboxNo.checked) {
        checkboxNo.checked = false
    }
    if (answer == "no" && checkboxYes.checked) {
        checkboxYes.checked = false
    }
}

function handlerCheckboxesDrinks (answer) {
    const checkboxes = document.querySelectorAll('[id^="drinks-"]');
    const checkboxNotDrink = document.getElementById("drinks-Не-пью")

    if (answer == "no" && checkboxNotDrink.checked) {
        checkboxes.forEach(function (el) {
            if (el.id != "drinks-Не-пью") {
                el.checked = false
            }
        })
    }
    if (answer == "yes") {
        checkboxNotDrink.checked = false
    }
}