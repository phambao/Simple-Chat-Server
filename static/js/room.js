const roomName = JSON.parse(document.getElementById('room-name').textContent);
const userUUID = document.getElementById('user-uuid').value

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    showMessage(data);
    scrollChat();
};

chatSocket.onclose = function (e) {
    alert('Room is not exits.')
    window.location.pathname = '/chat/';
};

document.querySelector('#message').focus();
document.querySelector('#message').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        sendMessage();
    }
};

let sendMessage = function () {
    const messageInputDom = document.querySelector('#message');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'user_uuid': userUUID
    }));
    messageInputDom.value = '';
}

let showMessage = function (data) {
    const messageInputBox = document.querySelector('#show-message-box');

    let isOwner;
    if (data.user_uuid == userUUID) {
        isOwner = true;
    }
    messageInputBox.insertAdjacentHTML('beforeend', formMessage(data.message, isOwner));
}

let formMessage = function (message, isOwner) {
    let time = formatAMPM(new Date());
    if (isOwner) {
        return '<div class="chat darker"><p>' + message+ '</p><span class="time-left">' + time + '</span></div>'
    }

    return '<div class="chat"><p>' + message+ '</p><span class="time-right">' + time + '</span></div>'
}

let scrollChat = function () {
    const messageInputDom = document.getElementById('show-message-box');
    messageInputDom.scrollTop = messageInputDom.scrollHeight;
}

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}