import axios from 'axios'
import router from './routes.js'

//server rest
const baseURL = 'https://eventspot.srvz-webapp.he-arc.ch';
const apiURL = baseURL + "/api";

//create a axios pointing on rest
const getAPI = axios.create({
    baseURL: apiURL,
    timeout: 5000,
});

//intercept errors to reddirect
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

//used to refresh token
const getAPIAuth = axios.create({
    baseURL: apiURL,
    timeout: 3000,
})

export { getAPI, getAPIAuth, baseURL }
