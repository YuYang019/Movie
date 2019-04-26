import React, { useState, useEffect } from 'react'
import { withRouter } from 'react-router'
import { Card, Row, Col, Button, message } from 'antd'

import './Rating.css'

import { getMovies } from '../api'
import Loading from '../components/Loading'
import MovieItem from '../components/MovieItem'
import mockData from '../mock/movies'


// const movies = mockData
// console.log(movies)

function Rating(props) {
  const [ isFetch, setIsFetch ] = useState(true)
  const [ movies, setMovies ] = useState(null)

  useEffect(() => {
    getMovies().then(data => {
      setIsFetch(false)
      setMovies(data)
      console.log(JSON.stringify(movies))
    })
  }, [])

  if (isFetch) {
    return (
      <Loading />
    )
  }

  const { history } = props
  console.log('render')
  // 此处的rating，不需要使用到视图上，所以不作为state
  let rating = {}

  function handleClick() {
    console.log(rating)
    const ratingLen = Object.keys(rating).length
    if (ratingLen !== 15) {
      message.error('电影未全部评分，请全部评分')
    } else {
      history.push('/result', { ...rating })
    }
  }

  function handleChange() {
    window.location.reload()
  }

  function handleRating(id, value) {
    rating = {
      ...rating,
      [id]: value
    }
  }

  return (
    <div className="rating">
      <p className="tip">
        请先对以下15部电影进行评分，方便我们收集您的喜好
        <Button className="change_btn" icon="redo" onClick={handleChange}>换一批电影</Button>
      </p>
      <div className="list">
        {
          movies ?
          movies.map(movie => (
            <MovieItem
              useRating={true}
              setRating={handleRating}
              key={movie.id}
              poster={movie.poster_url}
              id={movie.id}
              detail={movie.detail}
            />
          )) :
          null
        }
        <Button className="btn" type="primary" size="large" onClick={handleClick}>开始推荐</Button>
      </div>
    </div>
  )
}

export default withRouter(Rating)