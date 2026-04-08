export const API_BASE_URL = "http://localhost:8000";

export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/analyze-image`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to analyze image");
  }
  return response.json();
};

export const generateRecipe = async (ingredients) => {
  const response = await fetch(`${API_BASE_URL}/generate-recipe`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ingredients }),
  });

  if (!response.ok) {
    throw new Error("Failed to generate recipe");
  }
  return response.json();
};

export const fetchHistory = async () => {
  const response = await fetch(`${API_BASE_URL}/recipes`);
  if (!response.ok) {
    throw new Error("Failed to fetch history");
  }
  return response.json();
};
