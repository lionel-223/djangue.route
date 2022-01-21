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
