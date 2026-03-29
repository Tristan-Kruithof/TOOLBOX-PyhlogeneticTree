// The input field and add button for registering keystrokes
const input_field =  document.getElementById("species")
const add = document.getElementById("add")

// The selector
const selector = document.getElementById('input_method');

// Two wrapper divs for blocking and unblocking
const fasta = document.getElementById('input_fasta');
const common = document.getElementById('input_common');

// Two input fields for changing input required
const fasta_required = document.getElementById('multi_fasta_file');
const common_required = document.getElementById('species');

// Function to prevent default action and click the add button instead
function input_keypress(event) {
    if (event.key === "Enter") {
        event.preventDefault()
        add.click()
    }
}

// Function to toggle the input fields based on which is selected
function toggle_inputs(){
    const selectorValue = selector.value;
    console.log(selectorValue);

    if (selectorValue === 'common') {
        fasta.style.display = 'none';
        common.style.display = 'block';
        common_required.required = true;
        fasta_required.required = false;
    }
    else {
        fasta.style.display = 'block';
        common.style.display = 'none';
        common_required.required = false;
        fasta_required.required = true;

    }
}

// Run whenever a key is pressed within the input field
input_field.addEventListener('keypress', input_keypress)
// Run whenever the input on the document is changed
selector.addEventListener('change', toggle_inputs)
// Run on start of the loaded page
document.addEventListener("DOMContentLoaded", toggle_inputs);

