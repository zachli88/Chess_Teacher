const log = (sender, message) => {
    // Get the ul element that is a child of the .terminal div
    const terminal = document.querySelector(".terminal")
    const terminalUl = document.querySelector('.terminal > ul');
    const newLi = document.createElement('li');
    newLi.textContent = `[${sender}]    \t` + message;
    terminalUl.appendChild(newLi);
    terminal.scrollTop = terminal.scrollHeight;
}


const config = {
    draggable: true,
    mouseDraggable: 'true',
    dropOffBoard: 'snapback', // this is the default
    position: 'start'
}


var board
var move_reversed

function create_board() {
    board = Chessboard2('myBoard', config)
}


var socket = io.connect(document.URL);
log("web","connecting...")

socket.on('connect', () => {
    log(".io",'connected!');
});

socket.on('message', (data) => {
    data = JSON.parse(data)

    switch (data[0]) {
        case "cv2":
            const img = document.getElementById(data[1]);
            img.src = 'data:image/jpeg;base64,' + data[2];
        case "mov": 
            split = data[1].split(" O-O ")
            if (split.length > 1) {
                log("castle", data[1])
                log("split", split[0])
                log("split", split[1])
                board.move(split[0])
                board.move(split[1])
            } else {
                board.move(data[1])
            }
            break
        case "san":
            log(data[0], data[1])
            $("#san").text(data[1])
            break
        case "prb":
            $("#prb").text(Math.round(data[1]*100) + "% confidence")
            break
        case "cls":
            $(".terminal > ul").empty();
            board = Chessboard2('myBoard', config)
            log("web","connecting...")
            break
        default:
            log(data[0], data[1])
            break
    }



    // const img = document.getElementById(data[1]);
    // if(img)
    //     img.src = 'data:image/jpeg;base64,' + data[2];
    // else {
    //     split = data[1].split(" O-O ")
    //     switch (data[0]) {
    //         case "mov": 
    //             if (split.length > 1) {
    //                 log("castle", data[1])
    //                 board.move(split[0])
    //                 board.move(split[1])
    //             } else {
    //                 board.move(data[1])
    //             }
    //             break
    //         case "san":
    //             $("#san").text(data[1])
    //             break
    //         case "prb":
    //             $("#san").text(data[1])
    //             break
    //         case "cls":
    //             $(".terminal > ul").empty();
    //             log("web","connecting...")
    //     }
        

    //     currentMove = data
    // }
})

       

addEventListener("keydown", (event) => {
    switch (event.key) {
        case "]":
            log("web","requesting move")
            socket.emit("client_message", "NEXT")
            break
        case "q":
            log("web","requesting halt")
            socket.emit("client_message", "HALT")
            break
        case "m":
            log("web","requesting move")
            move = prompt("enter a move or your files will be deleted")
            socket.emit("client_message", "MOVE " + move)
            break
        case "[":
            // log("web","requesting undo")
            // socket.emit("client_message", "UNDO ")
            break
        default:
            log("key", event.key)
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

