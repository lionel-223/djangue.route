document.querySelectorAll(".locale-number").forEach(e => {
    let text = e.innerText;
    let to_float = Number(text);
    // TODO: Use lang from current user
    e.innerText = isNaN(to_float) ? text : to_float.toLocaleString("fr");
});
