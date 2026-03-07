import { useEffect, useState } from "react";
import TaskCard from "../components/TaskCard";
import StatsCard from "../components/StatsCard";
import { getTasks, deleteTask, completeTask, getStats } from "../services/api";

const Dashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState({});
  const token = localStorage.getItem("token");

  const loadData = async () => {
    const taskData = await getTasks(token);
    const statsData = await getStats(token);
    setTasks(taskData);
    setStats(statsData);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleDelete = async (id) => {
    await deleteTask(id, token);
    loadData();
  };

  const handleComplete = async (id) => {
    await completeTask(id, token);
    loadData();
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Smart Study Planner</h1>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <StatsCard title="Total" value={stats.total_tasks} />
        <StatsCard title="Completed" value={stats.completed_tasks} />
        <StatsCard title="Pending" value={stats.pending_tasks} />
        <StatsCard title="High Priority" value={stats.high_priority_tasks} />
      </div>

      {/* Tasks */}
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onDelete={handleDelete}
          onComplete={handleComplete}
        />
      ))}
    </div>
  );
};

export default Dashboard;