const admin_box = document.getElementById('admin_box');
const admin_check = document.getElementById('admin_check');
const admin_pass = document.getElementById('admin_pass');

admin_check.addEventListener('change', () => {

    if (admin_check.checked) {
        admin_box.style.display = 'block';
        admin_pass.required = true;
    }
    else {
        admin_pass.required = false;
        admin_box.style.display = 'none';
    }
});