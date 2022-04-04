import axios from 'axios'
import router from './routes.js'

const baseURL = 'http://127.0.0.1:8000';
const apiURL = baseURL + "/api";

const getAPI = axios.create({
    baseURL: apiURL,
    timeout: 5000,
});

getAPI.interceptors.response.use(null, error => {

    console.log(error);
    let path = ''
    switch (error.response.status) {
      case 404: path = 'notFoundPage'; break;
      case 403: path = 'forbiddenPage'; break;
    }
    router.push({name : path});
    return Promise.reject(error);
  });


const getAPIAuth = axios.create({
    baseURL: apiURL,
    timeout: 3000,
})

export { getAPI, getAPIAuth, baseURL }