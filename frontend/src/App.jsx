import { useState, useEffect } from "react"
import axios from "axios"

function App() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")
  const [token, setToken] = useState(localStorage.getItem("token") || "")
  const [tasks, setTasks] = useState([])

  const [title, setTitle] = useState("")
  const [deadline, setDeadline] = useState("")
  const [hours, setHours] = useState("")
  const [priority, setPriority] = useState("medium")

  const register = async () => {
    try {
      await axios.post("http://127.0.0.1:8000/auth/register", {
        email,
        password,
      })
      setMessage("User registered successfully")
    } catch {
      setMessage("Registration failed")
    }
  }

  const login = async () => {
    try {
      const formData = new URLSearchParams()
      formData.append("username", email)
      formData.append("password", password)

      const response = await axios.post(
        "http://127.0.0.1:8000/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      )

      setToken(response.data.access_token)
      localStorage.setItem("token", response.data.access_token)
      setMessage("Login successful")
    } catch {
      setMessage("Login failed")
    }
  }

  const logout = () => {
    localStorage.removeItem("token")
    setToken("")
  }

  const fetchTasks = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/tasks/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      setTasks(response.data)
    } catch (error) {
      console.log(error)
    }
  }

  const createTask = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/tasks/",
        {
          title,
          description: "",
          deadline,
          estimated_hours: Number(hours),
          priority,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      setTitle("")
      setHours("")
      setDeadline("")
      setPriority("medium")
      fetchTasks()
    } catch {
      setMessage("Task creation failed")
    }
  }

  const toggleComplete = async (task) => {
    try {
      await axios.put(
        `http://127.0.0.1:8000/tasks/${task.id}`,
        {
          ...task,
          status: task.status === "completed" ? "pending" : "completed",
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      fetchTasks()
    } catch (error) {
      console.log(error)
    }
  }

  const deleteTask = async (id) => {
    try {
      await axios.delete(
        `http://127.0.0.1:8000/tasks/${id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      fetchTasks()
    } catch (error) {
      console.log(error)
    }
  }

  useEffect(() => {
    if (token) fetchTasks()
  }, [token])

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-6">
     <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-2xl p-8">
        <h1 className="text-3xl font-bold text-center text-indigo-600 mb-8">
          Smart Study Planner
        </h1>

        {!token ? (
          <div className="space-y-4 max-w-md mx-auto">
            <input
              className="w-full border p-3 rounded-lg"
              placeholder="Email"
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              type="password"
              className="w-full border p-3 rounded-lg"
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
            />

            <div className="flex gap-4">
              <button
                onClick={register}
                className="w-full bg-green-500 text-white p-3 rounded-lg"
              >
                Register
              </button>

              <button
                onClick={login}
                className="w-full bg-indigo-500 text-white p-3 rounded-lg"
              >
                Login
              </button>
            </div>

            {message && (
              <p className="text-center text-sm text-gray-600">{message}</p>
            )}
          </div>
        ) : (
          <>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Create New Task</h2>
              <button
                onClick={logout}
                className="bg-red-500 text-white px-4 py-2 rounded-lg"
              >
                Logout
              </button>
            </div>

            <div className="grid md:grid-cols-4 gap-4 mb-6">
              <input
                className="border p-2 rounded-lg"
                placeholder="Task Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />

              <input
                type="datetime-local"
                className="border p-2 rounded-lg"
                value={deadline}
                onChange={(e) => setDeadline(e.target.value)}
              />

              <input
                type="number"
                className="border p-2 rounded-lg"
                placeholder="Hours"
                value={hours}
                onChange={(e) => setHours(e.target.value)}
              />

              <select
                className="border p-2 rounded-lg"
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <button
              onClick={createTask}
              className="w-full bg-indigo-600 text-white p-3 rounded-lg mb-6"
            >
              Create Task
            </button>

            <div className="grid grid-cols-3 gap-4 mb-6 text-center">
              <div className="bg-indigo-100 p-4 rounded-xl">
                <h3 className="text-lg font-bold">{tasks.length}</h3>
                <p className="text-sm">Total</p>
              </div>

              <div className="bg-green-100 p-4 rounded-xl">
                <h3 className="text-lg font-bold">
                  {tasks.filter(t => t.status === "completed").length}
                </h3>
                <p className="text-sm">Completed</p>
              </div>

              <div className="bg-yellow-100 p-4 rounded-xl">
                <h3 className="text-lg font-bold">
                  {tasks.filter(t => t.status !== "completed").length}
                </h3>
                <p className="text-sm">Pending</p>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className="bg-gray-50 p-4 rounded-xl shadow"
                >
                  <h3 className="font-bold text-lg">{task.title}</h3>
                  <p className="text-sm">Priority: {task.priority}</p>
                  <p className="text-sm mb-3">Status: {task.status}</p>

                  <div className="flex gap-2">
                    <button
                      onClick={() => toggleComplete(task)}
                      className="bg-green-500 text-white px-3 py-1 rounded"
                    >
                      Complete
                    </button>

                    <button
                      onClick={() => deleteTask(task.id)}
                      className="bg-red-500 text-white px-3 py-1 rounded"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default App