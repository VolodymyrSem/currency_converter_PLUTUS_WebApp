// vars for setting options to <select> tag on pages, where it is needed to choose a currency
const from_currency_options = `
<option value='USD' selected="selected">USD - US Dollar</option>
<option value='EUR'>EUR - Euro</option>
<option value='CZK'>CZK - Czech Koruna</option>
<option value='UAH'>UAH - Hryvnia</option>
<option value='RUB'>RUB - Russian Ruble</option>
<option value='GBP'>GBP - Pound Sterling</option>
<option value='CAD'>CAD - Canadian Dollar</option>
<option value='ALL'>ALL - Lek</option>
<option value='AMD'>AMD - Armenian Dram</option>
<option value='AZN'>AZN - Azerbaijan Manat</option>
<option value='BAM'>BAM - Convertible Mark</option>
<option value='BGN'>BGN - Bulgarian Lev</option>
<option value='BYN'>BYN - Belarusian Ruble</option>
<option value='DKK'>DKK - Danish Krone</option>
<option value='GEL'>GEL - Lari</option>
<option value='HUF'>HUF - Forint</option>
<option value='ISK'>ISK - Iceland Krona</option>
<option value='MKD'>MKD - Denar</option>
<option value='MDL'>MDL - Moldovan Leu</option>
<option value='NOK'>NOK - Norwegian Krone</option>
<option value='PLN'>PLN - Zloty</option>
<option value='RON'>RON - Romanian Leu</option>
<option value='RSD'>RSD - Serbian Dinar</option>
<option value='SEK'>SEK - Swedish Krona</option>
<option value='CHF'>CHF - Swiss Franc</option>
<option value='TRY'>TRY - Turkish Lira</option>
`;

const to_currency_options = `
    <option value='USD'>USD - US Dollar</option>
    <option value='EUR' selected="selected">EUR - Euro</option>
    <option value='CZK'>CZK - Czech Koruna</option>
    <option value='UAH'>UAH - Hryvnia</option>
    <option value='RUB'>RUB - Russian Ruble</option>
    <option value='GBP'>GBP - Pound Sterling</option>
    <option value='CAD'>CAD - Canadian Dollar</option>
    <option value='ALL'>ALL - Lek</option>
    <option value='AMD'>AMD - Armenian Dram</option>
    <option value='AZN'>AZN - Azerbaijan Manat</option>
    <option value='BAM'>BAM - Convertible Mark</option>
    <option value='BGN'>BGN - Bulgarian Lev</option>
    <option value='BYN'>BYN - Belarusian Ruble</option>
    <option value='DKK'>DKK - Danish Krone</option>
    <option value='GEL'>GEL - Lari</option>
    <option value='HUF'>HUF - Forint</option>
    <option value='ISK'>ISK - Iceland Krona</option>
    <option value='MKD'>MKD - Denar</option>
    <option value='MDL'>MDL - Moldovan Leu</option>
    <option value='NOK'>NOK - Norwegian Krone</option>
    <option value='PLN'>PLN - Zloty</option>
    <option value='RON'>RON - Romanian Leu</option>
    <option value='RSD'>RSD - Serbian Dinar</option>
    <option value='SEK'>SEK - Swedish Krona</option>
    <option value='CHF'>CHF - Swiss Franc</option>
    <option value='TRY'>TRY - Turkish Lira</option>
    `;

$(Document).ready(function () {
    $('.select-two').select2({
        width: '100%',
});
});

