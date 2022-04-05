const getRoom = async () => {
    const response = await fetch('', {
        method: 'POST',
        body: JSON.stringify({}), // string or object
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const myJson = await response.json(); //extract JSON from the http response
    if (myJson.is_open) {
        window.location.pathname = '/chat/' + myJson.name + '/';
    }
    // do something with myJson
}

document.querySelector('#chat-now').onclick = function (e) {
    document.getElementById('js-default').classList.add('d-none');
    document.getElementById('js-waiting').classList.remove('d-none');
    setInterval(getRoom, 1000);
};
