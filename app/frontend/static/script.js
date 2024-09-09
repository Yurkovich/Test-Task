
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();

    const form = document.getElementById('task-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        data.deadline = new Date(data.deadline).toISOString();

        await fetch('/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        form.reset();
        loadTasks();
    });
});

async function loadTasks() {
    const response = await fetch('/api/tasks');
    const tasks = await response.json();

    const tbody = document.getElementById('task-list-body');
    tbody.innerHTML = '';

    tasks.forEach(task => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${task.title}</td>
            <td>${task.description}</td>
            <td>${task.category}</td>
            <td>${task.priority}</td>
            <td>${task.author}</td>
            <td>${task.deadline}</td>
            <td>${task.completed ? 'Да' : 'Нет'}</td>
            <td>${task.date_completed || '-'}</td>
            <td>
                <!-- Действия, такие как редактирование и удаление -->
                <button onclick="editTask(${task.id})">Редактировать</button>
                <button onclick="deleteTask(${task.id})">Удалить</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function deleteTask(id) {
    await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
    loadTasks();
}

function editTask(id) {
    // Логика для редактирования задачи
}
