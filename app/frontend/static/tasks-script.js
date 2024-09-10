document.addEventListener("DOMContentLoaded", () => {
    loadTasks();

    const form = document.getElementById("task-form");
    let editingTaskId = null;

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        const deadline = new Date(formData.get("deadline"));

        deadline.setHours(deadline.getHours() + 7);
        data.deadline = deadline.toISOString().slice(0, 19);

        if (editingTaskId) {
            await fetch(`/api/tasks/${editingTaskId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });

            editingTaskId = null;
        } else {
            await fetch("/api/tasks", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
        }
        form.reset();
        loadTasks();
    });
});


async function loadTasks() {
    const response = await fetch("/api/tasks");
    const tasks = await response.json();

    const tbody = document.getElementById("task-list-body");
    tbody.innerHTML = "";

    tasks.forEach((task) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td class="taskTitle">${task.title}</td>
            <td class="taskDescription">${task.description}</td>
            <td class="taskCategory">${task.category}</td>
            <td class="taskPriority">${task.priority}</td>
            <td class="taskAuthor">${task.author}</td>
            <td class="taskDeadline">${task.deadline}</td>
            <td class="taskCompleted">${task.completed ? "Да" : "Нет"}</td>
            <td class="taskDateCompleted">${task.date_completed || "-"}</td>
            <td class="taskActions">
                <button onclick="editTask(${task.id})">Редактировать</button>
                <button onclick="deleteTask(${task.id})">Удалить</button>
                <button onclick="markAsCompleted(${task.id})" ${task.completed ? "disabled" : ""}>Выполнено</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}


async function deleteTask(id) {
    await fetch(`/api/tasks/${id}`, { method: "DELETE" });
    loadTasks();
}


async function editTask(id) {
    const response = await fetch(`/api/tasks/${id}`);
    const task = await response.json();
    const form = document.getElementById('task-form');

    form.elements['title'].value = task.title;
    form.elements['description'].value = task.description;
    form.elements['category'].value = task.category;
    form.elements['priority'].value = task.priority;
    form.elements['author'].value = task.author;
    
    let deadline = new Date(task.deadline);

    const year = deadline.getFullYear();
    const month = String(deadline.getMonth() + 1).padStart(2, '0');
    const day = String(deadline.getDate()).padStart(2, '0');
    const hours = String(deadline.getHours()).padStart(2, '0');
    const minutes = String(deadline.getMinutes()).padStart(2, '0');

    const formattedDeadline = `${year}-${month}-${day}T${hours}:${minutes}`;

    form.elements['deadline'].value = formattedDeadline;

    editingTaskId = id;
    deleteTask(id);
}

async function markAsCompleted(id) {
    const completedDate = new Date().toISOString();
    await fetch(`/api/tasks/${id}/complete`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            completed: true,
            date_completed: completedDate,
        }),
    });
    loadTasks();
}