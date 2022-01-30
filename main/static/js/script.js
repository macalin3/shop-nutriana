document.getElementById("logIn").onclick= function () {
    location.href='/log-in';
}

function togglePopup() {
    document.getElementById("popup-1")
    .classList.toggle("active");
}


function togglePopupSignUp() {
    document.getElementById("popup-2")
    .classList.toggle("active");
}


// quotes api
const api_url ="https://zenquotes.io/api/quotes/";

async function getapi(url)
{
    const response = await fetch(url);
    var data = await response.json();
    console.log(data);
}

getapi(api_url);
