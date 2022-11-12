function onScanSuccess(decodedText, decodedResult) {
    let my_dict2 = JSON.parse(decodedText);

    // Get data from QR code
    // Dictionary data must match the names of the fields in the HTML form
    for(const key in my_dict2) {
        document.getElementById(key).value = my_dict2[key];
    }

    document.getElementById('myForm').submit();
}

let html5QrcodeScanner = new Html5QrcodeScanner(
	"reader", { fps: 10, qrbox: 250 });
html5QrcodeScanner.render(onScanSuccess);