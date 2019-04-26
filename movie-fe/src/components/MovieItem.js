import React, { useState } from 'react'
import { Rate, Tooltip } from 'antd'
import './MovieItem.css'

function getGenres(genres) {
  let result = ''

  if (!genres) return ''
  
  for (let i = 0; i < genres.length; i++) {
    const g = genres[i]
    if (i === 0) {
      result += `${g.name}`
    } else {
      result += ` / ${g.name}`
    }
  }

  return result
}

function MovieItem(props) {

  const defaultProps = {
    id: null,
    poster: null,
    detail: null,
    useRating: null,
    setRating: null
  }

  const currentProps = {
    ...defaultProps,
    ...props,
  }

  const { id, poster, detail, useRating, setRating } = currentProps
  const [ value, setValue ] = useState(0)

  function handleChange(value) {
    setValue(value)
    setRating(id, value)
  }

  return (
    <div className="movie_item">
      <div className="item_left">
        <img src={ poster } alt="img"/>
      </div>
      <div className="item_right">
        <p className="title">
          { detail.title }
        </p>
        <p className="genres">
          { getGenres(detail.genres) }
        </p>
        <Tooltip title={ detail.overview }>
          <p className="overview">{ detail.overview }</p>
        </Tooltip>
        {
          useRating ?
          (
            <div className="rate">
              <Rate allowHalf value={value} onChange={handleChange} />
              <span className="number">{value ? `${value}分` : ''}</span>
            </div>
          )
          :
          null
        }
      </div>
    </div>
  )
}

export default MovieItem