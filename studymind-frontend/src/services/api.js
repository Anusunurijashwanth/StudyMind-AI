import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 120000
});

export const uploadPDF = async (formData) => {
  const res = await API.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
  return res.data;
};

export const askAI = async (question) => {
  const res = await API.get("/ask", {
    params: { question }
  });
  return res.data;
};

export const getStatus = async () => {
  const res = await API.get("/status");
  return res.data;
};