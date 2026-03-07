const TaskCard = ({ task, onDelete, onComplete }) => {
  return (
    <div className="bg-white shadow-md p-4 rounded-lg mb-3">
      <h3 className="text-lg font-bold">{task.title}</h3>
      <p>{task.description}</p>
      <p>Priority: {task.priority}</p>
      <p>Status: {task.status}</p>

      <div className="mt-3 flex gap-2">
        <button
          onClick={() => onComplete(task.id)}
          className="bg-green-500 text-white px-3 py-1 rounded"
        >
          Complete
        </button>

        <button
          onClick={() => onDelete(task.id)}
          className="bg-red-500 text-white px-3 py-1 rounded"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskCard;