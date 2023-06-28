// function to automatically add ids and names in tags for saved pairs
function addIds() {
    let i = 1;

    // process saved pairs only if there are any
    if (number_of_saved_pairs != 0) {
        // get an array of all saved pairs
        const saved_pairs = document.getElementById('saved_pairs_content').children;

        // iterate through every pair and change ids and names of tags
        for (i; i < saved_pairs.length; i++) {
            saved_pairs[i].id = `${i}`;
            saved_pairs[i].children[0].children[0].id = `amount${i}`;
            saved_pairs[i].children[1].id = `result${i}`;
            saved_pairs[i].children[2].id = `from_currency${i}`;
            saved_pairs[i].children[3].id = `to_currency${i}`;
            saved_pairs[i].children[4].id = `delete_pair${i}`;
            saved_pairs[i].children[0].children[0].name = `amount${i}`;
            saved_pairs[i].children[1].name = `result${i}`;
            saved_pairs[i].children[2].name = `from_currency${i}`;
            saved_pairs[i].children[3].name = `to_currency${i}`;
            saved_pairs[i].children[4].name = `delete_pair${i}`;
        }
    } else {
        // change the default pair's id and content
        document.getElementById('default-pair').id = '1';
        document.getElementById('from_currency1').innerHTML = from_currency_options;
        document.getElementById('to_currency1').innerHTML = to_currency_options;

        document.getElementById('from_currency1').value = 'USD';
        document.getElementById('to_currency1').value = 'EUR';

        i++;
    }
    // alert('done with saved_pairs');

    // store a previous value of i in a new variable (current number of rows)
    number_of_rows = i - 1;

    // update value of the button for posting the form to get number of rows on backend
    document.getElementById("add_pairs").value = `${number_of_rows}`;

    // increment number of rows to set an id of div tag of the next pair
    number_of_rows++;

    // set id of the next new row to process a next row, which user will add
    document.getElementById('first').id = `${number_of_rows}`;
    // alert(`number of rows = ${localStorage.getItem('number_of_rows')}`)
}

function addNewRow() {
    // get an element to fill it with a new row
    let element = document.getElementById(`${number_of_rows}`);
    // alert(`number of rows = ${number_of_rows}`);
    // alert(`element = ${element}`);

    // add all tags inside the element
    element.innerHTML = `
    <div class="newPairs__item-amount">
    <input class="pair__row-input" type="number" id="amount${number_of_rows}" name="amount${number_of_rows}" step="0.01" value="1">
    </div>
    <select name="from_currency${number_of_rows}" id="from_currency${number_of_rows}" class="select-two">
    </select>
    <select name="to_currency${number_of_rows}" id="to_currency${number_of_rows}" class="select-two">
    </select>
    <button type="button" id="delete_pair${number_of_rows}" class="btn" onclick="deletePair()">Delete pair</button>
    </div>
    `;

    // add options to lists of currencies
    document.getElementById(`from_currency${number_of_rows}`).innerHTML = from_currency_options;
    document.getElementById(`to_currency${number_of_rows}`).innerHTML = to_currency_options;

    // update value of the button for posting the form to get number of rows on backend
    document.getElementById("add_pairs").value++;

    // update number of rows to set the next id
    number_of_rows++;

    // insert new div tag for the next pair
    element.insertAdjacentHTML('afterend', `
    <div id="${number_of_rows}" class="newPairs__item">
    </div>
    `);

    // refresh onclick action for a button to add a new row
    let button = document.getElementById("button");
    button.onclick = addNewRow;

    $('.select-two').select2({
        width: '100%',
    });
}

// function to delete a pair -> is done by hiding that pair and setting it's amount value to 0
function deletePair() {
    // get element (button), which was activated to delete a pair, to know, which pair is needed to delete
    let element = deletePair.caller.arguments[0].target;

    // set it's visibility to none and change it's amount to 0
    element.parentElement.style.display = 'none';
    element.parentElement.firstElementChild.firstElementChild.setAttribute('value', '0');

    // alert(element.parentElement.firstElementChild.getAttribute('value'));
}
