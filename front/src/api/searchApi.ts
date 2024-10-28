import axios from 'axios';

const API_URL = 'http://localhost:8000'; // URL для Django API

// Создаем поиск
export const createSearch = async (data: {
  text?: string;
  file_mask?: string;
  size?: { value: number; operator: string };
  creation_time?: { value: string; operator: string };
}) => {
  const response = await axios.post(`${API_URL}/searches`, data);
  return response.data;
};

// Получаем результаты поиска
export const getSearchResults = async (searchId: string) => {
  const response = await axios.get(`${API_URL}/searches/${searchId}`);
  return response.data;
};
