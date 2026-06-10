window.Architecture = {
  init: () => {
    document.querySelectorAll('.arch-node').forEach(node => {
      node.style.cursor = 'pointer';
    });
  }
};