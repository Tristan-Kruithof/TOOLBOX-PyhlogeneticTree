const slider = document.getElementById('myslider');
const previewBox = document.getElementById('preview-box');

slider.addEventListener('change', () => {

    const sliderValue = slider.value;

    fetch(`/live_preview?slider_value=${sliderValue}`)

        .then(function (response) {

            return response.text()
        })

        .then(function (htmlData) {

            previewBox.innerHTML = htmlData;
        });


})


