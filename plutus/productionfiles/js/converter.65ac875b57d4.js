// function to insert options to currency lists and set values of input fields if are passed from backend
function converter() {
    document.getElementById("from_currency").innerHTML = from_currency_options;
    document.getElementById("to_currency").innerHTML = to_currency_options;

    if (amount) {
    document.getElementById("amount").value = amount;
    document.getElementById("from_currency").value = from_currency;
    document.getElementById("to_currency").value = to_currency;
    };

    document.getElementById("from_currency__double").innerHTML = from_currency_options;
    document.getElementById("to_currency__double").innerHTML = to_currency_options;

    if (amount__double) {
    document.getElementById("amount__double").value = amount__double;
    document.getElementById("from_currency__double").value = from_currency__double;
    document.getElementById("to_currency__double").value = to_currency__double;
    };

    document.getElementById("payment__system").innerHTML = `
    <option value='MC'>MasterCard</option>
    <option value='VISA'>VISA</option>
    `;

    if (payment_system) {
    document.getElementById("payment__system").value = payment_system;
    }
}

function amountFocus() {
document.getElementById("amount").focus();
}

function amountDouble() {
document.getElementById("amount__double").focus();
}

function fromCurrency() {
document.getElementById("from_currency").focus();
}