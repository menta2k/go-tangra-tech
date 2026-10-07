/* Optional enhancements. Documentation and navigation work without this file. */
(() => {
  const toggle = document.querySelector('.search-toggle');
  const panel = document.getElementById('site-search');
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');
  const status = document.getElementById('search-status');
  let index;
  let request;
  if (toggle && panel) {
    toggle.hidden = false;
    const close = () => {
      panel.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    };
    toggle.addEventListener('click', () => {
      panel.hidden = !panel.hidden;
      toggle.setAttribute('aria-expanded', String(!panel.hidden));
      if (!panel.hidden) input.focus();
    });
    panel.addEventListener('keydown', event => {
      if (event.key === 'Escape') close();
    });
    input.addEventListener('input', async () => {
      const query = input.value.trim().toLowerCase();
      results.replaceChildren();
      status.textContent = '';
      if (!query) return;
      try {
        if (!request) request = fetch(panel.dataset.index).then(response => {
          if (!response.ok) throw new Error('Index unavailable');
          return response.json();
        });
        index = await request;
        if (query !== input.value.trim().toLowerCase()) return;
        const words = query.split(/\s+/);
        const hits = index.filter(page => words.every(word =>
          `${page.title} ${page.section} ${page.terms}`.toLowerCase().includes(word)))
          .sort((a, b) => Number(b.title.toLowerCase().includes(query)) - Number(a.title.toLowerCase().includes(query)))
          .slice(0, 12);
        status.textContent = hits.length ? `${hits.length} matching pages` : 'No matches. Try a module name or browse the module directory.';
        hits.forEach(page => {
          const item = document.createElement('li');
          const link = document.createElement('a');
          link.href = panel.dataset.root + page.url;
          link.textContent = page.title;
          const context = document.createElement('small');
          context.textContent = page.section.replaceAll('-', ' ');
          link.append(context);
          item.append(link);
          results.append(item);
        });
      } catch {
        request = undefined;
        status.textContent = 'Search is unavailable. Use the documentation navigation or module directory.';
      }
    });
  }
  document.querySelectorAll('pre').forEach(pre => {
    const code = pre.querySelector('code');
    if (!code || !navigator.clipboard) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'copy-button';
    button.textContent = 'Copy';
    button.setAttribute('aria-label', 'Copy code example');
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(code.textContent);
        button.textContent = 'Copied';
      } catch {
        button.textContent = 'Select code to copy';
      }
      setTimeout(() => { button.textContent = 'Copy'; }, 2500);
    });
    pre.append(button);
  });
})();
