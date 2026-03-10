const API_URL = "https://smart-study-planner-backend-e223.onrender.com";

export const getTasks = async (token) => {
  const res = await fetch(`${API_URL}/tasks/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
};

export const deleteTask = async (id, token) => {
  await fetch(`${API_URL}/tasks/${id}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const completeTask = async (id, token) => {
  await fetch(`${API_URL}/tasks/${id}/complete`, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const getStats = async (token) => {
  const res = await fetch(`${API_URL}/tasks/stats`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
};