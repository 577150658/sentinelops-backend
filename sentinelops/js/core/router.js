export const Router = {
  current() { return location.hash.replace(/^#\/?/, '') || 'dashboard'; },
  go(pageId) { location.hash = `#/${pageId}`; },
};
