import axios from 'axios'

export function generateAnswer(data) {
  return axios.post('/api/generate/', data)
}