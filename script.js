const themeToggle = document.querySelector("#themeToggle");
const printResume = document.querySelector("#printResume");
const filterButtons = document.querySelectorAll(".filter");
const projectCards = document.querySelectorAll(".project-card");
const year = document.querySelector("#year");
const hero = document.querySelector(".hero");

year.textContent = new Date().getFullYear();

const savedTheme = localStorage.getItem("portfolio-theme");
if (savedTheme === "dark") {
  document.body.classList.add("dark");
}

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  localStorage.setItem(
    "portfolio-theme",
    document.body.classList.contains("dark") ? "dark" : "light"
  );
});

if (printResume) {
  printResume.addEventListener("click", () => {
    window.print();
  });
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;

    filterButtons.forEach((item) => item.classList.remove("active"));
    button.classList.add("active");

    projectCards.forEach((card) => {
      const shouldShow = filter === "all" || card.dataset.category === filter;
      card.classList.toggle("is-hidden", !shouldShow);
    });
  });
});

const updateHeroArtwork = () => {
  if (!hero) return;

  const progress = Math.min(Math.max(window.scrollY / Math.max(hero.offsetHeight, 1), 0), 1);
  hero.style.setProperty("--hero-art-y", `${Math.round(progress * 70)}px`);
};

updateHeroArtwork();
window.addEventListener("scroll", updateHeroArtwork, { passive: true });
