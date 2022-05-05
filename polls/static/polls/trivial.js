function urlclipboard() {
    var copyText = document.querySelector(".share-url")

    navigator.clipboard.writeText(copyText.textContent);
}