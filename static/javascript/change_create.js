const selector = document.getElementById('calculator');
const imagebox = document.getElementById('imgbox');

selector.addEventListener('change', () => {

    const selectorValue = selector.value;

    fetch(`/home/create?selectorValue=${selectorValue}`)

        .then(function (response) {

            return response.text()
        })

        .then(function (htmlData) {
            imagebox.src = htmlData;
        });

})


