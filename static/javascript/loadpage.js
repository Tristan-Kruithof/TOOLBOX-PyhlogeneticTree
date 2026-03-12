async function loadPage(page) {
    title = await page.split('.')[0];
    document.title = title.charAt(0).toUpperCase() + title.slice(1);

    const page_to_load = await fetch(page);

    document.getElementById('frame_container').innerHTML = await page_to_load.text();

}

document.addEventListener('DOMContentLoaded', async() => {
    await loadPage('home.html');
    });