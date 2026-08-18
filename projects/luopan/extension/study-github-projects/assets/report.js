(() => {
  document.documentElement.classList.add("js");

  const viewButtons = [...document.querySelectorAll("[data-set-view]")];
  const viewSections = [...document.querySelectorAll("[data-view-scope]")];
  const setView = (view) => {
    viewButtons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.setView === view)));
    viewSections.forEach((section) => {
      const scopes = section.dataset.viewScope.split(" ");
      section.hidden = view !== "all" && !scopes.includes(view);
    });
    document.body.dataset.activeView = view;
  };
  viewButtons.forEach((button) => button.addEventListener("click", () => setView(button.dataset.setView)));

  const filterButtons = [...document.querySelectorAll("[data-cap-filter]")];
  const capabilityCards = [...document.querySelectorAll("[data-cap-status]")];
  filterButtons.forEach((button) => button.addEventListener("click", () => {
    const filter = button.dataset.capFilter;
    filterButtons.forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
    capabilityCards.forEach((card) => { card.hidden = filter !== "all" && card.dataset.capStatus !== filter; });
    const count = capabilityCards.filter((card) => !card.hidden).length;
    const region = document.getElementById("filter-status");
    if (region) region.textContent = `已显示 ${count} 项能力`;
  }));

  setView("all");
})();
