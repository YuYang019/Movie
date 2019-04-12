import React from 'react'
import { Spin } from 'antd'
import './Loading.css'

function Loading() {
  return (
    <div className="loading">
      <div className="loading_icon">
        <Spin size="large" />
      </div>
    </div>
  )
}

export default Loading