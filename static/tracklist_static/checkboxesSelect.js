document.querySelector("table").addEventListener("click", ({
    target
}) => {
    // discard direct clicks on input elements
    if (target.nodeName === "INPUT") return;
    // get the nearest tr
    const tr = target.closest("tr");
    if (tr) {
        // if it exists, get the first checkbox
        const checkbox = tr.querySelector("input[type='checkbox']");
        if (checkbox) {
            // if it exists, toggle the checked property
            checkbox.checked = !checkbox.checked;
        }
    }
});