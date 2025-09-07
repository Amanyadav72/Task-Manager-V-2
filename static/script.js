document.addEventListener('DOMContentLoaded', () => {
  const taskItems = document.querySelectorAll('.task-list li');

  taskItems.forEach(item => {
    item.addEventListener('click', () => {
      item.classList.toggle('done');
      // Optional: send update to backend via fetch()
      // fetch('/update-task', { method: 'POST', body: JSON.stringify({ id: item.dataset.id }) })
    });
  });
});
