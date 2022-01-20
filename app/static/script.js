window.onload = function() {
    document.querySelectorAll(".locale-number").forEach(e => {
        let text = e.innerText;
        let to_float = Number(text);
        // TODO: Use lang from current user
        e.innerText = isNaN(to_float) ? text : to_float.toLocaleString("fr");
    });

    const moderation_form = document.getElementById("moderation_form");
    if (moderation_form) {
        const letter_id = moderation_form.querySelector("input[name='letter_id']").value;
        document.querySelectorAll("a").forEach(e => {
            e.onclick = function() {
                fetch(`/admin/moderation/unlock_letter/${letter_id}`, {
                    method: "POST",
                    headers: {'Content-Type': 'application/json'}
                }).then();
            };
        });
    }

    const nav_toggle = document.getElementById("nav-toggle");
    const nav_menu = document.getElementById("nav-menu");
    nav_toggle.onclick = function() {
        nav_menu.classList.toggle("active");
    };
};

