document.querySelectorAll('[data-comparison]').forEach((comparison) => {
  const input = comparison.querySelector('input[type="range"]');
  const update = () => comparison.style.setProperty('--split', `${input.value}%`);
  input.addEventListener('input', update);
  update();
});

document.querySelectorAll('[data-scene-switcher]').forEach((switcher) => {
  const tabs = Array.from(switcher.querySelectorAll('[role="tab"]'));
  const panels = tabs.map((tab) => document.getElementById(tab.getAttribute('aria-controls')));

  const activate = (nextTab, moveFocus = false) => {
    tabs.forEach((tab, index) => {
      const selected = tab === nextTab;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      panels[index].hidden = !selected;
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
});
