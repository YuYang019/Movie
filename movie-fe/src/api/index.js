import axios from 'axios'

export const getMovies = (params) => axios.get('/movies', { params }).then(res => res.data)

export const getRecommended = (params) => axios.post('/recommend', params).then(res => res.data)