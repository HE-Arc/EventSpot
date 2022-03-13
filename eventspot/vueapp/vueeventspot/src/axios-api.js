import axios from 'axios'
import router from './routes.js'

const getAPI = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    timeout: 1000,
});



getAPI.interceptors.response.use(null, error => {

    let path = ''
    switch (error.response.status) {
      case 404: path = 'notFoundPage'; break;
    }
    router.push({name : path});
    return Promise.reject(error);
  });


export { getAPI }