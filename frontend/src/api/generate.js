import axios from 'axios'

export async function generateAnswer(data, token) {
  try {
    return await axios.post('/api/generate/', data, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
  } catch (error) {
    console.error('Fehler beim Generieren der Antwort:', error);
    throw error;
  }
}