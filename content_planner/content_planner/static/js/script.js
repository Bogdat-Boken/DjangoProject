document.addEventListener("DOMContentLoaded", () => {
    const mobileNav = document.querySelector(".mobile-nav");
    const burger = document.querySelector(".burger-menu");

    burger.addEventListener("click", () => {
        if (mobileNav.style.right === "0px") {
            mobileNav.style.right = "-100%";
        } else {
            mobileNav.style.right = "0px";
        }
    });

    // Закрытие мобильного меню при клике вне его
    document.addEventListener("click", (event) => {
        if (!mobileNav.contains(event.target) && !burger.contains(event.target)) {
            mobileNav.style.right = "-100%";
        }
    });
});
