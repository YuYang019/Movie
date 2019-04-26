import React from 'react'
import { Link } from 'react-router-dom'

import './Welcome.css'

function Welcome() {
  return (
    <div className="welcome">
      欢迎使用电影推荐系统
      <div className="link">
        <Link to="/rating">开始使用</Link>
      </div>
    </div>
  );
}

export default Welcome