const log = (sender, message) => {
    // Get the ul element that is a child of the .terminal div
    const terminalUl = document.querySelector('.terminal > ul');
    const newLi = document.createElement('li');
    newLi.textContent = `[${sender}]    \t` + message;
    terminalUl.appendChild(newLi);
}

const config = {
    position: 'start'
}
var board
var boardWorking = false
var currentMove = "NA"
function create_board() {
    board = Chessboard2('myBoard', config)
    boardWorking = true
}

var socket = io.connect(document.URL);
log("web","connecting...")

socket.on('connect', () => {
    log(".io",'connected!');
});

socket.on('message', (data) => {
    data = JSON.parse(data)
    log(data[0], data[1])
    const img = document.getElementById(data[1]);
    if(img)
        img.src = 'data:image/jpeg;base64,' + data[2];
    else {
        log(data[0],"checkeddd")
        split = data[1].split(" O-O ")
        if(split.length > 1) {
            log("CASTLING", data[1])
            board.move(split[0])
            board.move(split[1])
        } else {
            log("MOVING",data[1])
            board.move(data[1])
        }
        currentMove = data
    }
})

       

addEventListener("keypress", (event) => {
    switch (event.key) {
        case "Enter":
            log("web","requesting next frame")
            socket.emit("client_message", "NEXT")
            break
        case "q":
            log("web","requesting halt")
            socket.emit("client_message", "HALT")
            break
    }
});

// socket.on('message', (data) => {
        //     document.querySelector("#timestamp").innerHTML = Date.now();
        //     // console.log("message!!")
        //     // console.log(data)
        //     socket.emit("message",data)
        //     if(boardWorking && data != currentMove && data != "NA") {
        //         console.log(data)
        //         split = data.split(" O-O ")
        //         if(split.length > 1) {
        //             console.log("castling!!! " + data)
        //             board.move(split[0])
        //             board.move(split[1])
        //         } else {
        //             console.log("making move!!! " + data)
        //             board.move(data)
        //         }
        //         currentMove = data
        //     }
        // });

