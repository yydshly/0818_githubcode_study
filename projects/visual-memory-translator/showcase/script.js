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

document.querySelectorAll('[data-extension-lab]').forEach((lab) => {
  const tabs = Array.from(lab.querySelectorAll('.lab-tabs [role="tab"]'));
  const panels = tabs.map((tab) => document.getElementById(tab.getAttribute('aria-controls')));

  const activate = (nextTab, moveFocus = false) => {
    tabs.forEach((tab, index) => {
      const selected = tab === nextTab;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      panels[index].hidden = !selected;
      if (!selected) panels[index].dispatchEvent(new CustomEvent('panelhidden'));
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

document.querySelectorAll('[data-emotion-module]').forEach((module) => {
  const time = module.querySelector('[data-time-range]');
  const feeling = module.querySelector('[data-feeling-range]');
  const stage = module.querySelector('.emotion-stage');
  const timeOutput = module.querySelector('[data-time-output]');
  const feelingOutput = module.querySelector('[data-feeling-output]');
  const detail = module.querySelector('[data-detail-value]');
  const abstraction = module.querySelector('[data-abstraction-value]');
  const copy = module.querySelector('[data-copy-value]');
  const title = module.querySelector('[data-emotion-title]');
  const note = module.querySelector('[data-emotion-note]');

  const update = () => {
    const age = Number(time.value);
    const intensity = Number(feeling.value);
    stage.style.setProperty('--age', age);
    stage.style.setProperty('--feeling', intensity);
    timeOutput.value = age < 34 ? '刚刚发生 · 事实清晰' : age < 68 ? '已有距离 · 只留主线' : '很久以前 · 接近印象';
    feelingOutput.value = intensity < 34 ? '安静 · 保持克制' : intensity < 68 ? '有余温 · 增加强调' : '强烈 · 主体更靠前';
    detail.textContent = `${Math.max(12, Math.round(88 - age * .68))}%`;
    abstraction.textContent = age < 30 ? 'low' : age < 72 ? 'high' : 'extreme';
    copy.textContent = age < 34 ? '贴近事实' : age < 68 ? '反思距离' : '一个隐喻';
    title.textContent = age < 34 ? '湖边，仍然清楚' : age < 68 ? '风把细节带走一些' : '只记得一条红色的线';
    note.textContent = intensity > 70
      ? '减少环境信息，让人物与强调色成为记忆中心。'
      : age > 67
        ? '不再复述地点，只保留人物比例、冷暖关系和停顿。'
        : '保留人物、地点和主要光线，只让边缘稍微退后。';
  };
  time.addEventListener('input', update);
  feeling.addEventListener('input', update);
  update();
});

document.querySelectorAll('[data-layer-module]').forEach((module) => {
  module.querySelectorAll('[data-layer-toggle]').forEach((toggle) => {
    const layer = module.querySelector(`[data-layer="${toggle.dataset.layerToggle}"]`);
    const update = () => layer.classList.toggle('is-hidden', !toggle.checked);
    toggle.addEventListener('change', update);
    update();
  });
});

document.querySelectorAll('[data-series-module]').forEach((module) => {
  const buttons = Array.from(module.querySelectorAll('[data-format]'));
  const stage = module.querySelector('[data-format-stage]');
  const activate = (button, moveFocus = false) => {
    buttons.forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
    stage.dataset.formatStage = button.dataset.format;
    if (moveFocus) button.focus();
  };
  buttons.forEach((button, index) => {
    button.addEventListener('click', () => activate(button));
    button.addEventListener('keydown', (event) => {
      let nextIndex = index;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') nextIndex = (index + 1) % buttons.length;
      else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') nextIndex = (index - 1 + buttons.length) % buttons.length;
      else if (event.key === 'Home') nextIndex = 0;
      else if (event.key === 'End') nextIndex = buttons.length - 1;
      else return;
      event.preventDefault();
      activate(buttons[nextIndex], true);
    });
  });
  activate(buttons[0]);
});

document.querySelectorAll('[data-motion-module]').forEach((module) => {
  const stage = module.querySelector('.motion-stage');
  const caption = module.querySelector('[data-motion-caption]');
  const status = module.querySelector('[data-motion-status]');
  const steps = Array.from(module.querySelectorAll('[data-motion-step]'));
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const labels = ['01 / 现实仍然完整', '02 / 选择要留下的线索', '03 / 照片被重新组织', '04 / 成为可收藏的余韵'];
  let current = 0;
  let timer = null;

  const render = () => {
    stage.dataset.motionStage = String(current);
    caption.textContent = labels[current];
    status.textContent = `停在第 ${current + 1} 阶段`;
    steps.forEach((step, index) => step.classList.toggle('active', index === current));
  };
  const pause = () => {
    window.clearInterval(timer);
    timer = null;
  };
  module.querySelector('[data-motion-action="play"]').addEventListener('click', () => {
    pause();
    if (reducedMotion.matches) {
      current = 3;
      render();
      status.textContent = '已按减少动态偏好直接显示最终阶段';
      return;
    }
    if (current === 3) current = 0;
    render();
    timer = window.setInterval(() => {
      current += 1;
      render();
      if (current >= 3) pause();
    }, 1050);
  });
  module.querySelector('[data-motion-action="pause"]').addEventListener('click', () => {
    pause();
    status.textContent = `已暂停在第 ${current + 1} 阶段`;
  });
  module.querySelector('[data-motion-action="reset"]').addEventListener('click', () => {
    pause();
    current = 0;
    render();
  });
  module.addEventListener('panelhidden', pause);
  render();
});

document.querySelectorAll('[data-voice-module]').forEach((module) => {
  const button = module.querySelector('[data-voice-start]');
  const steps = Array.from(module.querySelectorAll('[data-voice-step]'));
  const output = module.querySelector('[data-voice-output]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let timers = [];

  const clear = () => {
    timers.forEach(window.clearTimeout);
    timers = [];
  };
  const show = (count) => {
    steps.forEach((step, index) => {
      const active = index < count;
      step.classList.toggle('is-active', active);
      step.setAttribute('aria-current', index === count - 1 ? 'step' : 'false');
    });
    output.classList.toggle('is-active', count >= steps.length);
    button.textContent = count >= steps.length ? '重新演示' : `处理中 ${count}/${steps.length}`;
  };
  button.addEventListener('click', () => {
    clear();
    show(0);
    if (reducedMotion.matches) {
      show(steps.length);
      return;
    }
    steps.forEach((_, index) => {
      timers.push(window.setTimeout(() => show(index + 1), 420 * (index + 1)));
    });
  });
  module.addEventListener('panelhidden', clear);
  show(0);
  button.textContent = '演示处理链';
});
