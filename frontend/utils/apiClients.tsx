// Axios
import axios from 'axios';

export const flaskInstance = axios.create({
  baseURL: "http://localhost:5000"
})
flaskInstance.defaults.headers.post['Content-Type'] = 'application/json';
flaskInstance.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

export const nextInstance = axios.create({
  baseURL: "http://localhost:3000"
});
nextInstance.defaults.headers.post['Content-Type'] = 'application/json';
nextInstance.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
