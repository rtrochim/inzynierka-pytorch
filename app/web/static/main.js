function init() {
    drawBoard()
    document.querySelector("#action-choice").value = ''
    let button = Object.assign(document.createElement("button"), {className: 'list-group-item list-group-item-action'});
    button.innerHTML = 'start';
    button.onclick = function () {
        document.querySelector("#action-choice").value = button.innerHTML;
        execute_action()
    };
    document.querySelector("#hint").appendChild(button);
    document.querySelector("#button-execute").disabled = true;

}

function validate_input() {
    let actions = document.querySelector("#actions").childNodes;
    let value = document.querySelector("#action-choice").value;
    for (let i = 0; i < actions.length; i++) {
        if (actions[i].value !== value) {
            document.querySelector("#button-execute").disabled = true;
        } else {
            document.querySelector("#button-execute").disabled = false;
            break;
        }
    }
}

function execute_action() {
    document.querySelector("#button-execute").disabled = true;
    let data = {'command': document.querySelector("#action-choice").value}
    sendData(data).then(data => {
        update(data)
    })
}

async function sendData(data) {
    const response = await fetch(location.origin, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });
    return response.json();
}

function update(data) {
    let actions = data['actions']
    let state = data['state']

    let board = state[0]
    let bar = state[1]
    let off = state[2]

    document.querySelector("#log").value = document.querySelector("#log").value + '\n' + data['message']
    document.querySelector("#action-choice").value = ''
    document.querySelector("#hint").innerHTML = ''
    let options = ''
    actions.forEach(action => {
        let moves = 'move '
        if (Array.isArray(action)) {
            action.forEach(move => {
                moves += '(' + move.join('/') + ')';
                moves += ','
            });
            options += '<option value="' + moves.slice(0, -1) + '" />';

            let button = Object.assign(document.createElement("button"), {className: 'list-group-item list-group-item-action'});

            button.innerHTML = moves.slice(0, -1);
            button.onclick = function () {
                document.querySelector("#action-choice").value = button.innerHTML;
                execute_action()
            };
            document.querySelector("#hint").appendChild(button);

        } else {
            options += '<option value="' + action + '" />';

            let button = Object.assign(document.createElement("button"), {className: 'list-group-item list-group-item-action'})
            button.innerHTML = action;
            button.onclick = function () {
                document.querySelector("#action-choice").value = button.innerHTML;
                execute_action()
            };
            document.querySelector("#hint").appendChild(button);
        }
    });
    document.querySelector("#actions").innerHTML = options;

    let log = document.querySelector("#log");
    log.scrollTop = log.scrollHeight;

    drawAllCheckers(board, bar, off)
}


let input = document.querySelector("#action-choice");
input.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.querySelector("#button-execute").click();
    }
});