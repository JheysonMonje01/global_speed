import axios from "axios";

const API_URL = "http://localhost:5000/api/auth/login";

export const login = async (email: string, password: string) => {
  try {
    const response = await axios.post(API_URL, { email, password });
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      throw error.response?.data?.message || "Error al iniciar sesión";
    }
    throw "Ocurrió un error inesperado";
  }
};
