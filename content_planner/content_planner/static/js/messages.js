document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        document.querySelectorAll(".message").forEach(msg => msg.style.display = "none");
    }, 3000);
});
