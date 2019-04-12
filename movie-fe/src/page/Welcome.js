import React from 'react'
import { Link } from 'react-router-dom'

function Welcome() {
  return (
    <div className="welcome">
      欢迎使用电影推荐系统
      <Link to="/rating">开始</Link>
    </div>
  );
}

export default Welcome