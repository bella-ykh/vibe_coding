document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('menuButton');
  const sidebar = document.getElementById('sidebar');
  if (btn && sidebar) {
    btn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
      if (sidebar.classList.contains('collapsed')) {
        sidebar.style.width = '64px';
      } else {
        sidebar.style.width = '';
      }
    });
  }
});


