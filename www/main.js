async function onSearch() {
    results_div = $('#results');
    results_div.css('opacity', 0.5);
    results_div.empty()
    const query = $('#search-box').val()
    const res = await fetch(
        `/api/search?query=${encodeURI(query)}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    const j = await res.json()
    j['results'].forEach(e => {
        results_div.append(`<div class="search-item">${e}</div>`)
    });
    results_div.css('opacity', 1);
}

$(document).ready(() => {
    $('#search-button').on('click', onSearch);
})
