let soundplaying = false;
async function onScanSuccess(decodedText, decodedResult) {
    playAudio();

    await new Promise(r => setTimeout(r, 1000));

    let my_dict2 = JSON.parse(decodedText);
    // Get data from QR code
    // Dictionary data must match the names of the fields in the HTML form
    for(const key in my_dict2) {
        document.getElementById(key).value = my_dict2[key];
    }

    const auto_submit_box = document.getElementById('auto_submit')

    if(auto_submit_box.checked) {
        document.getElementById('myForm').submit();
    }
}

function clearForm() {
    let formElements = document.getElementsByTagName('input');
    for(i=0;i<formElements.length;i++) {
        if(formElements[i].type === 'text') {
            formElements[i].value='';
        }
    }
}

function playAudio() {
    var audio = new Audio("/static/elegant-notification-sound.mp3");
    if(!soundplaying) {
        audio.play();
        soundplaying = true;
    }
}

let html5QrcodeScanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 300 });
    html5QrcodeScanner.render(onScanSuccess);