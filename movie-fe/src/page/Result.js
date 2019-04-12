import React, { useState, useEffect } from 'react'
import { withRouter } from 'react-router'

import './Result.css'
import { getRecommended } from '../api'
import Loading from '../components/Loading'
import MovieItem from '../components/MovieItem'

function Result(props) {
  const [ isFetch, setIsFetch ] = useState(true)
  const [ movies, setMovies ] = useState(null)
  const { location } = props
  const params = location.state

  // 第二个参数，传空数组，表明effect永远不需要重复执行
  // 在这个组件里，推荐电影只需要获取一次
  useEffect(() => {
    getRecommended(params).then(data => {
      setIsFetch(false)
      setMovies(data)
      console.log(data)
    })
  }, [])

  console.log('render')

  if (isFetch) {
    return (
      <Loading />
    )
  }

  return (
    <div className="result">
      <p className="tip">为您推荐的10部电影：</p>
      <div className="list">
        {
          movies ?
          movies.map(movie => (
            <MovieItem
              key={movie.id}
              poster={movie.poster_url}
              id={movie.id}
              detail={movie.detail}
            />
          )) :
          null
        }
      </div>
    </div>
  )
}

export default withRouter(Result)