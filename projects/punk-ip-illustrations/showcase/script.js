(() => {
  'use strict';

  const initTabs = (root, tabSelector, panelSelector) => {
    if (!root) return;
    const tabs = Array.from(root.querySelectorAll(tabSelector));
    const panels = Array.from(root.querySelectorAll(panelSelector));
    if (!tabs.length || !panels.length) return;

    const activate = (nextTab, moveFocus = false) => {
      tabs.forEach((tab) => {
        const selected = tab === nextTab;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        const panel = root.querySelector(`#${tab.getAttribute('aria-controls')}`);
        if (panel) panel.hidden = !selected;
      });
      if (moveFocus) nextTab.focus();
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', (event) => {
        let nextIndex = index;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') nextIndex = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') nextIndex = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === 'Home') nextIndex = 0;
        else if (event.key === 'End') nextIndex = tabs.length - 1;
        else return;
        event.preventDefault();
        activate(tabs[nextIndex], true);
      });
    });

    const selected = tabs.find((tab) => tab.getAttribute('aria-selected') === 'true') || tabs[0];
    activate(selected);
  };

  initTabs(document.querySelector('[data-layer-explorer]'), '[role="tab"]', '.layer-panel');
  initTabs(document.querySelector('[data-roadmap]'), '[role="tab"]', '.roadmap-panel');

  const scenarioRoot = document.querySelector('[data-scenario-filter]');
  if (scenarioRoot) {
    const buttons = Array.from(scenarioRoot.querySelectorAll('[data-filter]'));
    const cards = Array.from(scenarioRoot.querySelectorAll('[data-category]'));
    const status = scenarioRoot.querySelector('[data-filter-status]');

    const applyFilter = (filter) => {
      let visible = 0;
      cards.forEach((card) => {
        const match = filter === 'all' || card.dataset.category === filter;
        card.classList.toggle('is-filtered', !match);
        card.setAttribute('aria-hidden', String(!match));
        if (match) visible += 1;
      });
      buttons.forEach((button) => {
        button.setAttribute('aria-pressed', String(button.dataset.filter === filter));
      });
      if (status) status.textContent = `当前显示 ${visible} 个场景`;
    };

    buttons.forEach((button) => {
      button.addEventListener('click', () => applyFilter(button.dataset.filter));
    });
    applyFilter('all');
  }
})();
